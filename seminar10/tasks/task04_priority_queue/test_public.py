import pytest

from seminar10.tasks.task04_priority_queue.priority_queue import PriorityQueue

pytestmark = pytest.mark.timeout(5)


def test_smallest_priority_first_and_peek_does_not_remove() -> None:
    queue = PriorityQueue[str]()
    queue.push(10, "позже")
    queue.push(-2, "срочно")
    queue.push(0, "обычно")
    assert len(queue) == 3
    assert queue.peek() == "срочно"
    assert queue.peek() == "срочно"
    assert len(queue) == 3
    assert [queue.pop(), queue.pop(), queue.pop()] == ["срочно", "обычно", "позже"]
    assert len(queue) == 0


def test_equal_priorities_keep_fifo_order_even_after_a_pop() -> None:
    queue = PriorityQueue[str]()
    queue.push(2, "first")
    queue.push(2, "second")
    assert queue.pop() == "first"
    queue.push(2, "third")
    queue.push(1, "urgent")
    assert [queue.pop(), queue.pop(), queue.pop()] == ["urgent", "second", "third"]


def test_payloads_are_never_compared_or_copied() -> None:
    class Payload:
        def __lt__(self, other: object) -> bool:
            raise AssertionError("Сравнение данных запрещено")

        def __eq__(self, other: object) -> bool:
            raise AssertionError("Сравнение данных запрещено")

    first, second = Payload(), Payload()
    queue = PriorityQueue[Payload]()
    queue.push(0, first)
    queue.push(0, second)
    assert queue.peek() is first
    assert queue.pop() is first
    assert queue.pop() is second


def test_false_values_are_valid_payloads() -> None:
    queue = PriorityQueue[object]()
    for item in (None, False, 0, ""):
        queue.push(0, item)
    assert [queue.pop() for _ in range(4)] == [None, False, 0, ""]


def test_empty_operations_raise_but_queue_can_be_reused() -> None:
    queue = PriorityQueue[int]()
    for _ in range(2):
        with pytest.raises(IndexError):
            queue.peek()
        with pytest.raises(IndexError):
            queue.pop()
        assert len(queue) == 0
        queue.push(1, 42)
        assert queue.pop() == 42


def test_instances_do_not_share_state() -> None:
    first = PriorityQueue[int]()
    second = PriorityQueue[int]()
    first.push(1, 10)
    second.push(0, 20)
    assert first.pop() == 10
    assert second.pop() == 20
