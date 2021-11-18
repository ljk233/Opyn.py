
"""Various implementations of the Sequence ADT.
"""

from __future__ import annotations as _annotations
from typing import Iterator as _Iterator
from . import arrays as _arrays
from . import linkedlists as _linkedlists
from .vectors import Vector, BoundedVector, ArrayVector, LinkedVector
import math as _math


class Sequence(Vector):
    """The sequence ADT as a interface.
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

    def __mul__(self, times: int) -> Sequence:
        """Return the sequence repeated a given number of times.

        Preconditions: times >= 1
        """
        pass

    def append(self, item: object) -> None:
        """Add item to the end of the sequence.

        Postconditions: post-self is the sequence pre-self[0], ... ,
        pre-self[len(self) - 1), item
        """
        self.insert(len(self), item)

    def prepend(self, item: object) -> None:
        """Add the given item to the start of the receiver.
        """
        self.insert(0, item)

    def swap(self, left: int, right: int) -> None:
        """Swap items at positions left and right.
        """
        left_item: object = self[left]
        right_item: object = self[right]
        self[left] = right_item
        self[right] = left_item

    def index(self, item: object) -> int:
        """Return the position of the given item.

        Preconditions: item is a member of self
        Postconditions: self[output] == item
        """
        for count, seq_item in enumerate(self):
            if seq_item == item:
                return count


class BoundedSequence(BoundedVector, Sequence):
    """A sequence with a fixed capacity, as outlined by M269.
    """

    def __init__(self, capacity: int) -> None:
        """Initialise an empty sequence with given capacity.

        Preconditions: capacity >= 0
        """
        super().__init__(capacity)

    def __add__(self, right: BoundedSequence) -> BoundedSequence:
        """@Override.
        Return the concatenated sequence self + right. The returned sequences
        capacity is the receiver's capacity + right's capacity.

        Accessed using the `+` keyword.
        """
        bseq: BoundedSequence = (
            BoundedSequence(self.capacity + right.capacity)
        )
        for item in self:
            bseq.append(item)
        for item in right:
            bseq.append(item)
        return bseq

    def __mul__(self, times: int) -> BoundedSequence:
        new_seq: Sequence = BoundedSequence(self.capacity * times)
        for _ in range(times):
            for item in self:
                new_seq.append(item)
        return new_seq

    def append(self, item: object) -> None:
        """@Override.
        Add item to the end of the sequence.

        Preconditions: len(self) < self.capacity()
        Postconditions: post-self is the sequence pre-self[0], ... ,
        pre-self[len(self) - 1), item
        """
        super().append(item)

    def prepend(self, item: object) -> None:
        """@Override.
        Add item to the end of the sequence.

        Preconditions: len(self) < self.capacity()
        Postconditions: post-self is the sequence pre-self[0], ... ,
        pre-self[len(self) - 1), item
        """
        super().prepend(item)


class ArraySequence(ArrayVector, Sequence):
    """A dynamic array implementation of the sequence ADT.
    """

    def __init__(self):
        """Initialise an empty sequence.
        """
        super().__init__()

    def __add__(self, right: BoundedSequence) -> ArraySequence:
        arr_seq: ArraySequence = ArraySequence()
        for item in self:
            arr_seq.append(item)
        for item in right:
            arr_seq.append(item)
        return arr_seq

    def __mul__(self, times: int) -> ArraySequence:
        new_seq: Sequence = ArraySequence()
        for _ in range(times):
            for item in self:
                new_seq.append(item)
        return new_seq


class LinkedSequence(LinkedVector, Sequence):
    """A linked list implementation of the sequence ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty sequence.
        """
        super().__init__()

    def __add__(self, right: LinkedSequence) -> LinkedSequence:
        linkedseq: LinkedSequence = LinkedSequence()
        for item in self:
            linkedseq.append(item)
        for item in right:
            linkedseq.append(item)
        return linkedseq

    def __mul__(self, times: int) -> LinkedSequence:
        new_seq: LinkedSequence = LinkedSequence()
        for _ in range(times):
            for item in self:
                new_seq.append(item)
        return new_seq
