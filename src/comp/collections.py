
"""Implementations of a select collection of ordered and unordered abstract
data types.
"""

from __future__ import annotations
from typing import Iterator as _Iterator
from typing import Union as _Union
from typing import Hashable as _Hashable
from collections import deque
from . import adt as _adt
from . import arrays as _arrays
from . import linkedlists as _linkedlists
import math as _math
from dataclasses import dataclass


class LinkedStack(_adt.Stack):
    """A linked list implentation of the Stack ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty stack.
        """
        self._items: _linkedlists.LinkedList = _linkedlists.LinkedList()

    def __len__(self) -> int:
        return len(self._items)

    def is_empty(self) -> bool:
        return super().is_empty()

    def peek(self) -> object:
        return self._items[len(self)-1]

    def pop(self) -> None:
        del self._items[len(self)-1]

    def push(self, item: object) -> None:
        self._items.insert(len(self), item)


class ArrayStack(_adt.Stack):
    """A dyanomic array implentation of the Stack ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty stack.
        """
        self._dynarr: _arrays.DynamicArray = _arrays.DynamicArray()
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return super().is_empty()

    def peek(self) -> object:
        return self._dynarr[len(self)-1]

    def pop(self) -> None:
        del self._dynarr[len(self)-1]
        self._size -= 1
        if _arrays.needs_resize(self._dynarr):
            new_capacity: int = _arrays.needs_capacity(self._dynarr)
            self._dynarr.resize(new_capacity)

    def push(self, item: object) -> None:
        if _arrays.needs_resize(self._dynarr):
            new_capacity: int = _arrays.needs_capacity(self._dynarr)
            self._dynarr.resize(new_capacity)
        self._dynarr[len(self)] = item
        self._size +=1
        

class LinkedQueue(_adt.Queue):
    """A linked list implementation of the Queue ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty queue
        """
        self._items: _linkedlists._LinkedList = _linkedlists.LinkedList()

    def __len__(self) -> int:
        return len(self._items)

    def front(self) -> object:
        return self._items[0]

    def enqueue(self, item) -> None:
        self._items.insert(len(self), item)

    def dequeue(self) -> None:
        del self._items[0]


class LinkedDeque(_adt.Deque):
    """A linked list implementation of the Deque ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty deque
        """
        self._items: _linkedlists._LinkedList = _linkedlists._LinkedList()

    def __len__(self) -> int:
        return len(self._items)

    def add_left(self, item: object) -> None:
        self._items.insert_left(item)

    def add_right(self, item: object) -> None:
        self._items.insert_right(item)

    def peek_left(self) -> object:
        assert len(self) > 0, "Cannot peek at an empty deque."
        return self._items[0]

    def peek_right(self) -> object:
        assert len(self) > 0, "Cannot peek at an empty deque."
        return self._items[len(self)-1]

    def remove_left(self) -> object:
        assert len(self) > 0, "Cannot remove from an empty deque."
        self._items.remove_left()

    def remove_right(self) -> object:
        assert len(self) > 0, "Cannot remove from an empty deque."
        self._items.remove_right()

    def __repr__(self) -> str:
        return f"LinkedDeque()"


class LinkedMaxPriorityQueue(_adt.MaxPriorityQueue):
    """A linked list implementation of the Max Priority Queue ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty max priority queue.
        """
        self._items: _linkedlists._LinkedList = _linkedlists._LinkedList()
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        """Return a string representation of the queue.
        """
        items: list = []
        for item in self._items:
            items.append(f"{item[0]} : {item[1]}")
        return str(items)

    def find_min(self) -> object:
        """Return the item with the maximum priority.
        """
        pass

    def insert(self, item: object, priority: int) -> None:
        """Adds the given item with the given priority.
        """
        new_item: list[int, object] = [priority, item]
        position: int = 0
        found: bool = False
        while position <= len(self) - 1 and not found:
            item: list[int, object] = self._items[position]
            if item[0] < priority:
                found = True
            else:
                position += 1        
        self._items.insert(position, new_item)
        self._size += 1

    def remove_min(self) -> None:
        """Remove the item with the maximum priority.
        """
        pass

    def change_priority(self, item, new_priority: int) -> None:
        """Change the given item's priority to the given new_priority.
        Item is inserted at the rear of new priority.
        """
        pass


