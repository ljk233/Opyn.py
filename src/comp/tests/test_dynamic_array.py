
"""Black-box testing of the StaticArray ADT
"""


from __future__ import annotations
from .util import check
from ..datatypes.arrays import DynamicArray


def test_init(length: int) -> None:
    """Initialise an array of given length, replace all items, and check
    it.

    Precondtions: length >= 0
    """
    array: DynamicArray = DynamicArray(length)
    for index in range(length):
        array[index] = index
    for index in range(length):
        check('replaced item', array[index], index, array)


def test_set_item(length: int) -> None:
    """Create an array of arg length, replace all items and check it

    Preconditions: length >= 0
    """
    array: DynamicArray = DynamicArray(length)
    for index in range(length):
        array[index] = index
    for index in range(length):
        check('replace item', array[index], index, array)


def test_resize(old_length: int, new_length: int) -> None:
    """Test resizing a dynamic array from old_length to new_length.

    Preconditions:
    - 0 <= old_length; 0 <= new_length
    - old_length != new_length
    """
    array: DynamicArray = DynamicArray(old_length)
    # populate the array
    for index in range(old_length):
        array[index] = index
    # resize the array
    array.resize(new_length)
    check('new length', len(array), new_length, array)
    # check the original items are still present
    for index in range(new_length):
        if index < min(old_length, new_length):
            value = index
        else:
            value = None
        check('get item', array[index], value, array)
