from dataclasses import dataclass
from datetime import datetime


@dataclass
class Person:
    """Person data representation"""

    first_name: str
    last_name: str
    birthday: datetime
    username: str
    password: str
