
"""A collection of implementations of different types of linked lists.
"""

from __future__ import annotations
from typing import Iterator as _Iterator


class LinkedList:
    """An implementation of a doubly linked list.
    """

    def __init__(self):
        """Initialise an empty dequeue.
        """
        self._left: _Node = None
        self._right: _Node = None
        self._size: int = 0

    def _getnode(self, index: int) -> _Node:
        """Private helper method.
        Return the node at a given index.
        """
        current_node: _Node = None

        if index > len(self) / 2 and len(self) >= 3:
            # work right to left
            counter: int = len(self) - 1
            current_node = self._right
            while counter > index:
                current_node = current_node.prev
                counter -= 1
            return current_node
        else:
            # work left to right
            counter: int = 0
            current_node = self._left
            while counter < index:
                current_node = current_node.next
                counter += 1
            return current_node

    def __len__(self) -> int:
        """Returns the length of the array.

        Accessed using the len(self) method.
        """
        return self._size

    def __getitem__(self, index: int) -> object:
        """Return the item stored in the given index.

        Implements the Pythonic-style: self[index].

        Preconditions: 0 <= index <= len(self)-1
        """
        return self._getnode(index).item

    def __setitem__(self, index: int, item: object) -> None:
        """Replace the item at in the given index with the given item.

        Implements the Pythonic-style: self[index] = value.

        Preconditions: 0 <= index <= len(self)-1
        Postconditions: self[index] == item
        """
        self._getnode(index).item = item

    def __delitem__(self, index: int) -> None:
        """Remove the item stored in position index.

        Accessed using the del keyword.
        """
        self.remove(index)

    def __iter__(self) -> _Iterator:
        """Return an iterator for traversing the array.

        Accessed using the iter() method.
        """
        return _LinkedIterator(self._left)

    def __reversed__(self) -> _Iterator:
        """Return an iterator for traversing the array in reverse.

        Accessed using the reversed() method.
        """
        if self._right is not None:
            return _ReversedLinkedIterator(self._right)
        else:
            return _ReversedLinkedIterator(self._left)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        """Return a string representation of the linked list.
        """
        ret_str: str = "["
        current_node: _Node = self._left
        if self._left is not None:
            ret_str += f"{current_node.item}"
            current_node = current_node.next
        while current_node is not None:
            ret_str += f", {current_node.item}"
            current_node = current_node.next
        return ret_str + "]"

    def insert(self, index: int, item: object) -> None:
        """Insert a given item at the given index.
        Items after the index will be shifted to the right.

        This method has constant complexity towards either side of the
        list, and linear complexity towards the middle of the list.
        """

        new_node: _Node = _Node(item)
        if index == 0 or self._left is None:
            if self._left is None:
                self._left = new_node
                self._right = new_node
            else:
                new_node.next = self._left
                self._left.prev = new_node
                self._left = new_node
        elif index >= len(self):
            new_node.prev = self._right
            self._right.next = new_node
            self._right = new_node
        else:
            current_node: _Node = self._getnode(index)
            previous_node: _Node = current_node.prev
            previous_node.next = new_node
            current_node.prev = new_node
            new_node.prev = previous_node
            new_node.next = current_node
        self._size += 1

    def remove(self, index: int) -> None:
        """Remove the item at a given index.

        This method has constant complexity towards either side of the
        list, and grows to linear complexity towards the middle of the
        list.

        Precondition:
        - 0 <= position <= len(self)-1
        """
        if index == 0:
            self._left = self._left.next
        elif index == len(self) - 1:
            previous_node: _Node = self._right.prev
            previous_node.next = None
            # this stops the same node being both the left and right node
            if previous_node is not self._left:
                self._right = previous_node
        else:
            current_node: _Node = self._getnode(index)
            previous_node: _Node = current_node.prev
            next_node: _Node = current_node.next
            # update pointers
            previous_node.next = next_node
            next_node.prev = previous_node
        self._size -= 1


class _Node:
    """A node in a Deque.
    """

    def __init__(self, item: object) -> None:
        """Initialise a node with a reference to the given item.
        """
        self.item: object = item
        self.next: _Node = None
        self.prev: _Node = None


class _LinkedIterator:
    """An iterator for the DoublyLinkedList.
    """

    def __init__(self, left: _Node) -> None:
        """Initialise an iterator for a Deque.
        """
        self.current: _Node = left

    def __iter__(self):
        return self

    def __next__(self) -> object:
        """Return the next item in the sequence

        Implements `next(self)`.

        Raises:
            StopIteration: When there are no more elements to retrieve
            from the set.
        """
        item: object = None
        if self.current is not None:
            item = self.current.item
            self.current = self.current.next
            return item
        else:
            raise StopIteration


class _ReversedLinkedIterator:
    """An iterator for the DoublyLinkedList.
    """

    def __init__(self, right: _Node) -> None:
        """Initialise a reversed iterator for a Deque.
        """
        self.current: _Node = right

    def __iter__(self):
        return self

    def __next__(self):
        item: object = None
        if self.current is not None:
            item = self.current.item
            self.current = self.current.prev
            return item
        else:
            raise StopIteration
