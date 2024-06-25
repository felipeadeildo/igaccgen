from typing import Optional

from src.utils import get_email_agent

from .account import IgAccount


class InstagramClient:
    """Instagram client to be used for account generation"""

    def __init__(self, config: dict):
        """Initialize the client

        Args:
            config (dict): The config to be used
        """
        # TODO: create a httpx client instance with proxy and base_url to instagram api endpoint
        self.config = config
        self.email_agent = get_email_agent(config)

    def generate_account(self) -> Optional[IgAccount]:
        """Generates an account using the config with fake data

        Returns:
            IgAccount: The generated account
            None: If some error occurred
        """
        # TODO: call fake data generator (scrap from some website) and the fake data must generate an email too (from somesite like 10minutemail)
        ...
