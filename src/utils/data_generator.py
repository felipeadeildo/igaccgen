from src.email_agent.base import EmailAgent
from src.email_agent.constants import EMAIL_AGENTS


def get_email_agent(config: dict) -> EmailAgent:
    """Gets a random email agent to receive the confirmation email code.

    Returns:
        EmailAgent: The email agent instance
    """
    email_agent = config.get("email_agent", "10minutemail")
    return EMAIL_AGENTS[email_agent](config)
