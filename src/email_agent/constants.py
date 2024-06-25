from typing import Literal, Mapping

from src.email_agent.base import EmailAgent
from src.email_agent.ten_min_mail import TenMinEmail

EMAIL_AGENTS: Mapping[Literal["10minemail"], type[EmailAgent]] = {
    "10minemail": TenMinEmail
}
"""List of email agents to generate emails and receive confirmation codes"""
