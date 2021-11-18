
"""
Alibrary of functions designed to for various test.
"""

from __future__ import annotations


def check(
    case: str,
    actual: object,
    expected: object,
    context: object
) -> None:
    """Write a message if actual and expected are different.
    """
    err: str = f"{case} FAILED for {context}: {actual} instead of {expected}"
    if actual != expected:
        print(err)
