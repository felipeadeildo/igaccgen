from typing import Literal, Mapping

from src.email_agent.base import EmailAgent
from src.email_agent.ten_minute_mail import TenMinuteMail


EMAIL_AGENTS: Mapping[Literal["10minutemail"], type[EmailAgent]] = {
    "10minutemail": TenMinuteMail
}
"""List of email agents to generate emails and receive confirmation codes"""
