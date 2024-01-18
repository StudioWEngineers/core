"""
MutableStringTestSuite
----------------------

Tests for the `MutableString` class.


__author__ = "Massimiliano Zecchetto"

__version__ = "0.0.0"

__maintainer__ = "Massimiliano Zecchetto"

__email__ = "eng.massimiliano.zecchetto@gmail.com"

__status__ "Release to manufacturing"
"""
# standard library imports
import unittest

# third party library imports

# local library specific imports
from ..mutable_string import MutableString


class MutableStringTestSuite(unittest.TestCase):
    """
    Tests for the `MutableString` class.
    """
    def test_add(self) -> None:
        """Tests for the `__add__` method.
        """
        string = MutableString("abc")

        with self.subTest():
            self.assertTrue(string + "a" == "abca")

        with self.subTest():
            self.assertFalse(string + "a" == "acc")

    def test_capitalize(self) -> None:
        """Tests for the `capitalize` method.
        """
        string = MutableString("abc")
        string.capitalize()

        self.assertEqual(string, "Abc")

    def test_equal(self) -> None:
        """Tests for the rich comparison `__eq__` method.
        """
        string = MutableString("abc")

        with self.subTest():
            self.assertTrue(string == "abc")

        with self.subTest():
            self.assertFalse(string == "acc")

    def test_empty_string(self) -> None:
        """Tests for the empty string.
        """
        self.assertEqual(MutableString(), "")

    def test_get_item_int(self) -> None:
        """Tests for the `__getitem__` method, with `int` input.
        """
        string = MutableString("abc")

        with self.subTest():
            self.assertEqual(string[0], "a")

        with self.subTest():
            self.assertEqual(string[-1], "c")

        with self.subTest():
            self.assertEqual(string[-2], "b")

        with self.subTest():
            self.assertEqual(string[1], "b")

        with self.assertRaises(IndexError):
            self.assertEqual(string[4], "")

        with self.assertRaises(IndexError):
            self.assertEqual(string[-4], "")

    def test_get_item_slice(self) -> None:
        """Tests for the `__getitem__` method, with `slice` input.
        """
        string = MutableString("abcdef")

        with self.subTest():
            self.assertEqual(string[0:3], "abc")

        with self.subTest():
            self.assertEqual(string[1:4], "bcd")

        with self.subTest():
            self.assertEqual(string[1:6:2], "bdf")

    def test_iterable(self) -> None:
        """Tests for the `__hash__` method.
        """
        string_1 = MutableString("abc")
        string_2 = MutableString("def")
        string_3 = MutableString("ghi")
        a_list = [string_1, string_2, string_3]

        expected_values = ["abc", "def", "ghi"]
        count = 0
        for item in a_list:
            with self.subTest(target = expected_values[count], source = item):
                self.assertEqual(item, expected_values[count])
            count += 1

    def test_lower(self) -> None:
        """Tests for the `lower` method.
        """
        string = MutableString("ABC")
        string.lower()

        self.assertEqual(string, "abc")

    def test_multiplication(self) -> None:
        """Tests for the `__mul__` method.
        """
        self.assertEqual(MutableString("ABC") * 3, "ABCABCABC")

    def test_to_string_method(self) -> None:
        """Test for the `to_string` method.
        """
        mutable_string = MutableString("ABC")

        with self.subTest():
            self.assertTrue(isinstance(mutable_string.to_string(), str))

        with self.subTest():
            self.assertTrue(mutable_string.to_string(), "ABC")

    def test_set(self) -> None:
        """Tests for the `__setitem__` method.
        """
        string = MutableString("ABC")

        with self.subTest():
            string[0] = "1"
            self.assertEqual(string, "1BC")

        with self.subTest():
            string[-1] = "c"
            self.assertEqual(string, "1Bc")

        with self.subTest():
            string[1] = "D"
            self.assertEqual(string, "1Dc")

    def test_split(self) -> None:
        """Tests for the `split` method.
        """
        string = MutableString("This is a separated.string")

        with self.subTest():
            self.assertEqual(string.split(" ")[1], "is")

        with self.subTest():
            self.assertEqual(string.split(".")[0], "This is a separated")

        with self.subTest():
            self.assertEqual(string.split(" "), ["This", "is", "a", "separated.string"])

        with self.subTest():
            self.assertEqual(string.split(), ["This", "is", "a", "separated.string"])

    def test_upper(self) -> None:
        """Tests for the `upper` method.
        """
        string = MutableString("abc")
        string.upper()

        self.assertEqual(string, "ABC")
