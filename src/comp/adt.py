
"""A module of abstract classes representing various abstract data types.
"""

from __future__ import annotations
from typing import Iterator as _Iterator


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


class Deque:
    """A dequeue is a ...
    """

    def __len__(self) -> int:
        """Return the number of element in the deque.
        """
        pass

    def is_empty(self) -> bool:
        """Return if the deque is empty or not.
        """
        return len(self) == 0

    def add_left(self, item: object) -> None:
        """Add an item to the left of the deque.
        """
        pass

    def add_right(self, item: object) -> None:
        """Add an item to the right of the deque.
        """
        pass

    def peek_left(self) -> object:
        """Return the item on the left of the deque.

        Preconditions: len(self) >= 1
        """
        pass

    def peek_right(self) -> object:
        """Return the item on the left of the deque.

        Preconditions: len(self) >= 1
        """
        pass

    def remove_left(self) -> object:
        """Return the item from the left of the deque.

        Preconditions: len(self) >= 1
        """
        pass

    def remove_right(self) -> object:
        """Return the item from the right of the deque.

        Preconditions: len(self) >= 1
        """
        pass

    def __repr__(self) -> str:
        """Return a string representation of the object.
        """
        return f"Deque({self})"

    def __str__(self) -> str:
        """Return a string representation of the items in the dequeue.
        """
        items: list = []
        count: int = 0
        while count < len(self):
            item = self.peek_left()
            items.append(item)
            self.remove_left()
            self.add_right(item)
            count += 1
        return str(items)


class MaxPriorityQueue:
    """
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
        pass

    def is_empty(self) -> bool:
        """Return if the queue is empty.

        Postcondtions: output is true if len(self) == 0
        """
        return len(self) == 0

    def find_min(self) -> object:
        """Return the item with the maximum priority.
        """
        pass

    def insert(self, item: object, priority: int) -> None:
        """Adds the given item with the given priority.
        """
        pass

    def remove_min(self) -> None:
        """Remove the item with the maximum priority.
        """
        pass

    def change_priority(self, item, new_priority: int) -> None:
        """Change the given item's priority to the given new_priority.
        Item is inserted at the rear of new priority.
        """
        pass


class MaxPriorityQueue:
    """
    """
    ...


class Set:
    """A set is a container that stores a collection of unique values
    over a given comparable domain in which the stored values have no
    particular ordering.
    """

    def __len__(self) -> int:
        """Return the number of elements in the set.

        Postconditions:
        - len(self) >= 0.
        """
        pass

    def __contains__(self, element: object) -> bool:
        """Check if the given element is an element ofs the set.

        Postconditions:
        - output is true if element ∈ self.
        """
        pass

    def __iter__(self) -> _Iterator:
        """Return an object that can be used to iterate of the elements
        of the set.
        """
        pass

    def is_empty(self) -> bool:
        """Return if the set represents the empty set.
        """
        return len(self) == 0

    def add(self, element: object) -> None:
        """Add the given element to the set.

        Postconditions:
        - if element is not member of pre-self, then element is member of
        post-self, other pre-self == post-self
        """
        pass

    def remove(self, element: object) -> None:
        """Remove the given element from the set.

        Preconditions: element is member of self
        """
        pass

    def __eq__(self, right: Set) -> bool:
        """Return if the receiver and the given set represent are equal.
        """
        pass

    def __lt__(self, right: Set) -> bool:
        """Return if the receiver is a strict subset of the given right
        set.
        """
        pass

    def __le__(self, right: Set) -> bool:
        """Return if the receiver is equal to or a subset of the given
        right set.
        """
        pass

    def __gt__(self, right: Set) -> bool:
        """Return if the receiver is a strict superset of the given right
        set.
        """
        pass

    def __ge__(self, right: Set) -> bool:
        """Return if the receiver is equal to or a superset of the given
        right set.
        """
        pass

    def __add__(self, right: Set) -> Set:
        """Return a new set that represents the union of the receiver set
        and right.
        """
        pass

    def __mul__(self, right: Set) -> Set:
        """Return a new set that represents the intersection of the receiver
        set and right.
        """
        pass

    def __sub__(self, right: Set) -> Set:
        """Return a new set that represents the difference of the receiver
        set and right.
        """
        pass

    def __str__(self) -> str:
        """Return a string representation of the set.
        """
        str_set: str = "{"
        if not self.is_empty():
            for counter, element in enumerate(self):
                if counter == 0:
                    str_set += f"{self._elements[counter]}"
                else:
                    str_set += f", {self._elements[counter]}"
        return str_set + "}"

    def __repr__(self) -> str:
        """Return a string representation of the object.
        """
        return "Set()"


class Map:
    """A map is a container for storing a collection of data records in
    which each record is associated with a unique key.
    The key components must be comparable.
    """

    def __len__(self) -> int:
        """Return the number of entries in the map.

        Postconditions:
        - len(self) >= 0.
        """
        pass

    def __contains__(self, key) -> bool:
        """Check if the given key is in the map.

        Postconditions:
        - output is true if key is a member of keys, where keys
        is the set of all keys of self.
        """
        pass

    def __getitem__(self, key) -> object:
        """Return the value associated with the given key.

        Preconditions:
        - key is a member of the set of all self's keys.
        Postcondtions:
        - self[key] = output.
        """
        pass

    def __setitem__(self, key, value) -> None:
        """Associate the given value with the given key.

        If key is already associated with a value, then that value is
        overwritten.

        Postcondtions:
        - self[key] = value
        """
        pass

    def __delitem__(self, key) -> None:
        """Remove the given key from the map.

        Preconditions:
        - key is a member of the set of all self's keys.
        Postconditions:
        - key is not a member of the set of all self's keys.
        """
        pass

    def __eq__(self, right: Map) -> bool:
        """Determine if self represents the same map as right.

        Postconditions:
        - output is True if self = right.
        """
        pass

    def keys(self) -> Set:
        """Return all keys in the map.
        """
        pass

    def values(self) -> list[list[object]]:
        """Return all values in the map.
        """
        pass