class Vector:
    """A mutable sequence of items implemented using a Python deque.

    This is an extended version of the Sequence ADT as outlined in M269.
    It differs from M269 by implementing various dunder methods to allow
    for a more Pythonic syntax when using an instance of the class.
    It also uses error checking of the preconditions to allow for more
    meaningful feedack.

    Methods:
        append: Add an item to the end of the vector.
        index: Return the position of the first occurrence of a given item.
        insert: Add an item to the vector at a given position.
        insert_left: Add an item to the start of the vector.
        insert_right: Add an item to the end of the vector.
        remove: Remove item to the vector at a given position.
        remove_left: remove an item from the start of the vector.
        remove_right: remove an item from the end of the vector.
        reverse: Return a vector with items in reverse order.
        swap: Swap two items in place.
    """

    # ==================================================================
    # Representations
    # ==================================================================

    def __str__(self) -> str:
        """Return a string representation of the items of the vector.
        """
        vector: list[object] = []
        for item in self:
            vector.append(item)
        return str(vector)

    def __repr__(self) -> str:
        """Returned a string representation of the collections
        """
        return f"{self.__class__.__name__}()"

    # ==================================================================
    # Inspection
    # ==================================================================

    def __contains__(self, item: object) -> bool:
        """Return True if and only if item is a member of the receiver.

        Accessed using the `in` operator.
        """
        for vector_item in self:
            if vector_item == item:
                return True
        return False

    def __getitem__(self, position: int) -> object:
        """Return the item at the given position.

        Implements Pythonic-style: self[index].

        Preconditions: 0 <= index <= len(self) - 1
        Postconditions: the output is the n-th item of self
        """
        return self._items[position]

    def index(self, item: object) -> int:
        """Return the position of the first occurrence of a given item.

        Precondition: item is member of vector.
        Postcondtions: self[output] = item
        """
        for position, vector_item in enumerate(self):
            if vector_item == item:
                return position

    def __iter__(self) -> _Iterator:
        """Initialises and return an iterator that can be used to iterate
        over the vector.
        """
        pass

    def __len__(self) -> int:
        """Return the number of items in the vector.

        Accessed using the len() function.

        Postconditions: 0 <= len(self)
        """
        pass

    # ==================================================================
    # Modification
    # ==================================================================

    def __delitem__(self, position: int) -> None:
        """Remove item at the given position.

        Preconditions: 0 <= position < self.length()
        Postconditions: post-self is the sequence pre-self[0], ... ,
        pre-self[index - 1], pre-self[index + 1], ... ,
        pre-self[len(pre-self) - 1)]
        """
        self.remove(position)

    def insert(self, position: int, item: object) -> None:
        """Add an item to the vector at a given position.
        """
        pass

    def insert_left(self, item: object) -> None:
        """Add an item to the start of the vector.
        """
        self.insert(0, item)

    def insert_right(self, item: object) -> None:
        """Add an item to the end of the vector.
        """
        self.insert(len(self), item)

    def remove(self, position: int) -> None:
        """Remove item to the vector at a given position.
        """
        pass

    def remove_left(self) -> None:
        """Remove an item from the start of the vector.
        """
        self.remove(0)

    def remove_right(self) -> None:
        """Remove an item from the end of the vector.
        """
        self.remove(len(self) - 1)

    def reverse(self) -> Vector:
        """Return a vector with items in reverse order.
        """
        rev_vector: list[object] = []
        for position in range(len(self)-1, -1, -1):
            rev_vector.append(self[position])
        return rev_vector

    def __setitem__(self, index: int, item: object) -> None:
        """Replace the item at the given position given item.

        Implements Pythonic-style: `self[key] = value`.

        Preconditions: 0 <= index <= len(self) - 1
        Postconditions: post-self[index] == item
        """
        self._items[index] = item

    def swap(self, left: int, right: int) -> None:
        """Swap two items at positions left and right in place.
        """
        left_item: object = self[left]
        self[left] = self[right]
        self[right] = left_item

    # ==================================================================
    # Creation
    # ==================================================================


