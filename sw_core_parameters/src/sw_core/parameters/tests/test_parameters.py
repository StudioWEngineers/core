"""
ParametersTest
--------------

This module aims at providing extensive testing for the `Parameters` class.

__author__ = "Studio W Engineers"

__version__ = "0.0.1"

__maintainer__ = "Studio W Engineers"

__email__ = "studio.w.engineers@gmail.com"

__status__ "Release"
"""
# standard library imports
import unittest
from pathlib import Path

# third party library imports

# local library specific imports
from ..parameters import Parameters


class ParametersTests(unittest.TestCase):
    """The `Parameters` test class.
    """
    def setUp(self) -> None:
        """Creates a `Parameters` object to be used for all the tests.
        """
        inputs_for_testing = """{
            "string_input": "my_string",
            "float_input": 1.1,
            "int_input": 1,
            "list_input": [1, 2, 3],
            "nested_list_input": [[1, 2], [3, 4]],
            "nested_list_of_dict": [{
                "int": 1,
                "bool": false
            },{
                "float": 1.2,
                "list": [1, 2]
            }],
            "dict_input": {
                "sub_string_input": "my_sub_string",
                "sub_float_input": 11.1,
                "sub_int_input": 10,
                "sub_list_input": [10, 20, 30],
                "sub_bool_input": true,
                "sub_dict_input": {
                    "sub_sub_string_input": "my_sub_sub_string",
                    "sub_sub_float_input": 111.1,
                    "sub_sub_int_input": 100,
                    "sub_sub_list_input": [100, 200, 300],
                    "sub_sub_bool_input": true,
                    "sub_nested_list_input": [[1, 2], [3, 4]],
                    "sub_nested_list_of_dict": [{
                        "int": 1,
                        "bool": false
                    },{
                        "float": 1.2,
                        "list": [1, 2]
                    }],
                    "sub_sub_empty_input": null
                    },
                "sub_empty_input": null
            },
            "bool_input": true,
            "empty_input": null
        }"""
        self.parameters = Parameters.create_from_input_stream(inputs_for_testing)

    def test_add_empty_value(self) -> None:
        """Tests the `add_empty_item` method.
        """
        self.parameters.add_empty_value("new_empty_item")

        with self.subTest():
            self.assertEqual("new_empty_item" in self.parameters.keys(), True)

            self.assertEqual(self.parameters["new_empty_item"].is_null(), True)

            self.assertEqual(self.parameters["new_empty_item"].is_sub_parameter(), False)

    def test_add_empty_value_nested(self) -> None:
        """Tests the `add_empty_item` method in nested `Parameters` objects.
        """
        self.parameters["dict_input"]["sub_dict_input"].add_empty_value("new_empty_item")

        with self.subTest():
            new_keys = self.parameters["dict_input"]["sub_dict_input"].keys()
            self.assertEqual("new_empty_item" in new_keys, True)

            actual_value = self.parameters["dict_input"]["sub_dict_input"].is_null()
            self.assertEqual(actual_value, True)

    def test_add_missing_parameters(self) -> None:
        """Tests the `add_missing_parameters` method.
        """
        default_parameters = Parameters.create_from_input_stream("""{
            "string_input": "my_string",
            "int_input": 1
            }""")

        new_parameters = Parameters.create_from_input_stream("""{
            "string_input": "my_string"
            }""")

        new_parameters.add_missing_parameters(default_parameters)

        with self.subTest():
            self.assertEqual("int_input" in new_parameters.keys(), True)

            self.assertEqual(new_parameters["int_input"].get_int(), 1)

    def test_add_missing_parameters_nested(self) -> None:
        """Tests the `add_missing_parameters` method.
        """
        default_parameters = Parameters.create_from_input_stream("""{
            "string": "my_string",
            "int": 1,
            "dict": {
                "sub_string": "my_string",
                "float": 11.1
                }
            }""")

        new_parameters = Parameters.create_from_input_stream("""{
            "string": "my_string",
            "dict": {
                "sub_string": "my_string"
                }
            }""")

        new_parameters["dict"].add_missing_parameters(default_parameters["dict"])

        with self.subTest():
            self.assertEqual("float" in new_parameters["dict"].keys(), True)

            self.assertEqual(new_parameters["dict"]["float"].get_double(), 11.1)

    def test_add_value(self) -> None:
        """Tests the `add_item` method.
        """
        self.parameters.add_value("new_item", 2)

        with self.subTest():
            self.assertEqual(self.parameters["new_item"].get_int(), 2)

            self.assertEqual("new_item" in self.parameters.keys(), True)

    def test_add_value_nested(self) -> None:
        """Tests the `add_item` method in nested `Parameters` objects.
        """
        self.parameters["dict_input"].add_value("new_item", False)

        with self.subTest():
            self.assertEqual(self.parameters["dict_input"]["new_item"].get_bool(), False)

            self.assertEqual("new_item" in self.parameters["dict_input"].keys(), True)

    def test_add_value_with_sub_parameters(self) -> None:
        """Tests the `add_value` method.
        """
        self.parameters.add_value("new_empty_item", """{}""")

        with self.subTest():
            self.assertEqual(self.parameters["new_empty_item"].is_sub_parameter(), False)

            self.assertEqual("new_empty_item" in self.parameters.keys(), True)

            self.parameters["new_empty_item"].add_value("string", "string")
            self.parameters["new_empty_item"].add_value("int", 1)

            self.assertEqual(self.parameters["new_empty_item"].is_sub_parameter(), True)

            self.assertEqual("string" in self.parameters["new_empty_item"].keys(), True)

            self.assertEqual(self.parameters["new_empty_item"]["int"].get_int(), 1)

    def test_create_empty_parameters_from_json(self) -> None:
        """Tests the creation of an empty `Parameters` from json file.

        See Also
        --------
        test_is_sub_parameter_with_empty_parameters
        """
        file_to_open = Path(__file__).parent / "test_empty_parameters.json"

        with open(file_to_open, 'r', encoding = "UTF-8") as parameter_file:
            parameters = Parameters.create_from_input_stream(parameter_file.read())

        self.assertEqual(parameters.is_sub_parameter(), False)

    def test_create_parameters_from_json(self) -> None:
        """Tests the creation of a `Parameters` from json file.
        """
        file_to_open = Path(__file__).parent / "test_parameters.json"

        with open(file_to_open, 'r', encoding = "UTF-8") as parameter_file:
            parameters = Parameters.create_from_input_stream(parameter_file.read())

        # check empty sub parameters
        with self.subTest():
            self.assertEqual(
                parameters["inputs"]["empty_sub_parameters"].is_sub_parameter(), False)

            self.assertEqual(parameters["inputs"]["int"].get_int(), 0)

            self.assertEqual(parameters["inputs"]["string"].get_string(), "string")

            self.assertEqual(parameters["inputs"]
                                       ["sub_parameters"]["bool"].get_bool(), False)

    def test_get_array(self) -> None:
        """Tests the `get_array` method.
        """
        first_value = self.parameters["list_input"].get_array()[0].get_int()
        second_value = self.parameters["list_input"].get_array()[1].get_int()
        third_value = self.parameters["list_input"].get_array()[2].get_int()
        self.assertEqual([first_value, second_value, third_value], [1, 2, 3])

    def test_get_array_nested(self) -> None:
        """Tests the `get_array` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            test_array = self.parameters["dict_input"]["sub_list_input"].get_array()
            first_value = test_array[0].get_int()
            second_value = test_array[1].get_int()
            third_value = test_array[2].get_int()
            self.assertEqual([first_value, second_value, third_value], [10, 20, 30])

            # test on the second level of nesting
            test_array = (self.parameters["dict_input"]
                                         ["sub_dict_input"]
                                         ["sub_sub_list_input"].get_array())
            first_value = test_array[0].get_int()
            second_value = test_array[1].get_int()
            third_value = test_array[2].get_int()
            self.assertEqual([first_value, second_value, third_value], [100, 200, 300])

    def test_get_bool(self) -> None:
        """Tests the `get_bool` method.
        """
        value = self.parameters["bool_input"].get_bool()
        self.assertEqual(value, True)

    def test_get_bool_nested(self) -> None:
        """Tests the `get_bool` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_bool_input"].get_bool()
            self.assertEqual(value, True)

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_bool_input"].get_bool())
            self.assertEqual(value, True)

    def test_get_double(self) -> None:
        """Tests the `get_double` method.
        """
        value = self.parameters["float_input"].get_double()
        self.assertEqual(value, 1.1)

    def test_get_double_nested(self) -> None:
        """Tests the `get_double` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_float_input"].get_double()
            self.assertEqual(value, 11.1)

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_float_input"].get_double())
            self.assertEqual(value, 111.1)

    def test_get_int(self) -> None:
        """Tests the `get_int` method.
        """
        value = self.parameters["int_input"].get_int()
        self.assertEqual(value, 1)

    def test_get_int_nested(self) -> None:
        """Tests the `get_int` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_int_input"].get_int()
            self.assertEqual(value, 10)

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_int_input"].get_int())
            self.assertEqual(value, 100)

    def test_get_string(self) -> None:
        """Tests the `get_string` method.
        """
        value = self.parameters["string_input"].get_string()
        self.assertEqual(value, "my_string")

    def test_get_string_nested(self) -> None:
        """Tests the `get_string` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_string_input"].get_string()
            self.assertEqual(value, "my_sub_string")

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_string_input"].get_string())
            self.assertEqual(value, "my_sub_sub_string")

    def test_is_array(self) -> None:
        """Tests the `is_array` method.
        """
        with self.subTest():
            # check positive is_array method
            is_array = self.parameters["list_input"].is_array()
            self.assertEqual(is_array, True)

            # check negative is_array method
            is_double = self.parameters["float_input"].is_array()
            self.assertEqual(is_double, False)

    def test_is_array_nested(self) -> None:
        """Tests the `is_array` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_list_input"].get_array()
            first_val = value[0].get_int()
            second_val = value[1].get_int()
            third_val = value[2].get_int()
            self.assertEqual([first_val, second_val, third_val], [10, 20, 30])

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_list_input"].get_array())
            first_val = value[0].get_int()
            second_val = value[1].get_int()
            third_val = value[2].get_int()
            self.assertEqual([first_val, second_val, third_val], [100, 200, 300])

    def test_is_bool(self) -> None:
        """Tests the `is_bool` method.
        """
        with self.subTest():
            # check positive is_bool method
            is_bool = self.parameters["bool_input"].is_bool()
            self.assertEqual(is_bool, True)

            # check negative is_bool method
            is_int = self.parameters["int_input"].is_bool()
            self.assertEqual(is_int, False)

    def test_is_bool_nested(self) -> None:
        """Tests the `is_bool` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_bool_input"].get_bool()
            self.assertEqual(value, True)

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_bool_input"].get_bool())
            self.assertEqual(value, True)

    def test_is_double(self) -> None:
        """Tests the `is_double` method.
        """
        with self.subTest():
            # check positive is_double method
            is_double = self.parameters["float_input"].is_double()
            self.assertEqual(is_double, True)

            # check negative is_double method
            is_int = self.parameters["int_input"].is_double()
            self.assertEqual(is_int, False)

    def test_is_double_nested(self) -> None:
        """Tests the `is_double` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_float_input"].get_double()
            self.assertEqual(value, 11.1)

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_float_input"].get_double())
            self.assertEqual(value, 111.1)

    def test_is_int(self) -> None:
        """Tests the `is_int` method.
        """
        with self.subTest():
            # check positive is_int method
            is_int = self.parameters["int_input"].is_int()
            self.assertEqual(is_int, True)

            # check negative is_int method
            is_double = self.parameters["float_input"].is_int()
            self.assertEqual(is_double, False)

    def test_is_int_nested(self) -> None:
        """Tests the `is_int` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_int_input"].get_int()
            self.assertEqual(value, 10)

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_int_input"].get_int())
            self.assertEqual(value, 100)

    def test_is_null(self) -> None:
        """Tests the `is_null` method.
        """
        self.assertEqual(self.parameters["empty_input"].is_null(), True)

    def test_is_null_nested(self) -> None:
        """Tests the `is_null` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_empty_input"].is_null()
            self.assertEqual(value, True)

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_empty_input"].is_null())
            self.assertEqual(value, True)

    def test_is_number(self) -> None:
        """Tests the `is_number` method.
        """
        with self.subTest():
            # check positive is_number method with float
            is_number = self.parameters["float_input"].is_number()
            self.assertEqual(is_number, True)

            # check positive is_number method with int
            is_number = self.parameters["int_input"].is_number()
            self.assertEqual(is_number, True)

            # check negative is_number method
            is_string = self.parameters["string_input"].is_number()
            self.assertEqual(is_string, False)

    def test_is_number_nested(self) -> None:
        """Tests the `is_number` method in nested `Parameters` objects..
        """
        with self.subTest():
            # check positive is_number method with float (first level of nesting)
            is_number = self.parameters["dict_input"]["sub_float_input"].is_number()
            self.assertEqual(is_number, True)

            # check positive is_number method with int (first level of nesting)
            is_number = self.parameters["dict_input"]["sub_int_input"].is_number()
            self.assertEqual(is_number, True)

            # check negative is_number method (first level of nesting)
            is_string = self.parameters["dict_input"]["sub_string_input"].is_number()
            self.assertEqual(is_string, False)

            # check positive is_number method with float (second level of nesting)
            is_number = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_sub_float_input"].is_number())
            self.assertEqual(is_number, True)

            # check positive is_number method with int (second level of nesting)
            is_number = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_sub_int_input"].is_number())
            self.assertEqual(is_number, True)

            # check negative is_number method (second level of nesting)
            is_string = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_sub_string_input"].is_number())
            self.assertEqual(is_string, False)

    def test_is_string(self) -> None:
        """Tests the `is_string` method.
        """
        with self.subTest():
            # check positive is_string method
            is_string = self.parameters["string_input"].is_string()
            self.assertEqual(is_string, True)

            # check negative is_string method
            is_double = self.parameters["float_input"].is_string()
            self.assertEqual(is_double, False)

    def test_is_string_nested(self) -> None:
        """Tests the `is_string` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            value = self.parameters["dict_input"]["sub_string_input"].get_string()
            self.assertEqual(value, "my_sub_string")

            # test on the second level of nesting
            value = (self.parameters["dict_input"]
                                    ["sub_dict_input"]
                                    ["sub_sub_string_input"].get_string())
            self.assertEqual(value, "my_sub_sub_string")

    def test_is_sub_parameter(self) -> None:
        """Tests the `_if_sub_parameter` method.
        """
        with self.subTest():
            self.assertEqual(self.parameters["dict_input"].is_sub_parameter(), True)

            self.assertEqual(self.parameters["int_input"].is_sub_parameter(), False)

    def test_is_sub_parameter_nested(self) -> None:
        """Tests the `_if_sub_parameter` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            self.assertEqual(self.parameters["dict_input"]
                                            ["sub_dict_input"].is_sub_parameter(), True)

            # test on the second level of nesting
            self.assertEqual(self.parameters["dict_input"]
                                            ["sub_int_input"].is_sub_parameter(), False)

    def test_is_sub_parameter_with_empty_parameters(self) -> None:
        """Tests `_if_sub_parameter` method in case of an empty `Parameters` object.

        See Also
        --------
        test_create_empty_parameters_from_json
        """
        empty_params = Parameters.create_from_input_stream("""{}""")

        self.assertEqual(empty_params.is_sub_parameter(), False)

    def test_items(self) -> None:
        """Tests the `items` method in `Parameters` objects.
        """
        expected_items = [("string_input", "my_string"),
                          ("float_input", 1.1),
                          ("int_input", 1),
                          ("list_input", [1, 2, 3]),
                          ("bool_input", True)]

        current_items = self.parameters.items()

        # checking all the items except nested Parameters, which is not possible.
        with self.subTest():
            self.assertEqual(expected_items[0][1], current_items[0][1].get_string())

            self.assertEqual(expected_items[1][1], current_items[1][1].get_double())

            self.assertEqual(expected_items[2][1], current_items[2][1].get_int())

            first_val = current_items[3][1].get_array()[0].get_int()
            second_val = current_items[3][1].get_array()[1].get_int()
            third_val = current_items[3][1].get_array()[2].get_int()
            self.assertEqual(expected_items[3][1], [first_val, second_val, third_val])

            self.assertEqual(expected_items[4][1], current_items[7][1].get_bool())

    def test_items_nested(self) -> None:
        """Tests the `items` method in nested `Parameters` objects.
        """
        # test on the first level of nesting
        expected_items = [("sub_string_input", "my_sub_string"),
                          ("sub_float_input", 11.1),
                          ("sub_int_input", 10),
                          ("sub_list_input", [10, 20, 30]),
                          ("sub_bool_input", True)]

        current_items = self.parameters["dict_input"].items()

        # checking all the items except nested Parameters, which is not possible.
        with self.subTest():
            self.assertEqual(expected_items[0][1], current_items[0][1].get_string())

            self.assertEqual(expected_items[1][1], current_items[1][1].get_double())

            self.assertEqual(expected_items[2][1], current_items[2][1].get_int())

            first_val = current_items[3][1].get_array()[0].get_int()
            second_val = current_items[3][1].get_array()[1].get_int()
            third_val = current_items[3][1].get_array()[2].get_int()
            self.assertEqual(expected_items[3][1], [first_val, second_val, third_val])

            self.assertEqual(expected_items[4][1], current_items[4][1].get_bool())

        # test on the second level of nesting
        expected_items = [("sub_sub_string_input", "my_sub_sub_string"),
                          ("sub_sub_float_input", 111.1),
                          ("sub_sub_int_input", 100),
                          ("sub_sub_list_input", [100, 200, 300]),
                          ("sub_sub_bool_input", True)]

        current_items = self.parameters["dict_input"]["sub_dict_input"].items()

        # checking all the items except nested Parameters, which is not possible.
        with self.subTest():
            self.assertEqual(expected_items[0][1], current_items[0][1].get_string())

            self.assertEqual(expected_items[1][1], current_items[1][1].get_double())

            self.assertEqual(expected_items[2][1], current_items[2][1].get_int())

            first_val = current_items[3][1].get_array()[0].get_int()
            second_val = current_items[3][1].get_array()[1].get_int()
            third_val = current_items[3][1].get_array()[2].get_int()
            self.assertEqual(expected_items[3][1], [first_val, second_val, third_val])

            self.assertEqual(expected_items[4][1], current_items[4][1].get_bool())

    def test_keys(self) -> None:
        """Tests the `keys` method.
        """
        keys = self.parameters.keys()
        expected_keys = (["string_input", "float_input", "int_input", "list_input",
                          "nested_list_input", "nested_list_of_dict", "dict_input",
                          "bool_input", "empty_input"])

        self.assertListEqual(keys, expected_keys)

    def test_keys_nested(self) -> None:
        """Tests the `keys` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            keys = self.parameters["dict_input"].keys()
            expected_keys = (["sub_string_input", "sub_float_input", "sub_int_input",
                              "sub_list_input", "sub_bool_input", "sub_dict_input",
                              "sub_empty_input"])

            self.assertListEqual(keys, expected_keys)

            # test on the second level of nesting
            keys = self.parameters["dict_input"]["sub_dict_input"].keys()
            expected_keys = (["sub_sub_string_input", "sub_sub_float_input",
                              "sub_sub_int_input", "sub_sub_list_input",
                              "sub_sub_bool_input", "sub_nested_list_input",
                              "sub_nested_list_of_dict", "sub_sub_empty_input"])

            self.assertListEqual(keys, expected_keys)

    def test_nested_list(self) -> None:
        """Tests the creation of the nested lists.
        """
        with self.subTest():
            sub_list = self.parameters["nested_list_input"].get_array()
            first_value = sub_list[1].get_array()[0].get_int()
            second_value = sub_list[1].get_array()[1].get_int()
            self.assertListEqual([first_value, second_value], [3, 4])

            sub_list = self.parameters["nested_list_input"].get_array()
            self.assertIsInstance(sub_list[1], Parameters)

            sub_param = self.parameters["nested_list_of_dict"].get_array()[1]
            first_value = sub_param["list"].get_array()[0].get_int()
            second_value = sub_param["list"].get_array()[1].get_int()
            self.assertListEqual([first_value, second_value], [1, 2])

            sub_param = self.parameters["nested_list_of_dict"].get_array()[1]
            self.assertIsInstance(sub_param, Parameters)

            sub_param = self.parameters["nested_list_of_dict"].get_array()[1]
            self.assertEqual(sub_param["float"].get_double(), 1.2)

            sub_param = self.parameters["nested_list_of_dict"].get_array()[1]
            self.assertEqual(sub_param["list"].get_array()[0].is_int(), True)

            sub_param = self.parameters["nested_list_of_dict"].get_array()[1]
            self.assertEqual(sub_param["float"].is_double(), True)

    def test_nested_list_in_nested_dict(self) -> None:
        """Tests the creation of the nested lists in nested `Parameters`.
        """
        with self.subTest():
            sub_list = (self.parameters["dict_input"]
                                       ["sub_dict_input"]
                                       ["sub_nested_list_input"].get_array())
            first_value = sub_list[1].get_array()[0].get_int()
            second_value = sub_list[1].get_array()[1].get_int()
            self.assertListEqual([first_value, second_value], [3, 4])

            sub_list = (self.parameters["dict_input"]
                                       ["sub_dict_input"]
                                       ["sub_nested_list_input"].get_array())
            self.assertEqual(sub_list[1].get_array()[1].is_int(), True)

            sub_list = (self.parameters["dict_input"]
                                       ["sub_dict_input"]
                                       ["sub_nested_list_input"].get_array())
            self.assertIsInstance(sub_list[1], Parameters)

            sub_param = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_nested_list_of_dict"].get_array()[1])
            first_value = sub_param["list"].get_array()[0].get_int()
            second_value = sub_param["list"].get_array()[1].get_int()
            self.assertListEqual([first_value, second_value], [1, 2])

            sub_param = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_nested_list_of_dict"].get_array()[1])
            self.assertEqual(sub_param["list"].get_array()[0].is_int(), True)

            sub_param = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_nested_list_of_dict"].get_array()[1])
            self.assertIsInstance(sub_param, Parameters)

    def test_null_entry_values(self) -> None:
        """Tests the addition of empty entry in the `validate_and_assign_default` method.
        """
        default_input = """{
            "int": 1,
            "empty": {}
        }"""

        new_input = """{
            "int": 1
        }"""

        default_param = Parameters.create_from_input_stream(default_input)
        param = Parameters.create_from_input_stream(new_input)
        param.validate_and_assign_defaults(default_param)

        with self.subTest():
            self.assertEqual(default_param["empty"].is_null(), True)

            self.assertEqual(type(param["empty"]), type(default_param["empty"]))

    def test_pretty_print_json_string(self) -> None:
        """Tests the `test_pretty_print_json_string` method.
        """
        with self.subTest():
            param = """{
                "string": "my_string",
                "float_input": 1.1,
                "dict_input": {
                    "sub_list_input": [10, 20, 30],
                    "sub_bool_input": true,
                    "sub_dict_input": {
                        "sub_sub_int_input": 100
                        }
                }
            }"""

            parameters = Parameters.create_from_input_stream(param)
            expected_string = ("{\n    \"string\": \"my_string\",\n    "
                               "\"float_input\": 1.1,\n    \"dict_input\": {\n        "
                               "\"sub_list_input\": [\n            10,\n            "
                               "20,\n            30\n        ],\n        "
                               "\"sub_bool_input\": "
                               "true,\n        \"sub_dict_input\": {\n            "
                               "\"sub_sub_int_input\": 100\n        }\n    }\n}")

            self.assertEqual(parameters.pretty_print_json_string(), expected_string)

            expected_str = ("{\n    \"string_input\": \"my_string\",\n    "
                            "\"float_input\": 1.1,\n    \"int_input\": 1,\n    "
                            "\"list_input\": [\n        1,\n        2,\n        3\n    ],"
                            "\n    \"nested_list_input\": [\n        [\n            1,\n"
                            "            2\n        ],\n        [\n            3,\n"
                            "            4\n        ]\n    ],\n    "
                            "\"nested_list_of_dict\": [\n        {\n            \"int\": "
                            "1,\n            \"bool\": false\n        },\n        "
                            "{\n            \"float\": 1.2,\n            \"list\": "
                            "[\n                1,\n                2\n            ]\n"
                            "        }\n    ],\n    \"dict_input\": {\n        "
                            "\"sub_string_input\": \"my_sub_string\",\n        "
                            "\"sub_float_input\": 11.1,\n        \"sub_int_input\": 10,\n"
                            "        \"sub_list_input\": [\n            10,\n            "
                            "20,\n            30\n        ],\n        \"sub_bool_input\":"
                            " true,\n        \"sub_dict_input\": {\n            "
                            "\"sub_sub_string_input\": \"my_sub_sub_string\",\n"
                            "            \"sub_sub_float_input\": 111.1,\n            "
                            "\"sub_sub_int_input\": 100,\n            "
                            "\"sub_sub_list_input\": [\n                100,\n"
                            "                200,\n                300\n            ],\n"
                            "            \"sub_sub_bool_input\": true,\n            "
                            "\"sub_nested_list_input\": [\n                [\n           "
                            "         1,\n                    2\n                ],\n    "
                            "            [\n                    3,\n                    "
                            "4\n                ]\n            ],\n            "
                            "\"sub_nested_list_of_dict\": [\n                {\n         "
                            "           \"int\": 1,\n                    \"bool\": "
                            "false\n                },\n                {\n              "
                            "      \"float\": 1.2,\n                    \"list\": [\n    "
                            "                    1,\n                        2\n         "
                            "           ]\n                }\n            ],\n           "
                            " \"sub_sub_empty_input\": null\n        },\n        "
                            "\"sub_empty_input\": null\n    },\n    \"bool_input\": true,"
                            "\n    \"empty_input\": null\n}")

            self.assertEqual(self.parameters.pretty_print_json_string(), expected_str)

    def test_recursively_validate_and_assign_defaults(self) -> None:
        """Tests the `recursively_validate_and_assign_defaults` method.
        """
        # These params are the almost the same defined in setUp, but without
        # sub_list_input and sub_sub_float_input.
        params = """{
            "string_input": "my_string",
            "float_input": 1.1,
            "int_input": 1,
            "list_input": [1, 2, 3],
            "dict_input": {
                "sub_string_input": "my_sub_string",
                "sub_float_input": 11.1,
                "sub_int_input": 10,
                "sub_bool_input": true,
                "sub_dict_input": {
                    "sub_sub_string_input": "my_sub_sub_string",
                    "sub_sub_int_input": 100,
                    "sub_sub_list_input": [100, 200, 300],
                    "sub_sub_bool_input": true,
                    "sub_sub_empty_input": null
                    },
                "sub_empty_input": null
            },
            "bool_input": true,
            "empty_input": null
        }"""

        # Using the self.parameters as default to avoid modification on other tests.
        new_params = Parameters.create_from_input_stream(params)
        new_params.recursively_validate_and_assign_defaults(self.parameters)

        with self.subTest():
            self.assertEqual("sub_list_input" in new_params["dict_input"].keys(), True)

            current_values = new_params["dict_input"]["sub_list_input"].get_array()
            first_value = current_values[0].get_int()
            second_value = current_values[1].get_int()
            third_value = current_values[2].get_int()
            self.assertEqual([first_value, second_value, third_value], [10, 20, 30])

            self.assertEqual("sub_sub_float_input" in
                             new_params["dict_input"]["sub_dict_input"].keys(), True)

            self.assertEqual(new_params["dict_input"]
                                       ["sub_dict_input"]
                                       ["sub_sub_float_input"].get_double(), 111.1)

    def test_remove_item(self) -> None:
        """Tests the `remove_item` method.
        """
        self.parameters.remove_item("string_input")

        self.assertEqual("string_input" in self.parameters.keys(), False)

    def test_remove_item_nested(self) -> None:
        """Tests the `remove_item` method in nested `Parameters` objects.
        """
        (self.parameters["dict_input"]
                        ["sub_dict_input"].remove_item("sub_sub_string_input"))
        new_keys = self.parameters["dict_input"]["sub_dict_input"].keys()

        self.assertEqual("sub_sub_string_input" in new_keys, False)

    def test_set_array(self) -> None:
        """Tests the `set_array` method.
        """
        self.parameters["list_input"].set_array([11, 22, 33, 44])
        new_value = self.parameters["list_input"].get_array()
        self.assertEqual(new_value, [11, 22, 33, 44])

    def test_set_array_nested(self) -> None:
        """Tests the `set_array` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            self.parameters["dict_input"]["sub_list_input"].set_array([11, 22, 33, 44])
            new_value = self.parameters["dict_input"]["sub_list_input"].get_array()
            self.assertEqual(new_value, [11, 22, 33, 44])

            # test on the second level of nesting
            (self.parameters["dict_input"]
                            ["sub_dict_input"]
                            ["sub_sub_list_input"].set_array([11, 22]))
            new_value = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_sub_list_input"].get_array())
            self.assertEqual(new_value, [11, 22])

    def test_set_bool(self) -> None:
        """Tests the `set_bool` method.
        """
        self.parameters["bool_input"].set_bool(False)
        new_value = self.parameters["bool_input"].get_bool()
        self.assertEqual(new_value, False)

    def test_set_bool_nested(self) -> None:
        """Tests the `set_bool` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            self.parameters["dict_input"]["sub_bool_input"].set_bool(False)
            new_value = self.parameters["dict_input"]["sub_bool_input"].get_bool()
            self.assertEqual(new_value, False)

            # test on the second level of nesting
            (self.parameters["dict_input"]
                            ["sub_dict_input"]
                            ["sub_sub_bool_input"].set_bool(False))
            new_value = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_sub_bool_input"].get_bool())
            self.assertEqual(new_value, False)

    def test_set_double(self) -> None:
        """Tests the `set_double` method.
        """
        self.parameters["float_input"].set_double(2.5)
        new_value = self.parameters["float_input"].get_double()
        self.assertEqual(new_value, 2.5)

    def test_set_double_nested(self) -> None:
        """Tests the `set_double` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            self.parameters["dict_input"]["sub_float_input"].set_double(0.22)
            new_value = self.parameters["dict_input"]["sub_float_input"].get_double()
            self.assertEqual(new_value, 0.22)

            # test on the second level of nesting
            (self.parameters["dict_input"]
                            ["sub_dict_input"]
                            ["sub_sub_float_input"].set_double(0.31))
            new_value = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_sub_float_input"].get_double())
            self.assertEqual(new_value, 0.31)

    def test_set_int(self) -> None:
        """Tests the `set_int` method.
        """
        self.parameters["int_input"].set_int(2)
        new_value = self.parameters["int_input"].get_int()
        self.assertEqual(new_value, 2)

    def test_set_int_nested(self) -> None:
        """Tests the `set_int` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            self.parameters["dict_input"]["sub_int_input"].set_int(23)
            new_value = self.parameters["dict_input"]["sub_int_input"].get_int()
            self.assertEqual(new_value, 23)

            # test on the second level of nesting
            (self.parameters["dict_input"]
                            ["sub_dict_input"]
                            ["sub_sub_int_input"].set_int(25))
            new_value = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_sub_int_input"].get_int())
            self.assertEqual(new_value, 25)

    def test_set_string(self) -> None:
        """Tests the `set_string` method.
        """
        self.parameters["string_input"].set_string("modified input string")
        new_value = self.parameters["string_input"].get_string()
        self.assertEqual(new_value, "modified input string")

    def test_set_string_nested(self) -> None:
        """Tests the `set_string` method in nested `Parameters` objects.
        """
        with self.subTest():
            # test on the first level of nesting
            self.parameters["dict_input"]["sub_string_input"].set_string("new_string")
            new_value = self.parameters["dict_input"]["sub_string_input"].get_string()
            self.assertEqual(new_value, "new_string")

            # test on the second level of nesting
            (self.parameters["dict_input"]
                            ["sub_dict_input"]
                            ["sub_sub_string_input"].set_string("new string"))
            new_value = (self.parameters["dict_input"]
                                        ["sub_dict_input"]
                                        ["sub_sub_string_input"].get_string())
            self.assertEqual(new_value, "new string")

    def test_size(self) -> None:
        """Tests the `size` method.
        """
        with self.subTest():
            self.assertEqual(self.parameters["list_input"].size(), 3)

            self.assertEqual(self.parameters["nested_list_input"].size(), 2)

    def test_size_nested(self) -> None:
        """Tests the `size` method in nested `Parameters` objects.
        """
        with self.subTest():
            self.assertEqual(self.parameters["dict_input"]
                                            ["sub_dict_input"]
                                            ["sub_sub_list_input"].size(), 3)

            self.assertEqual(self.parameters["dict_input"]
                                            ["sub_dict_input"]
                                            ["sub_nested_list_input"].size(), 2)

    def test_validate_and_assign_default(self) -> None:
        """Tests the `validate_and_assign_default` method.
        """
        # These params are the almost the same defined in setUp, but without bool_input
        params = """{
            "string_input": "my_string",
            "float_input": 1.1,
            "int_input": 1,
            "list_input": [1, 2, 3],
            "dict_input": {
                "sub_string_input": "my_sub_string",
                "sub_float_input": 11.1,
                "sub_int_input": 10,
                "sub_list_input": [10, 20, 30],
                "sub_bool_input": true,
                "sub_dict_input": {
                    "sub_sub_string_input": "my_sub_sub_string",
                    "sub_sub_float_input": 111.1,
                    "sub_sub_int_input": 100,
                    "sub_sub_list_input": [100, 200, 300],
                    "sub_sub_bool_input": true,
                    "sub_sub_empty_input": null
                    },
                "sub_empty_input": null
            },
            "empty_input": null
        }"""

        # Using the self.parameters as default to avoid modification on other tests.
        new_parameters = Parameters.create_from_input_stream(params)
        new_parameters.validate_and_assign_defaults(self.parameters)

        with self.subTest():
            self.assertEqual("bool_input" in new_parameters.keys(), True)

            self.assertEqual(new_parameters["bool_input"].get_bool(), True)

    def test_values(self) -> None:
        """Tests the `values` method.
        """
        current_values = self.parameters.values()

        with self.subTest():
            self.assertEqual(current_values[0].get_string(), "my_string")

            self.assertEqual(current_values[1].get_double(), 1.1)

            self.assertEqual(current_values[2].get_int(), 1)

            first_value = current_values[3].get_array()[0].get_int()
            second_value = current_values[3].get_array()[1].get_int()
            third_value = current_values[3].get_array()[2].get_int()
            self.assertEqual([first_value, second_value, third_value], [1, 2, 3])

            self.assertEqual(current_values[7].get_bool(), True)

    def test_values_nested(self) -> None:
        """Tests the `values` method in nested `Parameters` objects.
        """
        # check 1st level of nesting
        current_values = self.parameters["dict_input"].values()

        with self.subTest():
            self.assertEqual(current_values[0].get_string(), "my_sub_string")

            self.assertEqual(current_values[1].get_double(), 11.1)

            self.assertEqual(current_values[2].get_int(), 10)

            first_value = current_values[3].get_array()[0].get_int()
            second_value = current_values[3].get_array()[1].get_int()
            third_value = current_values[3].get_array()[2].get_int()
            self.assertEqual([first_value, second_value, third_value], [10, 20, 30])

            self.assertEqual(current_values[4].get_bool(), True)

            # check 2nd level of nesting
            current_values = self.parameters["dict_input"]["sub_dict_input"].values()

            self.assertEqual(current_values[0].get_string(), "my_sub_sub_string")

            self.assertEqual(current_values[1].get_double(), 111.1)

            self.assertEqual(current_values[2].get_int(), 100)

            first_value = current_values[3].get_array()[0].get_int()
            second_value = current_values[3].get_array()[1].get_int()
            third_value = current_values[3].get_array()[2].get_int()
            self.assertEqual([first_value, second_value, third_value], [100, 200, 300])

            self.assertEqual(current_values[4].get_bool(), True)
