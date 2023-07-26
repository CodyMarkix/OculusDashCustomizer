import re

def strToTuple(string: str):
    """
    A function that converts a string like this: '(45, 68, 45)' into a tuple.
    Don't feed it a tuple with strings or it will return an empty tuple.
    """

    try:
        stripped = re.sub("[()]", "", string)
        arr = [float(i) for i in stripped.split(",")]
        tup = tuple(arr)

        return tup
    except ValueError:
        return (0, 0, 0)
