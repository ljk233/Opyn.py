
# %%
from __future__ import annotations as _annotations
from typing import NoReturn


class Counter:

    """An implementation of the counter ADT
    """

    def __init__(self) -> None:
        self.items: dict[object, int] = {}

    def __contains__(self, item: object) -> bool:
        """Determine if the given item is currently being counted.
        """
        return item in self.items

    def __setitem__(self, item: object, val: int) -> NoReturn:
        """Set the count of the given item to the given value in the
        counter.
        """
        self.items[item] = val

    def __getitem__(self, item: object) -> object:
        """Return the count for the given item.
        """
        return self.items[item]

    def __len__(self) -> int:
        """Return the number of items being counted by the counter.
        """
        return len(self.items)

    def __str__(self) -> str:
        return str(self.items)

    def __repr__(self) -> str:
        return f"counter({len(self.items)})"

    def add(self, item: object) -> NoReturn:
        """Incrment the count for the given item in the given counter.
        """
        if item not in self:
            self.items[item] = 1
        else:
            self.items[item] = self.items[item] + 1

    def remove(self, item: object) -> NoReturn:
        """Decrement the count for the given item in the given counter.
        """
        if item in self:
            self.items[item] -= 1

    def isempty(self) -> bool:
        """Determine if the counter is empty.
        """
        return len(self) == 0


# %%
def mode(text: str) -> str:
    counter: Counter = Counter()
    maxchar: str = ""
    maxcount: int = 0
    for char in text:
        counter.add(char)
        if maxchar != char and counter[char] > maxcount:
            maxchar = char
            maxcount = counter[char]
    return maxchar