class MaxPriorityQueue:
    """An implementation of a max priority queue using a Python dictionary.

    Items with the same priority are ordered by FIFO.

    The "queues" are represented using Python dequeues. These have constant
    complexity for both inserting and removing items from the queues.

    Methods:
        insert: Add the given item at the given priority.
        is_empty: Return true if the queue is empty.
        find_max: Return the highest-priority item.
        remove_max: Remove the highest-priority item.
        increment_votes: Increment the candidates priority by 1.
    """

    def __init__(self) -> None:
        """Initialise an empty priority queue with given number of
        priorities.
        """
        self._items: dict[int, deque] = {}

    def __len__(self) -> int:
        """Return the number of items in the queue.
        """
        size: int = 0
        for items in self._items.values():
            size += len(items)
        return size

    def __str__(self) -> str:
        """
        """
        ret_str: str = ""
        for priority, items in self._items.items():
            str_items: str = ""
            for item in items:
                if len(str_items) == 0:
                    str_items += item
                else:
                    str_items += f", {item}"
            ret_str += f"{priority}: {str_items}\n"
        return ret_str

    def insert(self, item: object, priority: int) -> None:
        """Add the given item at the given priority.

        Preconditions:
        - 1 <= priority <= priorities
        """
        if priority in self._items:
            self._items[priority].append(item)
        else:
             self._items[priority] = deque([item])

    def is_empty(self) -> bool:
        """Return true if the queue is empty.
        """
        return len(self) == 0

    def find_max(self) -> object:
        """Return the highest-priority item.

        Preconditions: len(self) >= 1
        """
        max_priority = max(self._items.keys())
        return self._items[max_priority]

    def remove_max(self) -> object:
        """Remove the highest-priority item.

        Preconditions: len(self) >= 1
        """
        found: bool = False
        priority: int = 1
        while not found and priority <= len(self._items):
            if len(self._items[priority]) >= 1:
                self._items[priority].popleft()
                found = True
            else:
                priority += 1
        return None

    def change_priority(self, item: object, old_priority: int, new_priority: int) -> None:
        """Change the given item's priority to the given new priority.
        """
        # remove the item from the old priority
        self._items[old_priority].remove(item)

        # add the item to the new priority
        self.insert(item, new_priority)

    def find_priority(self, item: object) -> int:
        for priority, items in self._items.items():
            if item in items:
                return priority


