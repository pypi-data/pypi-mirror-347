import asyncio
import collections.abc
import contextlib
import inspect
import time

import typing_extensions as typing

from .sila.utils import clear_interval, set_interval

T = typing.TypeVar("T")


class Subject(typing.Generic[T]):
    def __init__(
        self,
        maxsize: int = 0,
        default: typing.Optional[T] = None,
    ) -> None:
        self._maxsize = maxsize
        self._value: typing.Optional[T] = default
        self.subscribers: list[asyncio.Queue[T]] = []
        self._queue_tasks: set[asyncio.Task] = set()

    @property
    def current(self) -> typing.Optional[T]:
        """The current value."""
        return self._value

    async def get(
        self,
        predicate: typing.Callable[[T], bool] = lambda _: True,
        timeout: typing.Optional[float] = None,
        current: bool = False,
    ) -> T:
        """
        Request an upcoming event that satisfies the predicate.

        Args:
          predicate: A filter predicate to apply.
          timeout: How many seconds to wait for new value.
          current: Whether to check the current value against the predicate.

        Raises:
          TimeoutError
        """

        queue = self.add()
        start_time = time.perf_counter()

        if all((current, (value := self.current), predicate(value))):
            return value

        try:
            while True:
                wait_for = timeout + start_time - time.perf_counter() if timeout is not None else None

                try:
                    value = await asyncio.wait_for(queue.get(), timeout=wait_for)
                    queue.task_done()
                except (TimeoutError, asyncio.TimeoutError):
                    raise TimeoutError from None

                if predicate(value):
                    return value
        finally:
            self.remove(queue)

    async def subscribe(self, abort: typing.Optional[asyncio.Event] = None) -> typing.AsyncIterator[T]:
        """
        Subscribe to changes from this `Subject`.

        Args:
          abort: An cancellable event, allowing subscriptions to be terminated.
        """
        queue = self.add()

        abort = abort or asyncio.Event()
        cancellation = asyncio.create_task(abort.wait())

        try:
            while not abort.is_set():
                queue_task = asyncio.create_task(queue.get())
                self._queue_tasks.add(queue_task)
                queue_task.add_done_callback(self._queue_tasks.discard)

                done, pending = await asyncio.wait((queue_task, cancellation), return_when=asyncio.FIRST_COMPLETED)

                if queue_task in done:
                    value = queue_task.result()
                    yield value

                if cancellation in done:
                    for pending_task in pending:
                        with contextlib.suppress(asyncio.TimeoutError):
                            await asyncio.wait_for(pending_task, 0)
                    break

        except asyncio.CancelledError:
            cancellation.cancel()
        finally:
            self.remove(queue)

    def notify(self) -> None:
        """Propagate updates to the current value to all subscribers."""
        if self._value is not None:
            for subscriber in self.subscribers:
                subscriber.put_nowait(self._value)

    def update(self, value: T) -> None:
        """Update the current value of this `Subject`, if `value` is not current value."""
        if self._value != value:
            self._value = value
            self.notify()

    def add(self) -> asyncio.Queue:
        """Add a subscriber to this `Subject`."""
        queue = asyncio.Queue[T](maxsize=self._maxsize)
        if self._value is not None:
            queue.put_nowait(self._value)

        self.subscribers.append(queue)

        return queue

    def remove(self, subscriber: asyncio.Queue) -> None:
        """Remove a subscriber from this `Subject`."""
        self.subscribers.remove(subscriber)

        if not self.subscribers:
            for task in self._queue_tasks:
                task.cancel()
            self._queue_tasks.clear()


class Publisher(typing.Generic[T], Subject[T]):
    """
    Manage a subscription which updates itself by polling a data source.

    Args:
      maxsize: The maximum number of messages to track in the queue.
      source: An awaitable method that will be called at a fixed interval as the data source of the subscription.
      interval: How many seconds to wait between polling calls to `source`.

    Examples:
      Create a publisher and set a temporary source for subscriptions:
      >>> publisher = Publisher[str](maxsize=100)
      >>> publisher.set(method, interval=2)
      >>> async for state in publisher.subscribe():
      >>>     yield state

      Create a publisher with a stable source:
      >>> publisher = Publisher[str](maxsize=100, source=method, interval=2)
      >>> async for state in publisher.subscribe():
      >>>     yield state
    """

    def __init__(
        self,
        maxsize: int = 0,
        source: typing.Optional[typing.Union[collections.abc.Coroutine[None, None, T], typing.Callable[[], T]]] = None,
        interval: float = 5,
    ) -> None:
        super().__init__(maxsize)

        self._setter: typing.Optional[
            typing.Union[collections.abc.Coroutine[None, None, T], typing.Callable[[], T]]
        ] = None
        self._update_task: typing.Optional[asyncio.Task] = None
        self._source = source
        self._interval = interval

    @typing.override
    def add(self) -> asyncio.Queue:
        if self._source and not self._update_task:
            self.set(self._source, self._interval)

        return super().add()

    def set(
        self,
        setter: typing.Union[collections.abc.Coroutine[None, None, T], typing.Callable[[], T]],
        interval: float = 5,
    ) -> None:
        """
        Create a temporary background task to poll data from an awaitable method and update `Publisher`.

        Task will be destroyed when all subscriptions to the `Publisher` are removed.

        Args:
          setter: The awaitable called at a fixed interval to update the current value of the `Publisher`.
          interval: The amount of time in seconds to wait between polling calls to `setter`.
        """
        if self._setter:
            msg = "Publisher already has a source set."
            raise ValueError(msg)
        self._setter = setter
        self._update_task = set_interval(self.__self_update, delay=interval)

    async def __self_update(self) -> None:
        if self._setter:
            if inspect.iscoroutinefunction(self._setter):
                new_value = await self._setter()
            else:
                new_value = self._setter()
            self.update(new_value)

    async def subscribe(self, abort: typing.Optional[asyncio.Event] = None) -> typing.AsyncIterator[T]:
        """
        Subscribe to updates from this Publisher.

        Args:
          abort: An cancellable event, allowing subscriptions to be terminated.

        Examples:
          Set and subscribe to a publisher with a temporary source:
          >>> publisher = Publisher[str](maxsize=100)
          >>> publisher.set(method, interval=2)
          >>> async for state in publisher.subscribe():
          >>>     yield state

          Subscribe to a publisher with a stable source:
          >>> publisher = Publisher[str](maxsize=100, source=method, interval=2)
          >>> async for state in publisher.subscribe():
          >>>     yield state
        """
        if self._source and not self._update_task:
            self.set(self._source, self._interval)

        return super().subscribe(abort)

    @typing.override
    def remove(self, subscriber: asyncio.Queue) -> None:
        super().remove(subscriber)
        if not self.subscribers and self._update_task:
            clear_interval(self._update_task)
            self._update_task = None
            self._setter = None
