
"""Implementation of black-box testing for vectors.
"""


from __future__ import annotations
from .util import check
from ..datatypes.vectors import Vector
from ..datatypes import vectors


def test_items(test: str, items: Vector) -> None:
    """Check that items is the vector 0, 1, 2, ..., length - 1.
    """
    for index in range(len(items)):
        check(test + ': n-th item', items[index], index, items)


def test_len(items: Vector, length: int) -> None:
    """Check that len(items) == length.
    """
    check(
        f"test len(items) == {length}",
        len(items) == length,
        True,
        items
    )


def test_init(items: Vector) -> None:
    """Check that items is the empty vector.
    """
    check('init length', len(items), 0, items)
    test_items('init', items)


def test_insert_start(items: Vector, length: int) -> None:
    """Check a vector created by successive inserts at index 0.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length, -1, -1):
        items.insert(0, num)
    test_items('insert at 0', items)


def test_insert_end(items: Vector, length: int) -> None:
    """Check a vector created with successive insertions at end.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length):
        items.insert(len(items), num)
    test_items('append', items)


def test_set_item(items: Vector, length: int) -> None:
    """Check a vector created by replacing all items.

    Preconditions:
    - items is empty;
    - 0 <= length
    """
    for num in range(length):
        items.insert(len(items), num)
    for num in range(length):
        items[num] = num
    test_items('set item', items)


def test_contains(items: Vector, length: int) -> None:
    """Add 'length' values to items and check membership.

    Preconditions:
    - items is empty;
    - 0 <= length
    """

    for num in range(length):
        items.insert(len(items), num)

    if len(items) == 0:
        pass  # no items to check
    elif len(items)== 1:
        check("has first item", 0 in items, True, items)
        check("has not -1", -1 in items, False, items)
    elif len(items)== 2:
        check("has first item", 0 in items, True, items)
        check("has last item", 1 in items, True, items)
        check("has not -1", -1 in items, False, items)
    else:
        check("has first item", 0 in items, True, items)
        check("has middle item", (len(items) // 2) in items, True, items)
        check("has last item", (len(items) - 1) in items, True, items)
        check("has not -1", -1 in items, False, items)       


def test_remove_first(items: Vector, length: int) -> None:
    """Add 'length' values to items, remove the first item, and check
    membership and length.

    Preconditions:
    - items is empty;
    - 0 <= length
    """

    for num in range(length):
        items.insert(len(items), num)

    if length == 0:
        pass  # cannot remove from an empty list
    elif length == 1:
        del items[0]
        test_len(items, 0)
    else:
        del items[0]
        for index in range(1, len(items)):
            check(
                "remove first item" + ': n-th item',
                items[index - 1],
                index,
                items
            )
        check( 
            'remove first item : length <= capacity',
            len(items) <= length-1,
            True,
            items
        )


def test_remove_last(items: Vector, length: int) -> None:
    """Add 'length' values to items, remove the last item, and check
    membership and length.

    Preconditions:
    - items is empty;
    - 1 <= length
    """
    for num in range(length):
        items.insert(len(items), num)

    if length == 0:
        pass  # cannot remove from an empty list
    elif length == 1:
        del items[len(items) - 1]
        test_len(items, 0)
    else:
        del items[len(items) - 1]
        test_items('remove last item', items)


def run_tests_bounded_vector(capacity: int = 6) -> None:
    """Run all tests for the BoundedVector.
    """
    for capacity in range(1, capacity):
        print(f"Testing capacity: {capacity}")
        print("===================")
        test_init(vectors.BoundedVector(capacity))
        for length in range(capacity+1):
            print(f"Testing length: {length}")
            test_insert_end(vectors.BoundedVector(capacity), length-1)
            test_insert_start(vectors.BoundedVector(capacity), length-1)
            test_set_item(vectors.BoundedVector(capacity), length)
            test_contains(vectors.BoundedVector(capacity), length)
            test_remove_first(vectors.BoundedVector(capacity), length)
            test_remove_last(vectors.BoundedVector(capacity), length)
        print("***\n")


def run_tests_array_vector(length: int = 5) -> None:
    """Run all tests for the ArrayVector.
    """
    test_init(vectors.ArrayVector())
    for length in range(length+1):
        print(f"Testing length: {length}")
        test_insert_end(vectors.ArrayVector(), length)
        test_insert_start(vectors.ArrayVector(), length)
        test_set_item(vectors.ArrayVector(), length)
        test_contains(vectors.ArrayVector(), length)
        test_remove_first(vectors.ArrayVector(), length)
        test_remove_last(vectors.ArrayVector(), length)


def run_tests_linked_vector(length: int = 5) -> None:
    """Run all tests for the LinkedVector.
    """
    test_init(vectors.LinkedVector())
    for length in range(length+1):
        print(f"Testing length: {length}")
        test_insert_end(vectors.LinkedVector(), length)
        test_insert_start(vectors.LinkedVector(), length)
        test_set_item(vectors.LinkedVector(), length)
        test_contains(vectors.LinkedVector(), length)
        test_remove_first(vectors.LinkedVector(), length)
        test_remove_last(vectors.LinkedVector(), length)
