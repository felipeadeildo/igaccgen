from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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


class InstagramClient:
    """Instagram client to be used for account generation"""

    def __init__(self, config: dict):
        """Initialize the client

        Args:
            config (dict): The config to be used
        """
        # TODO: create a httpx client instance with proxy and base_url to instagram api endpoint
        self.config = config

    def generate_account(self) -> Optional[IgAccount]:
        """Generates an account using the config with fake data

        Returns:
            IgAccount: The generated account
            None: If some error occurred
        """

        # TODO: call fake data generator (scrap from some website) and the fake data must generate an email too (from somesite like 10minutemail)
        ...
