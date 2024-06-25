import os
import random

from src.shared import USER_AGENTS
from src.utils.constants import CLEAR_SCREEN_CMD


def clear_screen():
    """Clears the screen"""
    os.system(CLEAR_SCREEN_CMD)


def get_random_user_agent() -> str:
    """Get a random user agent

    Returns:
        str: The random user agent
    """
    return random.choice(USER_AGENTS)
