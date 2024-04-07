"""
MutableString
-------------

The `MutableString` class represents a mutable string object.

This class mimics a Python string object, but being mutable at the same time. It stores
the content of the string and provides some of the methods that the original Python `str`
class provides.

__author__ = "Studio W Engineers"

__version__ = "0.1.0"

__maintainer__ = "Studio W Engineers"

__email__ = "studio.w.engineers@gmail.com"

__status__ "Release to manufacturing"
"""
# standard library imports

# third party library imports

# local library specific imports


class MutableString:
    """This class mimics a Python string object, but being mutable at the same time.
    It stores the content of the string and provides some of the methods that the original
    Python `str` class provides.
    """
    def __add__(self, value: str) -> str:
        if not isinstance(value, str):
            err_msg = (f"Sum operation for MutableString objects is possible only from "
                       f"strings, given of type \"{type(value)}\"!")
            raise RuntimeError(err_msg)

        return self._data + value

    def __init__(self, string: str = "") -> None:
        if not isinstance(string, str):
            err_msg = (f"MutableString objects can be created only from strings, given "
                       f"of type \"{type(string)}\"!")
            raise RuntimeError(err_msg)

        self._data = string

    def __eq__(self, other: object) -> bool:
        return self._data == other

    def __getitem__(self, value: int | slice) -> str:
        if isinstance(value, int):
            if value < 0:
                value += len(self._data)

            if value < 0 or value >= len(self._data):
                raise IndexError(f"The given index {value} is out of range!")

            return self._data[value]

        if isinstance(value, slice):
            return "".join(self._data[item]
                           for item in range(*value.indices(len(self._data))))

        raise TypeError(f"Slicing cannot be done with type of \"{type(value)}\"!")

    def __hash__(self) -> int:
        return hash(self._data)

    def __mul__(self, value: int) -> str:
        if not isinstance(value, int):
            err_msg = (f"Multiplication operation for MutableString objects is possible "
                       f"only from integers, given of type \"{type(value)}\"!")
            raise RuntimeError(err_msg)

        return self._data * value

    def __repr__(self) -> str:
        return self._data

    def __setitem__(self, item: int, value: str) -> None:
        if not isinstance(value, str):
            err_msg = (f"Set operation for MutableString objects is possible "
                       f"only with strings, given value of type \"{type(value)}\"!")
            raise RuntimeError(err_msg)

        if not isinstance(item, int):
            err_msg = ("Set operation for MutableString objects is not possible "
                       "with slices!")
            raise RuntimeError(err_msg)

        if item == -1:
            item += len(self._data)

        elif item < 0:
            err_msg = f"Trying to set a value to an unknown position: {item}!"
            raise RuntimeError(err_msg)

        self._data = self._data[:item] + value + self._data[item + len(value):]

    def capitalize(self) -> None:
        """Capitalize the first character and the rest convert to lowercase.
        If Python >= 3.8: the first character is put into titlecase rather than uppercase.
        """
        self._data = self._data.capitalize()

    def lower(self) -> None:
        """Convert the string to lowercase.
        """
        self._data = self._data.lower()

    def lstrip(self) -> None:
        """Remove leading whitespaces.
        """
        self._data = self._data.lstrip()

    def rstrip(self) -> None:
        """Remove trailing whitespaces.
        """
        self._data = self._data.rstrip()

    def split(self, sep: str | None = None, maxsplit: int = -1) -> list[str]:
        """Return a list of the substrings in the string, using `sep` as string separator.

        Parameters
        ----------
        sep : str | None, optional
            The separator used to split the string. When set to None (the default value),
            it will split on any whitespace character (including \\n \\r \\t \\f and
            spaces) and it will discard empty strings from the result.
        maxsplit : int, optional
            Maximum number of splits (starting from the left). -1 (the default value)
            means no limit.

        Returns
        -------
        list[str]
        """
        return self._data.split(sep, maxsplit)

    def to_string(self) -> str:
        """Return the content of this `MutableString` as `str`.

        Returns
        -------
        str
        """
        return self._data

    def upper(self) -> None:
        """Convert the string to uppercase.
        """
        self._data = self._data.upper()
