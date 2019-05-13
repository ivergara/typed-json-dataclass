# typed_json_dataclass
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4344420de20b4262a4912d81cb28d175)](https://www.codacy.com/app/abatilo/typed-json-dataclass?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=abatilo/typed-json-dataclass&amp;utm_campaign=Badge_Grade)
[![CircleCI](https://circleci.com/gh/abatilo/typed-json-dataclass.svg?style=svg)](https://circleci.com/gh/abatilo/typed-json-dataclass)
[![codecov](https://codecov.io/gh/abatilo/typed-json-dataclass/branch/master/graph/badge.svg)](https://codecov.io/gh/abatilo/typed-json-dataclass)
[![PyPI status](https://img.shields.io/pypi/status/typed_json_dataclass.svg)](https://pypi.python.org/pypi/typed_json_dataclass/)
[![PyPI version](https://badge.fury.io/py/typed-json-dataclass.svg)](https://badge.fury.io/py/typed-json-dataclass)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/typed-json-dataclass.svg)](https://pypi.python.org/pypi/typed-json-dataclass/)
[![MIT license](http://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)

`typed_json_dataclass` is a library that augments the Python3.7
[dataclass](https://docs.python.org/3/library/dataclasses.html) feature in two
major ways:
1. Add a way to recursively grab class dictionary definitions, thus making your
   dataclass JSON serializable
2. Add a light amount of type validation to your dataclasses, so that you can
   validate that the JSON you're being given matches the data types that you're
   expecting.

By expressing your data as dataclasses, and by having your incoming data
validated as it is received, you can easily implement the [Data Transfer Object
(DTO)](https://martinfowler.com/eaaCatalog/dataTransferObject.html) pattern in
your Python code.

This library can be thought of as a combination of
[attrs](https://github.com/python-attrs/attrs),
[cattrs](https://github.com/Tinche/cattrs), and
[marshamllow](https://github.com/marshmallow-code/marshmallow)

## Getting Started

Install the library from PyPI:
```
pip install typed_json_dataclass
```

Use the dataclass decorator just like normal, but add the `TypedJsonMixin` from
this library, to your class definition. This will add 4 new methods to all of your dataclasses:
1. from_dict()
```python
@classmethod
def from_dict(cls, raw_dict):
    """Given a python dict, create an instance of the implementing class.

    :raw_dict: A dictionary that represents the DTO to create
    :returns: Returns an instance of the DTO, instantiated via the dict
    """
```
2. from_json()
```python
@classmethod
def from_json(cls, raw_json):
    """Given a raw json string, create an instance of the implementing class.

    :raw_json: A json string that represents the DTO to create
    :returns: Returns an instance of the DTO, instantiated via the json
    """
```
3. to_dict()
```python
def to_dict(self, *, keep_none=False):
    """Express the DTO as a dictionary.

    :returns: Returns the instantiated DTO as a dictionary
    """
```
4. to_json()
```python
def to_json(self, *, keep_none=False):
    """Express the DTO as a json string.

    :returns: Returns the instantiated DTO as a json string
    """
```

## Examples

### Converting your dataclass to a JSON serializable format
```python
from typing import List
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin

@dataclass
class Person(TypedJsonMixin):
    name: str
    age: int

@dataclass
class Family(TypedJsonMixin):
    people: List[Person]

bob = Person(name='Bob', age=24)
alice = Person(name='Alice', age=32)
family = Family(people=[bob, alice])

print(family.to_json())
# => {"people": [{"name": "Bob", "age": 24}, {"name": "Alice", "age": 32}]}
```


If your data doesn't match the type definitions, you'll get a helpful error:
```python
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin

@dataclass
class Person(TypedJsonMixin):
    name: str
    age: int

request_data = '{"name":"Bob","age":"24"}'

bob = Person.from_json(request_data)
# => TypeError: Person.age is expected to be <class 'int'>, but value 24 with type <class 'str'> was found instead
```

And you can parse data from a Python `dict` as well. Just use the `.from_dict()` function instead:
```python
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin

@dataclass
class Person(TypedJsonMixin):
    name: str
    age: int

request_data_as_dict = {
    'name': 'Alice',
    'age': '32'
}

alice = Person.from_dict(request_data_as_dict)
# => TypeError: Person.age is expected to be <class 'int'>, but value 32 with type <class 'str'> was found instead
```

### Setting a mapping_mode for auto mapping
```python
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin, MappingMode

@dataclass
class Person(TypedJsonMixin):
    person_name: str
    person_age: int

request_data_as_dict = {
    'personName': 'Alice',
    'personAge': 32
}

alice = Person.from_dict(request_data_as_dict, mapping_mode=MappingMode.SnakeCase)
# => Person(person_name='Alice', person_age=32)
```

This mapping mode is useful for when you get requests that have the JSON in a
camel case format, but you want your objects to be snake case and stay PEP8
compliant.

### Custom mapping (WIP)
It's possible that the source of the data and the field names of the dataclass don't map directly. For example, after a refactoring, old source data can follow a different naming and changing the source might prove unpractical. Another case could be that you need to move between (human) languages.

In this case, you can provide a custom dictionary to the mathods provided by the mixin class that maps the dataclass field names to the field names in the source.

```python
from dataclasses import dataclass
from typed_json_dataclass import TypedJsonMixin, MappingMode

@dataclass
class Person(TypedJsonMixin):
    name: str
    age: int

request_data_as_dict = {
    'nombre': 'Alice',
    'edad': 32
}

alice = Person.from_dict(request_data_as_dict, mapping={'name': 'nombre', 'age': 'edad'})
# => Person(name='Alice', age=32)
```

It is not necessary that every field name is given, only those provided will be modified. Currently it doesn't work for recursively defined dataclasses and it does not do any kind of validation that the given dataclass fields exists or not.


## Changelog

0.1.1 - Sun, 2018-12-30
* Correct some lazy tests

0.1.0 - Sun, 2018-12-30
* We now support recursive ForwardRef type definitions

0.0.2 - Sun, 2018-12-30
* Added several open source project badges.
* Added much more useful information to the README.
* No code/functionality changes.

0.0.1 - Sun, 2018-12-30
* Created the base project and uploaded it to PyPI. Not much additional work has
been done.
