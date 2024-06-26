from abc import ABC, abstractmethod

from src.faker.person import Person


class FakePersonGenerator(ABC):
    """Base class for fake people generator"""

    def __init__(self, config: dict) -> None:
        """Initialize the fake person generator

        Args:
            config (dict): The config to be used
        """
        self.config = config

    @abstractmethod
    def generate_person(self) -> Person:
        """Generates a person using the provider set in the config

        Returns:
            Person: The generated person
        """
