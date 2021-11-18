
"""Various implementations of the Queue ADT, as defined by M269.
"""

from . import arrays as _arrays
from .sequences import ArraySequence as _ArraySequence
from .linkedlists import LinkedList as _LinkedList
from collections import deque as _deque
import math as _math


class Queue:
    """A queue is a data structure of a linear collection of items in
    which access is restricted to a first-in first-out basis. New items
    are inserted at the back and existing items are removed from the front.
    The items are maintained in the order in which they are added to the
    structure.
    """

    def __len__(self) -> int:
        """Return the number of items in the queue.

        Postconditions: 0 <= len(self)
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        """Return a string representation of the queue.
        """
        items = []
        for index in range(len(self)):
            items.append(self._items[index])
        return str(items)

    def is_empty(self) -> bool:
        """Return true if the stack is empty, otherwise false.

        Postcondtions: output is true if len(self) == 0
        """
        return len(self) == 0

    def front(self) -> object:
        """Return the item from the front of the queue.

        Preconditions: len(self) >= 1
        Postcondtions: output is self[0]
        """
        pass

    def enqueue(self, item: object) -> None:
        """Adds the given item to the back of the queue.

        Postconditions: post-self is pre-self[0], ... , pre-self[len(self)-1],
        item
        """
        pass

    def dequeue(self) -> None:
        """Remove the front item from the queue.

        Preconditions: len(self) >= 1
        Postconditions: post-self is pre-self[1], ... , pre-self[len(self)-1]
        """
        pass


class BoundedQueue(Queue):
    """A static array implementation of the queue adt.
    """

    def __init__(self, capacity: int) -> None:
        """Initialise an empty queue with given capacity.
        """
        self._items: _arrays.StaticArray = _arrays.StaticArray(capacity)
        self._size: int = 0

    @property
    def capacity(self) -> int:
        """Maximum number of items in the queue
        """
        return len(self._items)

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        """@Override. BoundedQueues have capacity.
        """
        return f"{self.__class__.__name__}({self.capacity})"

    def front(self) -> object:
        return self._items[0]

    def enqueue(self, item) -> None:
        """Adds the given item to the back of the queue.

        Precondition: len(self) < self.capacity
        Postconditions: post-self is pre-self[0], ... , pre-self[len(self)-1],
        item
        """
        self._items[len(self)] = item
        self._size += 1

    def dequeue(self) -> None:
        for position in range(1, len(self)):
            self._items[position-1] = self._items[position]
        del self._items[len(self) - 1]
        self._size -= 1


class ArrayQueue(Queue):
    """A dynamic array implementation of the queue ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty queue
        """
        self._items: _arrays.DynamicArray = _arrays.DynamicArray(16)
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def front(self) -> object:
        return self._items[0]

    def enqueue(self, item) -> None:
        # check if full
        if len(self) == len(self._items):
            self._items.resize(2 * len(self))
        self._items[len(self)] = item
        self._size += 1

    def dequeue(self) -> None:
        # remove the item
        for position in range(1, len(self)):
            self._items[position-1] = self._items[position]
        del self._items[len(self) - 1]
        self._size -= 1
        # is len(self) now a power of 2?
        if len(self) >= 1 and _math.log(len(self), 2).is_integer():
            self._items.resize(len(self)+16)
        elif self.is_empty():
            self._items.resize(16)


class LinkedQueue(Queue):
    """A linked list implementation of the queue ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty queue
        """
        self._items: _LinkedList = _LinkedList()
        self._size: int = 0

    def __len__(self) -> int:
        return len(self._items)

    def front(self) -> object:
        return self._items[0]

    def enqueue(self, item) -> None:
        self._items.insert(len(self), item)

    def dequeue(self) -> None:
        del self._items[0]


class DequeQueue(Queue):
    """A deque implementation of the queue ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty queue
        """
        self._items: _deque = _deque()

    def __len__(self) -> int:
        return len(self._items)

    def front(self) -> object:
        return self._items[len(self)-1]

    def enqueue(self, item) -> None:
        self._items.appendleft(item)

    def dequeue(self) -> None:
        self._items.pop()


class SequenceQueue(Queue):
    """An array sequence implementation of the queue ADT
    """

    def __init__(self) -> None:
        """Initialise an empty queue
        """
        self._items: _ArraySequence = _ArraySequence()
        self._size: int = 0
        self._start: int = 0

    def __len__(self) -> int:
        return self._size

    def front(self) -> object:
        return self._items[self._start]

    def enqueue(self, item) -> None:
        self._items.append(item)
        self._size += 1

    def dequeue(self) -> None:
        self._items[self._start] = None
        self._start += 1
        self._size -= 1


class BoundedCircularQueue(Queue):
    """A circular static array implementation of the queue ADT
    """

    def __init__(self, capacity: int) -> None:
        """Initialise an empty queue
        """
        self._items: _arrays.StaticArray = _arrays.StaticArray(capacity)
        self._size: int = 0
        self._start: int = 0    # Next free position, empty queue
        self._end: int = 0      # Next free position

    def __len__(self) -> int:
        return self._size

    @property
    def capacity(self) -> int:
        """Maximum number of items in the queue
        """
        return len(self._items)

    def front(self) -> object:
        return self._items[self._start]

    def enqueue(self, item) -> None:
        """Adds the given item to the back of the queue.

        Precondition: len(self) < self.capacity
        Postconditions: post-self is pre-self[0], ... , pre-self[len(self)-1],
        item
        """
        self._items[self._end] = item
        self._end = (self._end + 1) % self.capacity
        self._size += 1

    def dequeue(self) -> None:
        self._items[self._end] = None
        self._start = (self._start + 1) % self.capacity
        self._size +- 1