class ArraySet(_adt.Set):
    """An implementation of the Set ADT using a dynamic array as its
    underlying data structure.
    """

    def __init__(self) -> None:
        self._elements: _arrays.DynamicArray = _arrays.DynamicArray()
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __contains__(self, element: object) -> bool:
        for set_element in self:
            if set_element == element:
                return True
        return False

    def __iter__(self) -> _Iterator:
        return _ArraySetIterator(self)

    def add(self, element: object) -> None:
        if element not in self:
            if _arrays.needs_resize(self._elements):
                new_capacity: int = _arrays.needs_capacity(self._elements)
                self._elements.resize(new_capacity)
            self._elements[len(self)] = element
            self._size +=1

    def remove(self, element: object) -> None:
        # find address in the array
        self._elements.shift(self._elements.index(element)+1, len(self)-1, -1)
        if _arrays.needs_resize(self._elements):
            new_capacity: int = _arrays.needs_capacity(self._elements)
            self._elements.resize(new_capacity)
        self._size -= 1

    def __eq__(self, right: ArraySet) -> bool:
        if len(self) != len(right):
            return False
        else:
            for element in self:
                if element not in right:
                    return False
        return True

    def __lt__(self, right: ArraySet) -> bool:
        if len(self) >= len(right):
            return False
        else:
            for element in self:
                if element not in right:
                    return False
        return True

    def __gt__(self, right: ArraySet) -> bool:
        if len(self) <= len(right):
            return False
        return right < self

    def __le__(self, right: ArraySet) -> bool:
        return (self == right) or (self < right)

    def __ge__(self, right: ArraySet) -> bool:
        return (self == right) or (self > right)

    def __add__(self, right: ArraySet) -> ArraySet:
        union: ArraySet = ArraySet()
        for element in self:
            union.add(element)
        for element in right:
            union.add(element)
        return union

    def __mul__(self, right: ArraySet) -> ArraySet:
        intersection: ArraySet = ArraySet()
        if len(self) <= len(right):
            for element in self:
                if element in right:
                    intersection.add(element)
        else:
            for element in right:
                if element in self:
                    intersection.add(element)
        return intersection

    def __sub__(self, right: ArraySet) -> ArraySet:
        pass

    def __str__(self) -> str:
        str_set: str = "{"
        if not self.is_empty():
            counter: int = 1
            str_set += f"{self._elements[0]}"
            while counter < len(self):
                str_set += f", {self._elements[counter]}"
                counter += 1
        return str_set + "}"

    def __repr__(self) -> str:
        return "ArraySet()"        

    def __or__(self, right: ArraySet) -> ArraySet:
        """Return the union of this set and right set.

        Accessed using the | opertator.
        """
        return self + right


class _ArraySetIterator:
    """An iterator for an ArraySet.
    """

    def __init__(self, arrset):
        self.items = arrset
        self.current: int = 0

    def __iter__(self):
        """Implements iter(self).
        """
        return self

    def __next__(self) -> object:
        """Return the next item in the set.

        Implements `next(self)`.

        Raises:
            StopIteration: When there are no more elements to retrieve
            from the set.
        """
        item: object = None
        if self.current <= len(self.items)-1:
            item = self.items._elements[self.current]
            self.current += 1
            return item
        else:
            raise StopIteration


@dataclass
class _MapEntry:
    """Storage class for holding the key/value pairs
    """
    key: int
    value: object


_UNUSED = None
_EMPTY: _MapEntry = _MapEntry(None, None)


class ArrayHashMap(_adt.Map):
    """A dynamic array implementation of the HashMap ADT.
    """

    def __init__(self) -> None:
        """Initialise an empty hash map with 7 slots.
        """
        self._table: list[_MapEntry] = [None] * 7
        self._size: int = 0
        self._max_size: int = len(self._table) - len(self._table) // 3

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: _Hashable) -> bool:
        return self._search(key) is not None

    def __iter__(self) -> _Iterator:
        """Return an iterator object that can be used to traverse the map.
        """
        return _MapIterator(self._table)

    def __setitem__(self, key: _Hashable, value: object) -> bool:
        if key in self:
            self._table[self._search(key)].value = value
            return False
        else:
            slot = self._insertion_search(key)
            self._table[slot] = _MapEntry(key, value)
            self._size += 1
            if len(self) == self._max_size:
                self._rehash()
            return True

    def __getitem__(self, key: _Hashable) -> object:
        assert key in self, f"{key} is an invalid map key"
        return self._table[self._search(key)].value

    def __delitem__(self, key: _Hashable) -> None:
        assert key in self, f"{key} is an invalid map key"
        self._table[self._search(key)] = _EMPTY
        self._size -= 1

    def _search(self, key: _Hashable) -> int:
        """Return the slot containing the given key.
        """
        # compute home slot and the step size
        slot: int = self._key_hash(key)
        step: int = self._probe_hash(key)

        # probe for the key
        tbl_len: int = len(self._table)
        while self._table[slot] is not _UNUSED:
            if self._table[slot] is not _EMPTY and self._table[slot].key == key:
                return slot
            else:
                slot = (slot + step) % tbl_len

    def _insertion_search(self, key: _Hashable) -> int:
        """Return the first valid unused slot for insertion into the map.
        """
        # compute home slot and the step size
        slot: int = self._key_hash(key)
        step: int = self._probe_hash(key)

        # probe for the key
        tbl_len: int = len(self._table)
        while self._table[slot] is not _EMPTY and self._table[slot] is not _UNUSED:
            slot = (slot + step) % tbl_len
        return slot

    def _rehash(self) -> None:
        """Rebuilds the hash table, extending 
        """
        # create a larger table
        original_table: list[_MapEntry] = self._table
        new_max_size: int = (len(self._table) * 2) + 1
        self._table = [None] * new_max_size

        # modify the map attributes
        self._size = 0
        self._max_size = new_max_size

        # Populate the new table with entries from the original table
        for entry in original_table:
            if (entry is not _UNUSED) and (entry is not _EMPTY):
                self._table[self._insertion_search(entry.key)] = entry
                self._size += 1

    def _key_hash(self, key: _Hashable) -> int:
        """Return the hash of the given key.
        """
        return abs(hash(key)) % len(self._table)

    def _probe_hash(self, key: _Hashable) -> int:
        """Return the step size to be used when searching for thegiven
        key.
        """
        return 1 + abs(hash(key)) % (len(self._table) - 2)

    def __repr__(self) -> str:
        return f"ArrayHashMap({len(self)})"

    def __str__(self) -> str:
        adict = {}
        for entry in self:
            adict[entry] = self[entry]
        return str(adict)


