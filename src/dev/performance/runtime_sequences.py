
"""A collection of functions to test the run-time of a sequence.
"""


def insert_start_remove_start(seq) -> None:
    """Insert an item at the start of the sequence, and the remove item from
    start
    """
    seq.insert(0, 0)
    seq.remove(0)


def append_remove_start(seq) -> None:
    """Append an item to a sequence, and then remove item from the start.
    """
    seq.append(0)
    seq.remove(0)


def insert_start_remove_end(seq) -> None:
    """Insert an item at the start of the sequence, and the remove item from
    start
    """
    seq.insert(0, 0)
    seq.remove(len(seq) - 1)


def append_remove_end(seq) -> None:
    """Append an item to a sequence, and then remove item from the start.
    """
    seq.append(0)
    seq.remove(len(seq) - 1)

