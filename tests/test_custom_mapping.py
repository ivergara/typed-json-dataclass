from dataclasses import dataclass

import pytest
from typed_json_dataclass import TypedJsonMixin


@dataclass
class Book(TypedJsonMixin):
    title: str
    author: str


def test_custom_map_all_fields_from_dict():
    original = {'titulo': 'Some Book', 'autor': 'Me'}
    expected_object = Book('Some Book', 'Me')
    assert Book.from_dict(
            original,
            mapping={'title': 'titulo', 'author': 'autor'}) == expected_object


def test_custom_map_one_field_from_dict():
    original = {'title': 'Some Book', 'autor': 'Me'}
    expected_object = Book('Some Book', 'Me')
    assert Book.from_dict(
            original,
            mapping={'author': 'autor'}) == expected_object


def test_custom_map_all_fields_to_dict():
    expected = {'titulo': 'Some Book', 'autor': 'Me'}

    target = Book('Some Book', 'Me')
    actual = target.to_dict(mapping={'title': 'titulo', 'author': 'autor'})
    assert expected == actual


def test_custom_map_one_fields_to_dict():
    expected = {'title': 'Some Book', 'autor': 'Me'}

    target = Book('Some Book', 'Me')
    actual = target.to_dict(mapping={'author': 'autor'})
    assert expected == actual
