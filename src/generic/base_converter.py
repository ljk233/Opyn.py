
"""A collection of functions for various conversions between standard
number bases.
"""

from ..comp.collections import DequeStack as _DequeStack
from ..comp.collections import DequeQueue as _DequeQueue


def decimal_to_base(dec_num: int, base: int) -> str:
    """Return a positive decimal number in terms of another base.

    Precondition:
    - 2 <= base <= 36
    """
    digits: str = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    remainders: _DequeStack = _DequeStack()
    while dec_num >= 1:
        a_remainder: int = dec_num % base
        remainders.push(a_remainder)
        dec_num = dec_num // base

    new_base_text: str = ""
    while not remainders.is_empty():
        new_base_text += digits[remainders.peek()]
        remainders.pop()

    return new_base_text


def base_to_decimal(base_num: str, base: int) -> int:
    """Return a number of a given base as a decimal numer.

    Precondition:
    - 2 <= base <= 36
    """

    base_digits: list[str] = [
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
        "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
        "U", "V", "W", "X", "Y", "Z",
    ]

    digits: _DequeQueue = _DequeQueue()
    while len(base_num) >= 1:
        a_digit: str = base_digits.index(base_num[len(base_num)-1])
        digits.enqueue(a_digit)
        base_num = base_num[0:len(base_num)-1]

    dec_num: int = 0
    power: int = 0
    while not digits.is_empty():
        dec_num += digits.front() * (base ** power)
        digits.dequeue()
        power += 1

    return dec_num
