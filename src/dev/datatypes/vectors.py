
"""Various implementations of the vector ADT.
The inteface is based of that described in
http://www.math.bas.bg/~nkirov/2017/NETB201/slides/ch05/ch05.html
"""


from __future__ import annotations as _annotations
from typing import Iterator as _Iterator
from . import arrays as _arrays
from . import linkedlists as _linkedlists
from . import _iterators
import math as _math


class Vector:
    """The Vector ADT as an abstract class.
    """

    def __contains__(self, item: object) -> bool:
        """Return True if and only if item is a member of the receiver.

        Accessed using the `in` operator.
        """
        for vector_item in self:
            if vector_item == item:
                return True
        return False

    def __delitem__(self, index: int) -> None:
        """Remove item at position index.

        See Exercise 6.3.2.

        Preconditions: 0 <= index < self.length()
        Postconditions: post-self is the sequence pre-self[0], ... ,
        pre-self[index - 1], pre-self[index + 1], ... ,
        pre-self[len(pre-self) - 1)]
        """
        pass

    def __getitem__(self, index: int) -> object:
        """Return the item at position index.

        Implements Pythonic-style: self[index].

        Preconditions: 0 <= index <= len(self) - 1
        Postconditions: the output is the n-th item of self
        """
        return self._items[index]

    def __iter__(self) -> _Iterator:
        """Initialises and returns an iterator that can be used to iterate
        over the vector.

        Precondition: len(self) >= 1
        """
        pass

    def __len__(self) -> int:
        """Return the number of items in the vector.

        Accessed using the len() function.

        Postconditions: 0 <= len(self)
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __setitem__(self, index: int, item: object) -> None:
        """Replace the item at position index with the given one.

        Implements Pythonic-style: `self[key] = value`.

        Preconditions: 0 <= index <= len(self) - 1
        Postconditions: post-self[index] == item
        """
        self._items[index] = item

    def __str__(self) -> str:
        """Return a string representation of the sequence.

        Postconditions: the output uses Python's syntax for lists
        """
        items: list[object] = []
        for item in self:
            items.append(item)
        return str(items)

    def insert(self, index: int, item: object) -> None:
        """Insert item at position index.

        Preconditions: 0 <= index <= len(self)
        Postconditions: post-self is the sequence pre-self[0],
        ... , pre-self[index - 1], item, pre-self[index],
        ... , pre-self[len(pre-self) - 1]
        """
        pass


class BoundedVector(Vector):
    """A vector with a fixed capacity.
    """

    def __init__(self, capacity: int) -> None:
        """Initialise an empty vector with given capacity.

        Preconditions: capacity >= 0
        """
        self._items: _arrays.StaticArray = _arrays.StaticArray(capacity)
        self._size: int = 0

    @property
    def capacity(self) -> int:
        """Return the capacity of the vector.
        """
        return len(self._items)

    def __delitem__(self, index: int) -> None:
        for position in range(index + 1, len(self)):
            self[position - 1] = self[position]
        del self._items[len(self) - 1]
        self._size -= 1

    def __iter__(self) -> _Iterator:
        return _iterators.ArrayIterator(self)

    def __len__(self) -> int:
        """Return the number of items in the vector.

        Accessed using the len() function.

        Postconditions: 0 <= len(self)
        """
        return self._size

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.capacity})"

    def insert(self, index: int, item: object) -> None:
        """Insert item at position index.

        Preconditions: 0 <= index <= len(self) < self.capacity
        Postconditions: post-self is the sequence pre-self[0],
        ... , pre-self[index - 1], item, pre-self[index],
        ... , pre-self[len(pre-self) - 1]
        """
        for position in range(len(self) - 1, index - 1, -1):
            self[position + 1] = self[position]
        self[index] = item
        self._size += 1


class ArrayVector(Vector):
    """A dynamic array implementation of the vector ADT.
    """

    def __init__(self):
        """Initialise an empty vector.
        """
        self._items: _arrays.DynamicArray = _arrays.DynamicArray(16)
        self._size = 0

    def __delitem__(self, index: int) -> None:
        for position in range(index + 1, len(self)):
            self[position - 1] = self[position]
        del self._items[len(self) - 1]
        self._size -= 1
        # is len(self) now a power of 2?
        if len(self) >= 1 and _math.log(len(self), 2).is_integer():
            self._items.resize(len(self)+16)
        elif len(self) == 0:
            self._items.resize(16)

    def __iter__(self) -> _Iterator:
        return _iterators.ArrayIterator(self)

    def __len__(self) -> int:
        """Return the number of items in the vector.

        Accessed using the len() function.

        Postconditions: 0 <= len(self)
        """
        return self._size

    def insert(self, index: int, item: object) -> None:
        if len(self) == len(self._items):
            self._items.resize(2 * len(self))
        for position in range(len(self) - 1, index - 1, -1):
            self[position + 1] = self[position]
        self[index] = item
        self._size += 1


class LinkedVector(Vector):
    """A linked list implementation of the sequence ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty vector.
        """
        self._items: _linkedlists.LinkedList = _linkedlists.LinkedList()
        self._size: int = 0

    def __delitem__(self, index: int) -> None:
        del self._items[index]
        self._size -= 1

    def __iter__(self) -> _Iterator:
        """Return an iterator object for the linked sequence.
        """
        return _iterators.LinkedListIterator(self._items.head)

    def __len__(self) -> int:
        """Return the number of items in the vector.

        Accessed using the len() function.

        Postconditions: 0 <= len(self)
        """
        return self._size

    def insert(self, index: int, item: object) -> None:
        self._items.insert(index, item)
        self._size += 1
