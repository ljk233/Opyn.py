
"""An implementation of various array types.
"""


from __future__ import annotations
from dataclasses import dataclass as _dataclass
from typing import Iterator as _Iterator
from typing import Hashable as _Hashable
from .adt import Map, Set
import math as _math


def needs_resize(arr: DynamicArray) -> bool:
    """Return whether a resize is needed.
    """
    if arr._effective_size == 0:
        return True
    if (_math.log(arr._effective_size, 2).is_integer()
         or arr.fill >= 1
         or arr.fill == 0.0):
        return True
    else:
        return False


def needs_capacity(arr: DynamicArray) -> int:
    """Return the suggested capacity to use when resizing an array.
    """
    if arr.fill >= 1:
        return len(arr) * 2
    elif arr.fill == 0.0:
        return 1
    elif _math.log(arr._effective_size, 2):
        # print(2 ** (_math.log(arr._effective_size, 2)))
        return int(2 ** (_math.log(arr._effective_size, 2)+1))
    else:
        return len(arr)


class StaticArray:
    """A fixed-length sequence of references in contiguous memory.
    """

    def __init__(self, length: int) -> None:
        """Initialise an empty array of the given length.

        Preconditions: length >= 0
        Postconditions: every item in the array is None
        """
        self._items: list[object] = [None] * length

    def __len__(self) -> int:
        """Returns the length of the array.

        Accessed using the len(self) method.
        """
        return len(self._items)

    def __delitem__(self, index: int) -> None:
        """Remove the item stored in position index.

        Accessed using the del keyword.

        Preconditions: 0 <= index <= len(self)-1
        Postconditions: self[index] == None
        """
        self[index] = None

    def __getitem__(self, index: int) -> object:
        """Return the item stored in position index.

        Implements the Pythonic-style: self[index].

        Preconditions: 0 <= index <= len(self)-1
        """
        if index < 0 or index >= len(self):
            raise IndexError(f"Precondition: 0 <= index <= {len(self)-1}")
        return self._items[index]

    def __iter__(self) -> _ArrayIterator:
        """Return an iterator for traversing the array.
        """
        return iter(self._items)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({len(self)})"

    def __setitem__(self, index: int, item: object) -> None:
        """Replace the item at position index with the given item.

        Implements the Pythonic-style: self[index] = value.

        Preconditions: 0 <= index <= len(self)-1
        Postconditions: self[index] == item
        """
        self._items[index] = item

    def __str__(self) -> str:
        """Return a string representation of the array.
        """
        return str(self._items)

    def index(self, item) -> int:
        """Return the index of a given item.

        Precondition: item is contained in self
        """
        return self._items.index(item)


class DynamicArray(StaticArray):
    """An array that can grow and shrink.
    """

    def __init__(self) -> None:
        """Initialise an empty array.

        Postconditions: every item in the array is None
        """
        self._items: list[object] = [None]
        self._effective_size: int = 0

    @property
    def fill(self) -> float:
        """Returns the proportion of the effective size and the capacity
        of the array.
        """
        return self._effective_size / len(self)

    def __len__(self) -> int:
        """Returns the length of the array.

        Accessed using the len(self) method.
        """
        return len(self._items)

    def __setitem__(self, index: int, item: object) -> None:
        """@Override.
        Replace the item at position index with the given item.

        Implements the Pythonic-style: self[index] = value.

        Preconditions: 0 <= index <= len(self) - 1
        Postconditions: self[index] == item
        """
        if index < 0 or index >= len(self):
            raise IndexError(f"Precondition: 0 <= {index} <= {len(self)-1}")

        if self[index] is None and item is None:
            pass
        elif self[index] is None:
            self._effective_size += 1
        elif item is None:
            self._effective_size -= 1
        else:
            pass  # effective capacity is not changed
        self._items[index] = item

    def resize(self, capacity: int) -> None:
        """Extend or shrink the array.
        """
        alist: list[object] = [None] * capacity
        for index in range(self._effective_size):
            alist[index] = self[index]
        self._items = alist

    def shift(self, start: int, stop: int, step: int) -> None:
        """Shift the array's elements from the given start to the given
        end by the given step.

        Any existing items in the indices where items are moved will be
        overwritten.

        Preconditions:
        - start > 0
        - stop < len(self)
        - start < stop
        - start + step >= 0

        Postcondtions:
        """

        if step >= 0:  # shift to the right
            arr_range = range(stop, start-1, -1)
        else:
            arr_range = range(start, stop + 1, 1)
        for index in arr_range:
            self._items[index + step] = self._items[index]
            self._items[index] = None

    def __str__(self) -> str:
        """Return a string representation of the array.
        """
        return str(self._items)


class _ArrayIterator:
    """An iterator class for an array.
    """

    def __init__(self, array) -> None:
        """Initialises a ArrayIterator object.
        """
        self._items = array
        self._current: int = 0

    def __iter__(self) -> _Iterator:
        """Implements iter(self).
        """
        return self

    def __next__(self) -> object:
        """Return the next item in the sequence

        Implements `next(self)`.

        Raises:
            StopIteration: When there are no more elements to retrieve
            from the set.
        """
        item: object = None
        if self._current <= len(self._items) - 1:
            item = self._items[self._current]
            self._current += 1
            return item
        else:
            raise StopIteration


class ArrayHashMap(Map):
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


class HashSet(Set):
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

    def __eq__(self, right: HashSet) -> bool:
        if len(self) != len(right):
            return False
        else:
            for element in self:
                if element not in right:
                    return False
        return True

    def __lt__(self, right: HashSet) -> bool:
        if len(self) >= len(right):
            return False
        else:
            for element in self:
                if element not in right:
                    return False
        return True

    def __gt__(self, right: HashSet) -> bool:
        if len(self) <= len(right):
            return False
        return right < self

    def __le__(self, right: HashSet) -> bool:
        return (self == right) or (self < right)

    def __ge__(self, right: HashSet) -> bool:
        return (self == right) or (self > right)

    def __add__(self, right: HashSet) -> HashSet:
        union: HashSet = HashSet()
        for element in self:
            union.add(element)
        for element in right:
            union.add(element)
        return union

    def __mul__(self, right: HashSet) -> HashSet:
        intersection: HashSet = HashSet()
        if len(self) <= len(right):
            for element in self:
                if element in right:
                    intersection.add(element)
        else:
            for element in right:
                if element in self:
                    intersection.add(element)
        return intersection

    def __sub__(self, right: HashSet) -> HashSet:
        pass


@_dataclass
class _MapEntry:
    """Storage class for holding the key/value pairs
    """
    key: int
    value: object


_UNUSED = None
_EMPTY: _MapEntry = _MapEntry(None, None)

