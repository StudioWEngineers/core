"""
Parameters
----------

This module aims at defining and managing a `Parameters` data structure for I/O based on
the standard of JSON.

It provides methods to:
    - access, check and set the content of each elemental parameter;
    - complete check (keys and type) of hardcoded default parameters;
    - add missing parameters when comparing to hardcoded default parameters.

__author__ = "Studio W Engineers"

__version__ = "0.0.0"

__maintainer__ = "Studio W Engineers"

__email__ = "studio.w.engineers@gmail.com"

__status__ "Release"
"""
# standard library imports
from json import dumps, loads
from typing import Any

# third party library imports

# local library specific imports


class Parameters:
    """A class that aims at managing the parameters needed to run any type of analysis.
    """
    def __init__(self) -> None:
        """The initializer of the `Parameters` class. This magic method is NOT intended to
        be the default construtor, that is, the `create_from_input_string` method.
        """
        # Contains the elemental Parameters and it's empty if the Parameters is elemental.
        self.params: dict[str, Parameters] = {}

        # Contain the value and the type of an elemental Parameters.
        self.val: bool | float | list[Parameters] | int | None | str = None

    def __getitem__(self, key: str) -> "Parameters":
        """Returns a `Parameters` instance with the given key.
        """
        if not self.has(key):
            err_msg = f"Provided a key that does not exist. Entry string: \"{key}\"."
            raise KeyError(err_msg)

        return self.params[key]

    def __repr__(self) -> str:
        """Returns a string equivalent to the `Parameters` object.
        """
        return "Parameters object with content:\n" + self.pretty_print_json_string()

    def add_empty_value(self, key: str) -> None:
        """Adds an empty `Parameters` with the given key.
        """
        if not isinstance(key, str):
            err_msg = f"\"Parameters\" keys must be a string, provided \"{type(key)}\"."
            raise TypeError(err_msg)

        if self.has(key):
            warn_msg = f"Key \"{key}\" already exists and it will be overwritten!"
            print("Parameters" + warn_msg)

        self.params.update({key: Parameters._create_base_parameters(None)})

    def add_value(self,
                  key: str,
                  val: bool | float | list["Parameters"] | int | None | str) -> None:
        """Adds an item to an existing `Parameters` with the provided `key` and `val`.
        """
        if not isinstance(key, str):
            err_msg = f"\"Parameters\" keys must be a string, provided \"{type(key)}\"."
            raise TypeError(err_msg)

        if self.has(key):
            warn_msg = f"Key \"{key}\" already exists and it will be overwritten!"
            print("Parameters" + warn_msg)

        self.params.update({key: Parameters._create_base_parameters(val)})

    def add_missing_parameters(self, default_param: "Parameters") -> None:
        """Adds missing items (if any) to an existing `Parameters` comparing its keys with
        the ones of the provided `default_param`.
        """
        if not isinstance(default_param, Parameters):
            err_msg = (f"\"default_param\" input must be a Parameters object, "
                       f"provided of type \"{type(default_param)}\".")
            raise TypeError(err_msg)

        for key, val in default_param.items():
            if not self.has(key):
                self.add_value(key, val.val)

    def get_array(self) -> list["Parameters"]:
        """Returns the content if of type `list`, raises a `TypeError` otherwise.
        """
        return self._get(self.is_array(), "list")  # type: ignore

    def get_bool(self) -> bool:
        """Returns the content if of type `bool`, raises a `TypeError` otherwise.
        """
        return self._get(self.is_bool(), "bool")  # type: ignore

    def get_double(self) -> float:
        """Returns the content if of type `float`, returns a cast to `float` if of type
        `int`, raises a `TypeError` otherwise.
        """
        try:
            return self._get(self.is_double(), "number")  # type: ignore

        # This mimics Kratos behaviour, casting int values to float.
        except TypeError:
            return float(self._get(self.is_int(), "number"))  # type: ignore

    def get_int(self) -> int:
        """Returns the content if of type `int`, raises a `TypeError` otherwise.
        """
        return self._get(self.is_int(), "number")  # type: ignore

    def get_string(self) -> str:
        """Returns the content if of type `str`, raises a `TypeError` otherwise.
        """
        return self._get(self.is_string(), "string")  # type: ignore

    def has(self, key: str) -> bool:
        """Returns `True` if the given key is in `self.params`, `False` otherwise.
        """
        return key in self.params.keys()

    def is_array(self) -> bool:
        """Returns `True` if the content is of type `list`, `False` otherwise.
        """
        return isinstance(self.val, list)

    def is_bool(self) -> bool:
        """Returns `True` if the content is of type `bool`, `False` otherwise.
        """
        return isinstance(self.val, bool)

    def is_double(self) -> bool:
        """Returns `True` if the content is of type `float`, `False` otherwise.
        """
        return isinstance(self.val, float)

    def is_int(self) -> bool:
        """Returns `True` if the content is of type `int`, `False` otherwise.
        """
        return isinstance(self.val, int)

    def is_null(self) -> bool:
        """Returns `True` if the content is of type `NoneType`, `False` otherwise.
        """
        return self.val is None

    def is_number(self) -> bool:
        """Returns `True` if the content is of type `bool` or `int`, `False` otherwise.
        """
        return self.is_int() or self.is_double()

    def is_string(self) -> bool:
        """Returns `True` if the content is of type `str`, `False` otherwise.
        """
        return isinstance(self.val, str)

    def items(self) -> list[tuple[str, "Parameters"]]:
        """Returns the items of the current `Parameters`.
        """
        self._check_if_sub_parameter("items")

        return [_ for _ in zip(self.keys(), self.values())]

    def keys(self) -> list[str]:
        """Returns the keys of the current `Parameters`.
        """
        self._check_if_sub_parameter("keys")

        return list(self.params.keys())

    def pretty_print_json_string(self) -> str:
        """This method returns a string equivalent to the `Parameters` object and the
        *.json file. It considers tabulations.
        """
        return dumps(self._serialize(self.params), indent=4)

    def recursively_validate_and_assign_defaults(self, defaults: "Parameters") -> None:
        """Recursive call of the `validate_and_assign_defaults` method.
        """
        self.validate_and_assign_defaults(defaults, recursive=True)

    def remove_item(self, key: str) -> None:
        """Removes the item with given key from `Parameters`.
        """
        if not isinstance(key, str):
            err_msg = f"`Parameters` keys must be a string, provided \"{type(key)}\"."
            raise TypeError(err_msg)

        if not self.has(key):
            err_msg = f"Key \"{key}\" does not exist and cannot be removed!"
            raise KeyError(err_msg)

        self.params.pop(key)

    def set_array(self, val: list[Any]) -> None:
        """Sets the content if of type `list`, raises a `TypeError` otherwise.
        """
        if not isinstance(val, list):
            err_msg = f"Expected a list, got a \"{type(val)}\"."
            raise TypeError(err_msg)

        self._set(val)

    def set_bool(self, val: bool) -> None:
        """Sets the content if of type `bool`, raises a `TypeError` otherwise.
        """
        if not isinstance(val, bool):
            err_msg = f"Expected a bool, got a \"{type(val)}\"."
            raise TypeError(err_msg)

        self._set(val)

    def set_double(self, val: float) -> None:
        """Sets the content if of type `floar`, raises a `TypeError` otherwise.
        """
        if not isinstance(val, float):
            err_msg = f"Expected a float, got a \"{type(val)}\"."
            raise TypeError(err_msg)

        self._set(val)

    def set_int(self, val: int) -> None:
        """Sets the content if of type `int`, raises a `TypeError` otherwise.
        """
        if not isinstance(val, int):
            err_msg = f"Expected an int, got a \"{type(val)}\"."
            raise TypeError(err_msg)

        self._set(val)

    def set_string(self, val: str) -> None:
        """Sets the content if of type `str`, raises a `TypeError` otherwise.
        """
        if not isinstance(val, str):
            err_msg = f"Expected a str, got a \"{type(val)}\"."
            raise TypeError(err_msg)

        self._set(val)

    def size(self) -> int:
        """Returns the length of the array.
        """
        if not self.is_array():
            err_msg = f"\"size\" method works only with arrays! Got \"{type(self.val)}\"!"
            raise TypeError(err_msg)

        return len(self.get_array())

    def validate_and_assign_defaults(self,
                                     defaults: "Parameters",
                                     recursive: bool = False) -> None:
        """Validate the current `Parameters` object against the provided defaults.

        Raises
        -------
            KeyError: if a key exists in the current `Parameters`, but not in the defaults

        Notes
        -----
            Adds a pair key, value if a default is missing in the current Parameters.
        """
        if not isinstance(defaults, Parameters):
            error_msg = (f"\"defaults\" input is expected to be provided as an instance"
                         f" of the \"Parameters\" class,"
                         f" and not of type {type(defaults)}.")
            raise TypeError(error_msg)

        for key in self.keys():
            # check if all the keys also exists in the defaults
            if not defaults.has(key):
                err_msg = (f"Item with key \"{key}\" is present in this "
                           f"settings, but NOT in the defaults! "
                           f"Current settings are:\n"
                           f"{self.pretty_print_json_string()}\n"
                           f"Current defaults are:\n"
                           f"{defaults.pretty_print_json_string()}")
                raise RuntimeError(err_msg)

            # check if the type is the same in the defaults
            if isinstance(type(self.params[key]), type(defaults[key])):
                err_msg = (f"The item with key \"{key}\" is of type "
                           f"\"{type(self.params[key])}\" in this settings,"
                           f" but in the defaults is of type "
                           f"\"{type(defaults[key])}\". "
                           f"Current settings are:\n"
                           f"{self.pretty_print_json_string()}\n"
                           f"Current defaults are:\n"
                           f"{defaults.pretty_print_json_string()}")
                raise RuntimeError(err_msg)

        # loop the over the defaults and add the missing entries, if any
        for key_d, val_d in defaults.items():

            # add the default in case the setting is not present
            if not self.has(key_d):
                self.add_value(key_d, val_d.val)

            elif recursive and val_d.is_sub_parameter():
                self.params[key_d].recursively_validate_and_assign_defaults(val_d)

    def values(self) -> list["Parameters"]:
        """Returns the values of the current `Parameters`.
        """
        if not isinstance(self, Parameters):
            err_msg = ("Input is not of type \"Parameters\", but of type \""
                       f"{self.__class__.__name__}\" from module \"{self.__module__}\"!")
            raise TypeError(err_msg)

        return [_ for _ in self.params.values()]

    def _check_if_sub_parameter(self, fct_name: str) -> None:
        """Checks if the provided input is an instance of the `Parameters` class and if
        the corresponding `self.params` is not empty.

        Raises
        ------
        TypeError if the provided input is not of a `Parameters` type or if it is an
        elemental `Parameters`.
        """
        if not self.is_sub_parameter():
            err_msg = (f"\"{fct_name}\" can only be used if the value is of "
                       "\"Parameter\" type.")
            raise TypeError(err_msg)

    def _get(self,
             cmp_fct: bool,
             exp_type_str: str) -> bool | float | list["Parameters"] | int | None | str:
        """Performs type check and returns the content if the type matches.
        """
        if not cmp_fct:
            raise TypeError(f"Argument must be a {exp_type_str}!")

        return self.val

    def is_sub_parameter(self) -> bool:
        """Checks if the provided input is an instance of the `Parameters` class and if
        the corresponding `self.params` is not empty.
        """
        return isinstance(self, Parameters) and bool(self.params)

    def _set(self, val: bool | float | list["Parameters"] | int | None | str) -> None:
        """Sets the content of an elemental `Parameters`.
        """
        self.val = val

    @classmethod
    def create_from_input_stream(cls, input_stream: str) -> "Parameters":
        """The public constructor of the `Parameters` class.
        """
        if not isinstance(input_stream, str):
            err_msg = (f"\"input_stream\" is expected to be a \"str\" object instead of "
                       f"\"{type(input_stream)}\".")
            raise TypeError(err_msg)

        # Empty strings are not allowed as they lead to error when using json.loads()
        if not input_stream:
            err_msg = "\"Parameters\" cannot be constructed from empty string!"
            raise TypeError(err_msg)

        parameters = loads(input_stream)
        if not isinstance(parameters, dict):
            warn_msg = "The provided input stream is empty and so the Parameters object."
            print("Parameters" + warn_msg)

        obj = cls()
        obj.params = obj._create_dict_parameters(parameters)

        return obj

    @classmethod
    def _create_array_parameters(cls, value: list[Any]) -> "Parameters":
        """A private constructor of the `Parameters` class. It creates a `Parameters`
        object from a `list`.
        """
        if not all(isinstance(_, (bool, dict, float, int, list, str)) for _ in value):
            err_msg = "Lists must be homogeneous in this context. Check your input data."
            raise TypeError(err_msg)

        list_of_param = []
        for item in value:
            if isinstance(item, dict):
                new_result = Parameters._create_dict_parameters(item)
                list_of_param.append(Parameters._from_parameters(new_result))

            elif isinstance(item, list):
                list_of_param.append(Parameters._create_array_parameters(item))

            else:
                list_of_param.append(Parameters._create_base_parameters(item))

        obj = cls()
        obj.val = list_of_param

        return obj

    @classmethod
    def _create_base_parameters(
        cls,
        val: bool | float | list["Parameters"] | int | None | str
    ) -> "Parameters":
        """A private constructor of the `Parameters` class. It is used only when elemental
        `Parameters` are to be created.
        """
        obj = cls()
        obj.val = val

        return obj

    @classmethod
    def _from_parameters(cls, content: dict[str, "Parameters"]) -> "Parameters":
        """A private constructor of the `Parameters` class. It is used only when nested
        `Parameters` are to be created.
        """
        if not isinstance(content, dict):
            err_msg = f"Input must be of type \"dict\", provided of type {type(content)}."
            raise TypeError(err_msg)

        obj = cls()
        obj.params = content

        return obj

    @staticmethod
    def _create_dict_parameters(data: dict[str, Any]) -> dict[str, "Parameters"]:
        """A private constructor of the `Parameters` class. It fills the `params`
        dictionary with keys taken from input stream and `Parameters` objects having
        values from the same input stream.
        """
        result = {}
        for key, value in data.items():
            if isinstance(value, (bool, float, int, str, type(None))):
                result.update({key: Parameters._create_base_parameters(value)})

            elif isinstance(value, dict):
                new_result = Parameters._create_dict_parameters(data[key])
                result.update({key: Parameters._from_parameters(new_result)})

            elif isinstance(value, list):
                result.update({key: Parameters._create_array_parameters(value)})

            else:
                err_msg = ("\"Parameters\" object accepts values of type \"bool\", "
                           "\"dict\", \"float\", \"int\", \"list\", \"NoneType\" or "
                           f"\"str\". Provided of type \"{type(value)}\".")
                raise TypeError(err_msg)

        return result

    @staticmethod
    def _serialize(parameter: dict[str, "Parameters"]) -> dict[str, str | list[str]]:
        """
        """
        serialized_param: dict[str, str | list[str]] = {}
        for key, value in parameter.items():
            if isinstance(value.val, (bool | float | int | None | str)):
                serialized_param.update({key: str(value.val)})

            elif isinstance(value.val, list):
                serialized_param.update({key: Parameters._serialize_array(value.val)})

            elif isinstance(value.val, dict):
                serialized_param.update({key: Parameters._serialize({key: value.val})})

        return serialized_param

    @staticmethod
    def _serialize_array(list_of_parameters: list["Parameters"]) -> list[str]:
        """
        """
        serialized_list = []
        for item in list_of_parameters:
            if isinstance(item.val, ( bool | float | int | None | str)):
                serialized_list.append(str(item.val))

            elif isinstance(item.val, list):
                serialized_list = Parameters._serialize_array(item.val)

            else:
                raise TypeError

        return serialized_list
