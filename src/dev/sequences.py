
"""A modified version of m269_sequences.py.
"""

# %%
from __future__ import annotations as _annotations
from typing import Iterator as _Iterator
from . import arrays as _arrays
from . import linkedlists as _linkedlists
from . import _iterators
import math as _math


class Sequence:
    """The sequence ADT as a interface.

    This differs from M269's implementation of the interface:
    - Dunder methods have been added, to allow for a more Pythonic use.
    - __iter__ method added to allow for Pythonic iteration.
    - __add__ method aded to allow for concatenation (left + right)
    - Methods have been removed that implement the same behaviour as an
    equivalent dunder method.
    """

    def __add__(self, right: Sequence) -> Sequence:
        """Return the concatenated sequence self + right.

        Accessed using the `+` keyword.

        Postcondition:
        - output is self[0], ... , self[len(self)-1], right[0], ... ,
        right[len(right)-1]
        - len(output) == len(self) + len(right)
        - output.capacity() = self.capacity() + right.capacity()
        """
        pass

    def __contains__(self, item: object) -> bool:
        """Return True if and only if item is a member of self.

        Implements the membership function. (See Exercise 6.3.1.)
        Accessed using the `in` operator.
        """
        for seq_item in self:
            if seq_item == item:
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

        Preconditions: 0 <= index < len(self)
        Postconditions: the output is the n-th item of self, with n =
        index + 1
        """
        return self._items[index]

    def __iter__(self) -> _Iterator:
        """Initialises and returns an iterator that can be used to iterate
        over the sequence.

        Precondition: len(self) >= 1
        """
        pass

    def __len__(self) -> int:
        """Return the number of items in the sequence.

        Accessed using the len() function.

        Postconditions: 0 <= len(self) <= self.capacity()
        """
        return self._size

    def __mul__(self, times: int) -> Sequence:
        """Return the sequence repeated a given number of times.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __setitem__(self, index: int, item: object) -> None:
        """Replace the item at position index with the given one.

        Implements Pythonic-style: `self[key] = value`.

        Preconditions: 0 <= index < len(self)
        Postconditions: post-self[index] == item
        """
        self._items[index] = item

    def __str__(self) -> str:
        """Return a string representation of the sequence.

        Postconditions: the output uses Python's syntax for lists
        """
        items = []
        for index in range(len(self)):
            items.append(self[index])
        return str(items)

    def append(self, item: object) -> None:
        """Add item to the end of the sequence.

        Preconditions: len(self) < self.capacity()
        Postconditions: post-self is the sequence pre-self[0], ... ,
        pre-self[len(self) - 1), item
        """
        self.insert(len(self), item)

    def insert(self, index: int, item: object) -> None:
        """Insert item at position index.

        Preconditions: 0 <= index <= len(self) < self.capacity()
        Postconditions: post-self is the sequence pre-self[0],
        ... , pre-self[index - 1], item, pre-self[index],
        ... , pre-self[len(pre-self) - 1]
        """
        pass


class BoundedSequence(Sequence):
    """A sequence with a fixed capacity, as outlined by M269.
    """

    def __init__(self, capacity: int) -> None:
        """Create an empty sequence that can hold a given capacity items.

        Preconditions: capacity >= 0
        """
        self._items: _arrays.StaticArray = _arrays.StaticArray(capacity)
        self._capacity: int = capacity
        self._size: int = 0

    @property
    def capacity(self) -> int:
        """Return the capacity of the sequence.
        """
        return len(self._items)

    def __add__(self, right: BoundedSequence) -> BoundedSequence:
        """@Override.
        Return the concatenated sequence self + right. The returned sequences
        capacity is the receiver's capacity + right's capacity.

        Accessed using the `+` keyword.
        """
        bseq: BoundedSequence = (
            BoundedSequence(self.capacity() + right.capacity())
        )
        for item in self:
            bseq.append(item)
        for item in right:
            bseq.append(item)
        return bseq

    def __delitem__(self, index: int) -> None:
        for position in range(index + 1, len(self)):
            self[position - 1] = self[position]
        del self._items[len(self) - 1]
        self._size -= 1

    def __iter__(self) -> _Iterator:
        return _iterators.ArrayIterator(self)

    def __mul__(self, times: int) -> BoundedSequence:
        new_seq: Sequence = BoundedSequence(len(self._items * times))
        num: int = 0
        while num < times:
            new_seq = new_seq + self
            num += 1
        return new_seq

    def insert(self, index: int, item: object) -> None:
        for position in range(len(self) - 1, index - 1, -1):
            self[position + 1] = self[position]
        self[index] = item
        self._size += 1


class ArraySequence(Sequence):
    """A dynamic array implementation of the sequence ADT.
    """

    def __init__(self):
        """Create an empty sequence.
        """
        self._items: _arrays.DynamicArray = _arrays.DynamicArray(16)
        self._size = 0

    def __add__(self, right: BoundedSequence) -> ArraySequence:
        arr_seq: ArraySequence = ArraySequence
        for item in self:
            arr_seq.append(item)
        for item in right:
            arr_seq.append(item)
        return arr_seq

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
        from ._iterators import ArrayIterator
        return ArrayIterator(self)

    def __mul__(self, times: int) -> ArraySequence:
        new_seq: Sequence = ArraySequence()
        num: int = 0
        while num < times:
            new_seq = new_seq + self
            num += 1
        return new_seq

    def insert(self, index: int, item: object) -> None:
        if len(self) == len(self._items):
            self._items.resize(2 * len(self))
        for position in range(len(self) - 1, index - 1, -1):
            self[position + 1] = self[position]
        self[index] = item
        self._size += 1


class LinkedSequence(Sequence):
    """A linked list implementation of the sequence ADT.
    """

    class _Node:
        """A node in a linked list.
        """

        def __init__(self, item: object) -> None:
            """Initialise the node with the given item.
            """
            self.item: object = item
            self.next: LinkedSequence._Node = None

    def __init__(self) -> None:
        """Initialise the sequence to be empty.
        """
        self._items: _linkedlists.LinkedList = _linkedlists.LinkedList()
        self._size: int = 0

    def __add__(self, right: LinkedSequence) -> LinkedSequence:
        linkedseq: LinkedSequence = LinkedSequence()
        for item in self:
            linkedseq.append(item)
        for item in right:
            linkedseq.append(item)
        return linkedseq

    def __delitem__(self, index: int) -> None:
        del self._items[index]

    def __getitem__(self, index: int) -> object:
        return self._getnode(index).item

    def __iter__(self) -> _Iterator:
        """Return an iterator object for the linked sequence.
        """
        from ._iterators import LinkedListIterator
        return LinkedListIterator(self[0])

    def __mul__(self, times: int) -> LinkedSequence:
        new_seq: LinkedSequence = LinkedSequence()
        num: int = 0
        while num < times:
            new_seq = new_seq + self
            num += 1
        return new_seq

    def insert(self, index: int, item: object) -> None:
        self._items.insert(index, item)
