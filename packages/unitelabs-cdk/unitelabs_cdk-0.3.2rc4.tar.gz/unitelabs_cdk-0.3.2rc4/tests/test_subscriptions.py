import asyncio
import typing
import unittest.mock

import pytest

from unitelabs.cdk import Publisher, Subject

DEFAULT_VALUE = "default"
ONE_OP_TIME = 0.01


class TestSubject(Subject[str]):
    def __init__(self) -> None:
        super().__init__(maxsize=10, default=DEFAULT_VALUE)
        self._tasks = set()

    def _create_task(
        self, method: typing.Coroutine[typing.Awaitable, None, None]
    ) -> typing.Generator[asyncio.Task, None, None]:
        bg_update = asyncio.create_task(method)
        self._tasks.add(bg_update)
        bg_update.add_done_callback(self._tasks.discard)

        yield bg_update

        bg_update.cancel()
        self._tasks.discard(bg_update)


async def redundant_update(subject: Subject[str]) -> None:
    """Update the subject 10x, once per operation time, with redundant updates after the first iteration."""
    for x in range(1, 11):
        if x > 1:
            subject.update(f"update {x - 1}")  # redundant update
        subject.update(f"update {x}")
        await asyncio.sleep(ONE_OP_TIME)


async def bg_cancel(cancel_event: asyncio.Event):
    """Set the cancel event after a delay of ~5 operations."""
    await asyncio.sleep(ONE_OP_TIME * 5)
    cancel_event.set()


@pytest.fixture
def test_subject() -> TestSubject:
    return TestSubject()


class TestSubject_Defaults:
    async def test_should_set_default_value(self):
        subject = Subject[str]()
        assert subject.current is None

    async def test_get_should_timeout(self):
        subject = Subject[str]()
        with pytest.raises(TimeoutError):
            await subject.get(timeout=0.01)

    async def test_should_set_default_maxsize(self):
        subject = Subject[str]()
        sub = subject.add()

        assert sub.maxsize == 0


class TestSubject_Subscribe:
    async def test_should_return_default_if_nothing_queued(self):
        subject = TestSubject()

        async for value in subject.subscribe():
            assert value == DEFAULT_VALUE
            if value == DEFAULT_VALUE:
                return

    async def test_should_only_notify_on_changed_value(self):
        subject = TestSubject()
        subject.update = unittest.mock.Mock(wraps=subject.update)
        subject.notify = unittest.mock.Mock(wraps=subject.notify)

        update_task = next(subject._create_task(redundant_update(subject)))
        await asyncio.sleep(ONE_OP_TIME * 10 + 0.05)

        assert update_task.done()
        assert not subject._tasks
        assert subject.update.call_count == 19
        assert subject.notify.call_count == 10

    async def test_should_be_cancellable(self):
        subject = TestSubject()
        cancel_event = asyncio.Event()

        cancel_task = next(subject._create_task(bg_cancel(cancel_event)))

        async for value in subject.subscribe(cancel_event):
            assert value == DEFAULT_VALUE

        assert not subject._tasks
        assert cancel_event.is_set()
        assert cancel_task.done()

    async def test_should_be_cancellable_with_update_task(self):
        subject = TestSubject()
        cancel_event = asyncio.Event()

        update_task = next(subject._create_task(redundant_update(subject)))
        cancel_task = next(subject._create_task(bg_cancel(cancel_event)))
        # will cancel self after 5 operations
        values = [value async for value in subject.subscribe(cancel_event)]

        assert values == [DEFAULT_VALUE, *[f"update {x}" for x in range(1, 6)]]

        assert cancel_event.is_set()
        assert cancel_task.done()
        assert subject._tasks == {update_task}

        # update task is not set on publisher, thus it should still be running
        assert not update_task.cancelled()


class TestSubject_Get:
    async def test_should_return_default_if_nothing_queued(self):
        subject = TestSubject()
        assert await subject.get() == DEFAULT_VALUE

    async def test_should_return_default_if_nothing_queued_with_timeout(self):
        subject = TestSubject()
        assert await subject.get(timeout=0.5) == DEFAULT_VALUE

    async def test_should_timeout_if_nothing_queued_matching_predicate(self):
        subject = TestSubject()
        with pytest.raises(TimeoutError):
            await subject.get(lambda x: x != DEFAULT_VALUE, timeout=0.05)

    async def test_should_return_immediately_if_predicate_matches_current_value(self):
        subject = TestSubject()
        subject.notify = unittest.mock.Mock(wraps=subject.notify)
        update_task = next(subject._create_task(redundant_update(subject)))

        assert subject.current != await subject.get(lambda x: "update" in x)
        assert subject.current == await subject.get(lambda x: "update" in x, current=True)

        update_task.cancel()


class TestSubject_Update:
    async def test_should_update_current_value(self):
        subject = TestSubject()
        subject.update("new value")
        assert subject.current == "new value"

    async def test_should_not_notify_if_value_is_current(self):
        subject = TestSubject()
        subject.notify = unittest.mock.Mock(wraps=subject.notify)
        subject.update(DEFAULT_VALUE)
        subject.notify.assert_not_called()


