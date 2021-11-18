
"""A collection of functions to measure the performance of queues.
To ensure that we are only measuring the desired operation, we
break encapsulation and directly access the underlying data structure.
"""


from ..datatypes.queues import DequeQueue, Queue, BoundedQueue, ArrayQueue


def init_queue(queue: Queue, length: int) -> Queue:
    """Populate a queue with length-1 items.
    """
    for num in range(length-1):
        queue.enqueue(num)
    return queue


def runtime_bq_enqueue(bq: BoundedQueue, end: int) -> None:
    """Add items to queue.
    """
    bq.enqueue(0)
    del bq._items[end-1]
    bq._size -= 1


def runtime_bq_dequeue(bq: BoundedQueue) -> None:
    bq.dequeue()
    bq._items[0] = 0
    bq._size += 1


def runtime_aq_enqueue(aq: ArrayQueue, end: int) -> None:
    """Add items to queue.
    """
    aq.enqueue(0)
    del aq._items[end-1]
    aq._size -= 1


def runtime_aq_dequeue(aq: ArrayQueue) -> None:
    aq.dequeue()
    aq._items[0] = 0
    aq._size += 1


def runtime_dq_enqueue(dq: ArrayQueue, end: int) -> None:
    """Add items to queue.
    """
    dq.enqueue(0)
    del dq._items[end-1]


def runtime_dq_dequeue(dq: DequeQueue) -> None:
    dq.dequeue()
    dq.enqueue(0)
