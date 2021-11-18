
"""Black-box testing of the StaticArray ADT
"""


from __future__ import annotations
from .util import check
from ..linkedlists import LinkedList

def test_contains(test_str: str, linkedlist: LinkedList, length: int) -> None:
    """Check the membership of a linked list.
    """
    counter: int = 0
    while counter <= length:
        check(f"{test_str} (membership)", linkedlist[counter], counter, linkedlist)
        counter += 1


def test_init() -> None:
    """Initialise a linked list of given length, replace all items, and
    check it.

    Precondtions: length >= 0
    """
    linkedlist: LinkedList = LinkedList()
    check('length', len(linkedlist), 0, linkedlist)


def test_length(length: int) -> None:
    """Initialise a linked list of given length, add length items,
    and check its length.

    Precondtions: length >= 0
    """
    linkedlist: LinkedList = LinkedList()
    for number in range(length):
        linkedlist.insert(number, number)
        check(f"test length", len(linkedlist), number+1, linkedlist)


def test_insert(length: int) -> None:
    """Initialise a linked list of given length, add length items,
    and check membership and length.

    Precondtions: length >= 0
    """
    from random import randint

    linkedlist: LinkedList = LinkedList()

    expected_len: int = 0

    for number in range(length):
        linkedlist.insert(number, number)
        expected_len += 1
        check("test insert: right", linkedlist[number], number, linkedlist)
        check("test insert: len", len(linkedlist), expected_len, linkedlist)

    for number in range(length):
        linkedlist.insert(0, number)
        expected_len += 1
        check("test insert: left", linkedlist[0], number, linkedlist)
        check("test insert: len", len(linkedlist), expected_len, linkedlist)

    for number in range(length):
        rand: int = randint(0, len(linkedlist))
        expected_len += 1
        linkedlist.insert(rand, rand)
        check(
            "test insert: random index",
            linkedlist[rand],
            rand,
            linkedlist
        )
        check("test insert: len", len(linkedlist), expected_len, linkedlist)


def test_getitem(length: int) -> None:
    """Initialise a linked list of given length, add length items,
    and check their index.

    Precondtions: length >= 0
    """
    linkedlist: LinkedList = LinkedList()
    for number in range(length):
        linkedlist.insert(number, number)
    for number in range(length):
        check('get item', linkedlist[number], number, linkedlist)


def test_setitem(length: int) -> None:
    """Initialise a linked list of given length, add length items,
    replace items, and check their index.

    Precondtions: length >= 0
    """
    linkedlist: LinkedList = LinkedList()
    for number in range(length):
        linkedlist.insert(number, number)
    for number in range(length):
        linkedlist[number] = number * 2
        check('set item', linkedlist[number], number * 2, linkedlist)


def test_delitem(length: int) -> None:
    """Create an array of arg length, replace all items, then remove each
    item and check it.
    """
    from random import randint
    linkedlist: LinkedList = LinkedList()
    if length == 0:
        pass  # cannt remove from empy list
    elif length == 1:
        linkedlist.insert(0, 0)
        del linkedlist[0]
        check("test remove: len", len(linkedlist), 0, linkedlist)
        linkedlist.insert(0, 0)
        del linkedlist[len(linkedlist)-1]
        check("test remove: len", len(linkedlist), 0, linkedlist)
    else:
        exp_len = 0
        for number in range(length):
            linkedlist.insert(number, number)
            exp_len += 1
        while len(linkedlist) >= 2:
            rand = randint(0, len(linkedlist)-2)
            del linkedlist[rand]
            exp_len -= 1
            check(
                "remove random",
                linkedlist[rand] != rand,
                True,
                linkedlist
            )
            check("test insert: len", len(linkedlist), exp_len, linkedlist)


def test_iter(length: int) -> None:
    """Create an array of arg length, replace all items, iterate through
    the array and add it to a list, and check it.
    """
    linkedlist: LinkedList = LinkedList()
    for number in range(length):
        linkedlist.insert(number, number)
    # print(str(linkedlist))
    array_list = []
    for item in linkedlist:
        array_list.append(item)
    # print(str(array_list))
    check("iterate", str(linkedlist), str(array_list), linkedlist)


def test_reversed(length: int) -> None:
    """Create an array of arg length, replace all items, iterate through
    the array in reverse and add it to a list, and check it.
    """
    linkedlist: LinkedList = LinkedList()
    for number in range(length):
        linkedlist.insert(0, number)
    array_list = []
    for item in reversed(linkedlist):
        array_list.insert(0, item)
    check("rev iterate", str(linkedlist), str(array_list), linkedlist)
