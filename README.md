# Studio W developments: _Core Package_

This is the core package of the _Studio W Engineers_ developments.
It provides classes and functions to be used across all the other developments. Changes in
this package affect all the dependent applications.

## Data Types - MutableString
The `MutableString` class represents a mutable string object.

This class mimics a Python string object, but being mutable at the same time. It stores the content of the string and provides some of the methods that the original Python `str` class provides.

## Parameters
This module aims at defining and managing a `Parameters` data structure for I/O based on the standard of `JSON`.

It provides methods to:
- access, check and set the content of each elemental parameter;
- complete check (keys and type) of hardcoded default parameters;
- add missing parameters when comparing to hardcoded default parameters.

Currently, despite a quite extended test suite, it is in alpha release since the code is not really readable and therefore difficult to maintain, safely use and imnprove.

An example of something (maybe) similar can be found here: https://github.com/edelooff/sqlalchemy-json/tree/master/sqlalchemy_json
