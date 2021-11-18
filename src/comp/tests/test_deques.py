
"""Implementation of black-box testing for Deques.
"""


from __future__ import annotations
from .util import check as _check
from ..adt import Deque


def test_init(items: Deque) -> None:
    """Check that items is the empty sequence.
    """
    _check('init length', len(items), 0, items)
    # test_items('init', items)


def test_len(items: Deque, length: int) -> None:
    """Check that the length of the deque is equal to a given length.
    """
    _check(f"test length={length}", len(items) == length, True, items)


def test_add_right(items: Deque, length: int) -> None:
    """Check a deque created with successive additions to the right.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length):
        items.add_right(num)
        _check("add right: peek", items.peek_right(), num, items)
        _check("add right: len", len(items), num+1, items)


def test_add_left(items: Deque, length: int) -> None:
    """Check a deque created with successive additions to the right.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length):
        items.add_left(num)
        _check("add left: peek", items.peek_left(), num, items)
        _check("add left: len", len(items), num+1, items)


def test_remove_right(items: Deque, length: int) -> None:
    """Check a deque created with successive additions to the right.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length+1):
        items.add_right(num)
    expected_length = len(items)
    while not items.is_empty():
        item: object = items.peek_right()
        items.remove_right()
        expected_length -= 1
        if len(items) >= 1:
            _check("remove right: peek", items.peek_right() == item, False, items)
            _check("remove right: len", len(items), expected_length, items)


def test_remove_left(items: Deque, length: int) -> None:
    """Populate deque, check deque after repeated removals from the left.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length+1):
        items.add_right(num)
    expected_length = len(items)
    while not items.is_empty():
        item: object = items.peek_left()
        items.remove_left()
        expected_length -= 1
        if len(items) >= 1:
            _check("remove left: peek", items.peek_left() == item, False, items)
            _check("remove left: len", len(items), expected_length, items)


def test_remove(items: Deque, length: int) -> None:
    """Populate deque, check deque after repeated removals from middle.

    Preconditions:
    - items is empty;
    - 3 <= length
    """
    alist: list[str] = []
    if length >= 3:
        for num in range(3):
            alist.append(num)
            items.add(num, num)
        while len(alist) > 2:
            alist.pop(1)
            items.remove(1)
            test_len(items, len(alist))

        for index in range(len(items)):
            _check(f"adding {index} item :", items[index], alist[index], items)
