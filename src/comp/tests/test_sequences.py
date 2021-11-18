
"""Implementation of black-box testing for a subclass of Sequence.
See p204.
"""


from __future__ import annotations
from .util import check
from ..datatypes.sequences import Sequence
from opyn.comp.datatypes import sequences


def test_items(test: str, items: Sequence) -> None:
    """Check that items is the sequence 0, 1, 2, ..., length - 1.
    """
    for index in range(len(items)):
        check(test + ': n-th item', items[index], index, items)


def test_len(items: Sequence, length: int) -> None:
    """Check that len(items) == length.
    """
    check(
        f"test length={length}",
        len(items) == length,
        True,
        items
    )


def test_init(items: Sequence) -> None:
    """Check that items is the empty sequence.
    """
    check('init length', len(items), 0, items)
    test_items('init', items)


def test_append(items: Sequence, length: int) -> None:
    """Check a sequence created with successive appends.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length):
        items.append(num)
    test_items('append', items)
    test_len(items, length)


def test_prepend(items: Sequence, length: int) -> None:
    """Check a sequence created by successive inserts at index 0.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length-1, -1, -1):
        items.prepend(num)
    test_items('prepend', items)
    test_len(items, length)


def test_swap(items: Sequence, length: int) -> None:
    """Create a sequence of a given length, swap the first and last items,
    and check items.

    Preconditions:
    - items is empty;
    - 2 <= length
    """
    for num in range(length):
        items.prepend(num)
    if length >= 2:
        items.swap(0, len(items)-1)
        check("swap, first", items[0], 0, items)
        check("swap, last", items[len(items)-1], len(items)-1, items)


def test_index(items: Sequence, length: int) -> None:
    """Create a sequence of a given length, swap the first and last items,
    and check items.

    Preconditions:
    - items is empty;
    - 1 <= length
    """
    for num in range(length):
        items.append(num)
    if length >= 1:
        for num in range(length):
            check(f"index of {num}", items.index(num), num, items)


def test_add(left: Sequence, right: Sequence, length: int) -> None:
    """Populate left and right, concatenate left and right, and check
    items.

    Preconditions:
    - left, right are empty;
    """
    py_list: list = []
    for num in range(length):
        left.append(num)
        right.append(num)
        py_list.append(num)
    py_list = py_list + py_list
    joined: Sequence = left + right
    for index in range(length):
        check("add", joined[index], py_list[index], joined)


def test_mul(items: Sequence, length: int) -> None:
    """Populate items, repeatedly concatenate, and check items.

    Preconditions:
    - items is empty
    """
    py_list: list = []
    for num in range(length):
        items.append(num)
        py_list.append(num)
    py_list = py_list * 2
    items = items * 2
    for index in range(len(items)):
        check("mul", items[index], py_list[index], items)


def run_tests_bounded_sequence(capacity: int = 6) -> None:
    """Run all tests forthe bounded sequence.
    """
    for capacity in range(1, capacity):
        print(f"Testing capacity: {capacity}")
        print("===================")
        test_init(sequences.BoundedSequence(capacity))
        for length in range(capacity+1):
            print(f"Testing length: {length}")
            test_prepend(sequences.BoundedSequence(capacity), length)
            test_append(sequences.BoundedSequence(capacity), length)
            test_swap(sequences.BoundedSequence(capacity), length)
            test_index(sequences.BoundedSequence(capacity), length)
            test_add(
                sequences.BoundedSequence(capacity),
                sequences.BoundedSequence(capacity),
                length
            )
            test_mul(sequences.BoundedSequence(capacity), length)

        print("***\n")


def run_tests_array_sequence(length: int = 5) -> None:
    """Run all tests forthe bounded sequence.
    """
    test_init(sequences.ArraySequence())
    for length in range(length+1):
        print(f"Testing length: {length}")
        test_prepend(sequences.ArraySequence(), length)
        test_append(sequences.ArraySequence(), length)
        test_swap(sequences.ArraySequence(), length)
        test_index(sequences.ArraySequence(), length)
        test_add(
            sequences.ArraySequence(),
            sequences.ArraySequence(),
            length
        )
        test_mul(sequences.ArraySequence(), length)


def run_tests_linked_sequence(length: int = 5) -> None:
    """Run all tests for the linked sequence.
    """
    test_init(sequences.LinkedSequence())
    for length in range(length+1):
        print(f"Testing length: {length}")
        test_prepend(sequences.LinkedSequence(), length)
        test_append(sequences.LinkedSequence(), length)
        test_swap(sequences.LinkedSequence(), length)
        test_index(sequences.LinkedSequence(), length)
        test_add(
            sequences.LinkedSequence(),
            sequences.LinkedSequence(),
            length
        )
        test_mul(sequences.LinkedSequence(), length)
