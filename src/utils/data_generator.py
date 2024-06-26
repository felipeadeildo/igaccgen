from src.email_agent.base import EmailAgent
from src.email_agent.constants import EMAIL_AGENTS
from src.faker.base import FakePersonGenerator
from src.faker.constants import FAKER_GENERATORS


def get_email_agent(config: dict) -> EmailAgent:
    """Gets a random email agent to receive the confirmation email code.

    Returns:
        EmailAgent: The email agent instance
    """
    email_agent = config.get("email_agent", "10minutemail")
    return EMAIL_AGENTS[email_agent](config)


def get_fake_person_generator(config: dict) -> FakePersonGenerator:
    """Gets a random fake person generator

    Args:
        config (dict): The config to be used

    Returns:
        FakePersonGenerator: The fake person generator instance
    """
    fake_person_generator = config.get("fake_person_generator", "fake_name_generator")
    return FAKER_GENERATORS[fake_person_generator](config)
