
"""Implementation of black-box testing for the Queue.
"""


from .util import check
from ..datatypes.queues import Queue, BoundedQueue, ArrayQueue, LinkedQueue, DequeQueue, SequenceQueue


def test_is_empty(items: Queue, is_empty: bool) -> None:
    """Check whether items is empty of not.
    """
    check("is empty", items.is_empty(), is_empty, items)


def test_init_empty(items: Queue) -> None:
    """Check that items is the empty queue.
    """
    test_is_empty(items, True)


def test_front(items: Queue, item: object) -> None:
    """Check if front of queue is item.
    """
    check("front of queue", items.front(), item, items)


def test_enqueue(items: Queue, length: int) -> None:
    """Add length items to the queue, check the length.
    """
    for num in range(length):
        items.enqueue(num)
        check("enqueue", len(items), num+1, items)
    test_is_empty(items, False)


def test_front(items: Queue, length: int) -> None:
    """Add length items to the queue, check the front.
    """
    expected: list[int] = []
    for num in range(length):
        expected.append(num)
        items.enqueue(num)
        check("front, enqueue", items.front(), 0, items)
    expected: list[int] = []
    for num in range(length):
        items.dequeue()
        if not items.is_empty():
            check("front, dequeue", items.front(), num+1, items)


def test_dequeue(items: Queue, length: int) -> None:
    """Remove length items from the queue, check the length, check if empty.
    """
    for num in range(length):
        items.enqueue(num)
    for num in range(length-1, -1, -1):
        items.dequeue()
        check("dequeue", len(items), num, items)
    test_is_empty(items, True)
