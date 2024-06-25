from dataclasses import dataclass
from datetime import datetime


@dataclass
class IgAccount:
    """Instagram account data representation"""

    name: str
    username: str
    password: str
    email: str
    birth: datetime

    def export(self) -> dict:
        """Exports the account data to a dictionary

        Returns:
            dict: The account data
        """
        return {
            "name": self.name,
            "username": self.username,
            "password": self.password,
            "email": self.email,
            "birth": self.birth,
        }
