
"""
A library of implementations from M269.
"""


def has_internet_connection(
    in_flight_mode: bool, wifi_on: bool, data_on: bool
) -> bool:
    """Return whether or not a mobile phone has an internet connection.

    Postcondtion: has internet if and only if (not in flight mode)
    and (wifi on or data on)
    """
    return (not in_flight_mode) and (wifi_on or data_on)


def has_grade(mark: int) -> int:
    """Return the pass grade, from 1 to 5, for the given mark.

    Preconditions: 0 <= mark <= 100
    Postconditions:
    - if mark < 40, return 5
    - if 40 <= mark < 50, return 4
    - if 50 <= mark < 60, return 3
    - if 60 <= mark < 80, return 2
    - if mark >= 80, return 1
    """
    if mark < 40:
        grade = 5
    elif mark < 50:
        grade = 4
    elif mark < 60:
        grade = 3
    elif mark < 80:
        grade = 2
    else:
        grade = 1
    return grade