class _MapIterator:
    """Iterator object for traversing a map.
    """

    def __init__(self, hashtable: list[_MapEntry]):
        self.hashtable: list[_MapEntry] = hashtable
        self.current: int = 0

    def __iter__(self):
        return self

    def __next__(self):
        key: object = None

        while self.current < len(self.hashtable):
            entry: _MapEntry = self.hashtable[self.current]
            if entry is not None and entry.key is not None:
                key: object = entry.key
                self.current += 1
                return key
            else:
                self.current += 1

        if key is not None:
            return key
        else:
            raise StopIteration


class ArrayHashSet(ArraySet):
    """Implementation of the Set ADT as a ArrayHashMap.
    """

    def __init__(self) -> None:
        """Initialise an empy set.
        """
        self._elements: ArrayHashMap = ArrayHashMap()

    def __len__(self) -> int:
        return len(self._elements)

    def __contains__(self, element: object) -> bool:
        return element in self._elements

    def __iter__(self) -> _Iterator:
        return iter(self._elements)

    def add(self, element: object) -> None:
        self._elements[element] = True

    def remove(self, element: object) -> None:
        del self._elements[element]

    def __str__(self) -> str:
        str_set: str = "{"
        for elem in self._elements:
            if len(str_set) == 1:
                str_set += f"{elem}"
            else:
                str_set += f", {elem}"
        return str_set +"}"

    def __repr__(self) -> str:
        return "ArraySet()"        

    def __eq__(self, right: ArraySet) -> bool:
        if len(self) != len(right):
            return False
        else:
            for element in self:
                if element not in right:
                    return False
        return True

    def __lt__(self, right: ArraySet) -> bool:
        if len(self) >= len(right):
            return False
        else:
            for element in self:
                if element not in right:
                    return False
        return True

    def __gt__(self, right: ArraySet) -> bool:
        if len(self) <= len(right):
            return False
        return right < self

    def __le__(self, right: ArraySet) -> bool:
        return (self == right) or (self < right)

    def __ge__(self, right: ArraySet) -> bool:
        return (self == right) or (self > right)

    def __add__(self, right: ArrayHashMap) -> ArrayHashSet:
        union: ArrayHashSet = ArrayHashSet()
        for element in self:
            union.add(element)
        for element in right:
            union.add(element)
        return union

    def __mul__(self, right: ArrayHashSet) -> ArrayHashSet:
        intersection: ArrayHashSet = ArrayHashSet()
        if len(self) <= len(right):
            for element in self:
                if element in right:
                    intersection.add(element)
        else:
            for element in right:
                if element in self:
                    intersection.add(element)
        return intersection

    def __sub__(self, right: ArrayHashSet) -> ArrayHashSet:
        pass
