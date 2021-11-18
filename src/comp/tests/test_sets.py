
"""Implementation of black-box testing for the set.
"""

from __future__ import annotations
from .util import check
from ..adt import Set


def test_membership(elements: Set, length: int) -> None:
    """Check that elements in range 0, ..., length are a member of the set.
    """
    for number in range(length):
        elements.add(number)
        test_len(elements, number+1)
    for number in range(length):
        check(f"{number} is member", number in elements, True, elements)
    check(f"'A' is not member", 'A' in elements, False, elements)


def test_len(elements: Set, length: int) -> None:
    """Check that len(items) == length.
    """
    check(f"test length={length}", len(elements) == length, True, elements)


def test_init(items: Set) -> None:
    """Check that items is the empty sequence.
    """
    check('init length', len(items), 0, items)


def test_add(elements: Set, length: int) -> None:
    """Check that len(items) == length.
    """

    for number in range(1, length+1):
        elements.add(number)
        check("add: contains", number in elements, True, elements)
        check(f"add, len", len(elements) == number, True, elements) 

    for number in range(1, length+1):
        elements.add(number)
        check(f"add duplicate: len", len(elements) == length, True, elements)   


def test_remove(elements: Set, length: int) -> None:
    """Check that len(items) == length.
    """

    for number in range(1, length+1):
        elements.add(number)

    for number in range(length, 0, -1):
        elements.remove(number)
        check("remove: contains", number not in elements, True, elements)
        check(f"remove: len", len(elements) == number-1, True, elements) 


def test_equality(left: Set, right: Set, up: Set, length: int) -> None:
    """Add elements to left right, and up, and check for equality.
    """

    letters: str = "abcdefghijklmnopqrstuvwxyz"

    if length == 0:
        return

    for number in range(length):
        left.add(number)
    for number in range(length-1, -1, -1):
        right.add(number)
    for number in range(length, length*2):
        up.add(number)

    check(f"Equality", left == left, True, f"{left} and {left}")
    check(f"Equality", left == right, True, f"{left} and {right}")
    check(f"Non-Equality", left == up, False, f"{left} and {up}")


def test_subset(left: Set, right: Set, up: Set, length: int) -> None:
    """Add elements to left right, and up, and check for subsets.
    """

    if length == 0:
        return

    for number in range(length):
        left.add(number)
    for number in range(length*2):
        right.add(number)
    for number in range(length, length*2):
        up.add(number)

    check(f"is subset", left < left, False, f"{left} and {left}")
    check(f"is subset", left < right, True, f"{left} and {right}")
    check(f"is not subset", left < up, False, f"{left} and {up}")


def test_subset_eq(left: Set, right: Set, up: Set, length: int) -> None:
    """Add elements to left right, and up, and check for subsets.
    """

    if length == 0:
        return

    for number in range(length):
        left.add(number)
    for number in range(length*2):
        right.add(number)
    for number in range(length, length*2):
        up.add(number)

    check(f"is subset or equal", left <= left, True, f"{left} and {left}")
    check(f"is subset or equal", left <= right, True, f"{left} and {right}")
    check(f"is not subset or equal", left <= up, False, f"{left} and {up}")


def test_superset(left: Set, right: Set, up: Set, length: int) -> None:
    """Add elements to left right, and up, and check for subsets.
    """

    if length == 0:
        return

    for number in range(length):
        left.add(number)
    for number in range(length*3):
        right.add(number)
    for number in range(length, length*3):
        up.add(number)

    check(f"is superset", right > left, True, f"{left} and {left}")
    check(f"is not superset", up > left, False, f"{left} and {up}")


def test_superset_eq(left: Set, right: Set, up: Set, length: int) -> None:
    """Add elements to left right, and up, and check for subsets.
    """

    if length == 0:
        return

    for number in range(length):
        right.add(number)
    for number in range(length*3):
        left.add(number)
    for number in range(length*100, length*100 + length):
        up.add(number)

    check(f"is superset or equal", left >= left, True, f"{left} and {left}")
    check(f"is superset or equal", left >= right, True, f"{left} and {right}")
    check(f"is not superset or equal", left >= up, False, f"{left} and {up}")
