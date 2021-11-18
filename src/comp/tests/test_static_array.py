
"""Black-box testing of the StaticArray ADT
"""


from __future__ import annotations
from .util import check
from ..datatypes.arrays import StaticArray


def test_init(length: int) -> None:
    """Initialise an array of given length, replace all items, and check
    it.

    Precondtions: length >= 0
    """
    array: StaticArray = StaticArray(length)
    check('length', len(array), length, array)
    for index in range(length):
        check('initial item', array[index], None, array)


def test_set_item(length: int) -> None:
    """Create an array of arg length, replace all items and check it

    Preconditions: length >= 0
    """
    array = StaticArray(length)
    for index in range(length):
        array[index] = index
    for index in range(length):
        check('replaced item', array[index], index, array)


def test_del_item(length: int) -> None:
    """Create an array of arg length, replace all items, then remove each
    item and check it.
    """
    array: StaticArray = StaticArray(length)
    for index in range(length):
        array[index] = index
    for index in range(length-1, -1, -1):
        del array[index]
    for index in range(length):
        check('replaced item', array[index], None, array)


def test_iter(length: int) -> None:
    """Create an array of arg length, replace all items, iterate through
    the array and append it to a list, and check it.
    """
    array = StaticArray(length)
    for index in range(length):
        array[index] = index
    array_list = []
    for item in array:
        array_list.append(item)
    check("iterate over array", str(array_list), str(array), array)

def run_tests(length: int = 5) -> None:
    """Run all tests in the module
    - test_init
    - test_set_item

    Preconditions: length >= 0
    """
    for size in range(0, length):
        test_init(size)
        test_set_item(size)
        test_del_item(size)
        test_iter(size)
