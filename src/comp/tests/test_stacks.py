
"""Implementation of black-box testing for the Stack.
"""


from .util import check
from ..datatypes.stacks import DequeStack, LinkedStack, Stack, BoundedStack, ArrayStack


def test_len(items: Stack, length: int) -> None:
    """Check that len(items) == length.
    """
    check(
        f"test len(items) == {length}",
        len(items) == length,
        True,
        items
    )


def test_init(items: Stack) -> None:
    """Check that items is the empty stack.
    """
    check('init length', len(items), 0, items)


def test_push_peek_pop(items: Stack, length: int) -> None:
    """Add 'length' values to stack, pop all items, and check
    length.

    Preconditions:
    - items is empty;
    - 0 < length <= items.capacity()
    """
    for num in range(length):
        items.push(num)
        check("push item", len(items), num+1, items)
    test_len(items, length)
    for num in range(length-1, -1, -1):
        check("peek item", items.peek(), num, items)
        items.pop()
        check("pop item", len(items), num, items)
    test_len(items, 0)


def test_bounded_stack(capacity: int = 6) -> None:
    """Run all tests for the BoundedStack.

    Precondition: capacity > 1
    """

    for capacity in range(1, capacity):
        print('Testing capacity', capacity)
        print("==================")
        test_init(BoundedStack(capacity))
        for length in range(1, capacity + 1):
            print('Testing length', length)
            test_push_peek_pop(BoundedStack(capacity), length)
        print("")


def test_array_stack(length: int = 5) -> None:
    """Run all tests for the ArrayStack.
    """

    test_init(ArrayStack())
    for length in range(1, length + 1):
        print('Testing length', length)
        test_push_peek_pop(ArrayStack(), length)


def test_linked_stack(length: int = 5) -> None:
    """Run all tests for the LinkedStack.

    Precondition: capacity > 1
    """

    test_init(LinkedStack())
    for length in range(1, length + 1):
        print('Testing length', length)
        test_push_peek_pop(LinkedStack(), length)


def test_deque_stack(length: int = 5) -> None:
    """Run all tests for the LinkedStack.

    Precondition: capacity > 1
    """

    test_init(DequeStack())
    for length in range(1, length + 1):
        print('Testing length', length)
        test_push_peek_pop(DequeStack(), length)
