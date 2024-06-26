from typing import Literal, Mapping

from .base import FakePersonGenerator
from .fake_name_generator import FakeNameGenerator

FAKER_GENERATORS: Mapping[Literal["fake_name_generator"], type[FakePersonGenerator]] = {
    "fake_name_generator": FakeNameGenerator
}
"""List of fake person generators"""