class TestSubject_Add:
    async def test_should_add_subscription(self):
        subject = TestSubject()
        sub = subject.add()
        assert isinstance(sub, asyncio.Queue)
        assert sub in subject.subscribers
        assert await sub.get() == DEFAULT_VALUE


class TestSubject_Remove:
    async def test_should_remove_subscription(self):
        subject = TestSubject()
        sub = subject.add()
        assert sub in subject.subscribers
        subject.remove(sub)
        assert sub not in subject.subscribers

    async def test_should_raise_value_error_on_unknown_subscription(self):
        subject = TestSubject()
        with pytest.raises(ValueError):
            subject.remove(asyncio.Queue())

    async def test_should_raise_value_error_on_twice_removed(self):
        subject = TestSubject()
        sub = subject.add()
        subject.remove(sub)
        with pytest.raises(ValueError):
            subject.remove(sub)


class TestPublisher_Get:
    async def test_should_timeout_if_no_source_and_not_set(self):
        pub = Publisher[str](maxsize=10)
        with pytest.raises(TimeoutError):
            await pub.get(timeout=0.01)

    async def test_should_return_immediately_if_source(self):
        gen = (f"value {i}" for i in range(10))
        pub = Publisher[str](maxsize=10, source=lambda: next(gen), interval=ONE_OP_TIME)
        assert await pub.get() == "value 0"

        assert await pub.get(current=True) == "value 0"

        assert pub.current == "value 0"

    async def test_should_return_immediately_if_set(self):
        pub = Publisher[str](maxsize=10)
        pub.set(lambda: "value", interval=ONE_OP_TIME)
        assert await pub.get() == "value"
        assert await pub.get(current=True) == "value"
        assert pub.current == "value"

        pub.set(lambda: "value2", interval=ONE_OP_TIME)
        assert await pub.get(current=True) == "value"
        assert await pub.get() == "value2"
        assert pub.current == "value2"


class TestPublisher_Add:
    async def test_should_start_polling_if_initialized_with_source(self):
        pub = Publisher[str](maxsize=10, source=lambda: "value", interval=ONE_OP_TIME)
        assert not pub._update_task
        assert not pub._setter

        sub = pub.add()
        await asyncio.sleep(ONE_OP_TIME)
        assert sub.qsize() >= 1
        assert pub._update_task
        assert pub._setter

        pub.remove(sub)

    async def test_should_start_polling_if_set_after_addition_no_source(self):
        pub = Publisher[str](maxsize=10)
        assert not pub._update_task
        assert not pub._setter

        sub = pub.add()
        assert sub.qsize() == 0
        assert not pub._update_task
        assert not pub._setter

        pub.set(lambda: "value", interval=ONE_OP_TIME)
        await asyncio.sleep(ONE_OP_TIME)
        assert sub.qsize() >= 1
        assert pub._update_task
        assert pub._setter

        pub.remove(sub)

    async def test_should_not_start_polling_again_if_other_subscribers(self):
        pub = Publisher[str](maxsize=10, source=lambda: "value", interval=ONE_OP_TIME)
        pub.set = unittest.mock.Mock(wraps=pub.set)
        assert not pub._update_task
        assert not pub._setter

        sub = pub.add()
        assert pub._update_task
        assert pub._setter
        pub.set.assert_called_once()
        pub.set.reset_mock()

        sub2 = pub.add()
        pub.set.assert_not_called()

        for s in [sub, sub2]:
            pub.remove(s)


class TestPublisher_Remove:
    async def test_should_cancel_source_generated_update_task_if_no_subscribers(self):
        # create a data generator for the publisher
        x = 0

        async def get_next_value() -> str:
            nonlocal x
            x += 1
            return f"update {x}"

        pub = Publisher[str](maxsize=10, source=get_next_value, interval=ONE_OP_TIME)
        assert not pub._update_task
        assert not pub._setter

        # create subscription and let it run for a while
        sub = pub.add()
        iterations = 5
        await asyncio.sleep(ONE_OP_TIME * iterations)

        # check that internals are set and queue is being populated
        assert sub.qsize() >= iterations + 1
        assert pub._update_task
        assert pub._setter

        # save a reference to the task and remove the subscription
        task = pub._update_task
        pub.remove(sub)

        # check that internals from source are cleared
        assert not pub._update_task
        assert not pub._setter

        # give the task some to time to be gracefully cancelled
        await asyncio.sleep(0.01)
        assert task.cancelled()

    async def test_should_cancel_set_generated_update_task_if_no_subscribers(self):
        pub = Publisher[str](maxsize=10)
        assert not pub._update_task
        assert not pub._setter

        # create generator outside of set to ensure single-use
        values_gen = (f"value {x}" for x in range(10))
        pub.set(lambda: next(values_gen), interval=ONE_OP_TIME)

        # create a subscription and let it run for a while
        sub = pub.add()
        iterations = 5
        await asyncio.sleep(ONE_OP_TIME * iterations)

        # check that internals are set and queue is being populated
        assert sub.qsize() >= iterations + 1
        assert pub._update_task
        assert pub._setter

        # save a reference to the task and remove the subscription
        task = pub._update_task
        pub.remove(sub)

        # check that internals from set are cleared
        assert not pub._update_task
        assert not pub._setter

        # give the task some to time to be gracefully cancelled
        await asyncio.sleep(0.01)
        assert task.cancelled()
