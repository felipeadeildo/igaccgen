from abc import ABC, abstractmethod
from typing import Optional


class EmailAgent(ABC):
    """Base class for email agents"""

    def __init__(self, config: dict):
        """Initialize the email agent

        Args:
            config (dict): The config to be used
        """
        self.config = config
        self._email: Optional[str] = None

    @property
    def email(self) -> str:
        """Get the generated email

        Raises:
            ValueError: If the email was not generated

        Returns:
            str: The generated email
        """
        if self._email is None:
            raise ValueError("Email not generated")
        return self._email

    @email.setter
    def email(self, value: str):
        self._email = value

    @abstractmethod
    def generate_email(self) -> Optional[str]:
        """Generates an email using the config with fake data

        Returns:
            str: The generated email
            None: If some error occurred
        """
        ...

    @abstractmethod
    def get_code_confirmation(self) -> Optional[str]:
        """Get the received code confirmation

        Returns:
            Optional[str]: The received code
            None: If the code was not received
        """
