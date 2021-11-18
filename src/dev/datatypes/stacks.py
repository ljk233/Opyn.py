
"""Various implementations of the Stack ADT, as defined by M269.
"""

from .arrays import StaticArray, DynamicArray
from collections import deque
import math


class Stack:
    """A stack is a data structure that stores a linear collection of
    items with access limited to a last-in first-out order.

    Adding and removing items is restricted to one end known as the top
    of the stack.

    An empty stack is one containing no items.
    """

    def __len__(self) -> int:
        """Return the number of items in the stack.

        Postconditions: 0 <= len(self)
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __str__(self) -> str:
        """Return a string representation of the stack.
        """
        items = []
        for index in range(len(self)):
            items.append(self._items[index])
        return str(items)

    def is_empty(self) -> bool:
        """Return true if the stack is empty, otherwise false.
        """
        return len(self) == 0

    def pop(self) -> None:
        """Remove the top item of the stack.

        Preconditions: len(self) > 0
        Postconditions: post-self == pre-self[0], ... ,
        pre-self[len(self) - 2)
        """
        pass

    def peek(self) -> object:
        """Return the item on top of the stack.
        The stack is not modified by this operation.

        Preconditions: len(self) > 0
        """
        pass

    def push(self, item: object) -> None:
        """Push item to the top of the stack.

        Postconditions: post-self.peek() == item
        """
        pass


class BoundedStack(Stack):
    """A stack with a fixed capacity, as outlined by M269.
    """

    def __init__(self, capacity: int) -> None:
        """Initialise an empty stack with given capacity.

        Preconditions: capacity >= 0
        """
        self._items: StaticArray = StaticArray(capacity)
        self._size: int = 0

    @property
    def capacity(self) -> int:
        """Return how many items the sequence can hold.
        """
        return len(self._items)

    def __len__(self) -> int:
        return self._size

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.capacity})"

    def peek(self) -> object:
        return self._items[len(self) - 1]

    def pop(self) -> None:
        del self._items[len(self) - 1]
        self._size -= 1

    def push(self, item: object) -> None:
        self._items[len(self)] = item
        self._size += 1


class ArrayStack(Stack):
    """A dynamic array implementation of the stack ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty stack
        """

        self._items: DynamicArray = DynamicArray(1)
        self._size: int = 0   

    def __len__(self) -> int:
        return self._size

    def peek(self) -> object:
        return self._items[len(self) - 1]

    def pop(self) -> None:
        del self._items[len(self) - 1]
        # is len(self) now a power of 2?
        if len(self) >= 1 and math.log(len(self), 2).is_integer():
            self._items.resize(len(self))
        self._size -= 1

    def push(self, item: object) -> None:
        if len(self) == len(self._items):
            self._items.resize(2 * len(self))
        self._items[len(self)] = item
        self._size += 1


class LinkedStack(Stack):
    """A linked list implementation of the stack ADT.
    """

    class _Node:
        """A node in a linked list.
        """

        def __init__(self, item: object) -> None:
            """Initialise the node with the given item.
            """
            self.item: object = item
            self.next: LinkedStack._Node = None

    def __init__(self) -> None:
        """Initialised an empty stack.
        """
        self._head: LinkedStack._Node = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        items = []
        current: LinkedStack._Node = self._head
        while current is not None:
            items.insert(0, current.item)
            current = current.next
        return str(items)

    def peek(self) -> object:
        return self._head.item

    def pop(self) -> None:
        self._head = self._head.next
        self._size -= 1

    def push(self, item: object) -> None:
        new_node: LinkedStack._Node = LinkedStack._Node(item)
        new_node.next = self._head
        self._head = new_node
        self._size += 1


class DequeStack(Stack):
    """A deque implementation of the stack ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty stack.
        """
        self._items: deque = deque()
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def peek(self) -> object:
        return self._items[len(self)-1]

    def pop(self) -> None:
        self._size -= 1
        self._items.pop()

    def push(self, item: object) -> None:
        self._size += 1
        self._items.append(item)
