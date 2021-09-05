
"""
"""


from scipy import stats as st
from numpy.typing import ArrayLike


def get_sample(n: int) -> ArrayLike:
    """
    Generates a random sample of die rolls.

    Args:
        n (int): Number of times to roll the die

    Returns:
        ArrayLike: Array of die rolls
    """

    # declare parameters
    u: st.randint = st.randint(1, 7)
    # simulate trial
    return u.rvs(n)
