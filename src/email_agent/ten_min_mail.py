import json
from typing import Optional

import httpx

from src.email_agent.base import EmailAgent
from src.utils.common import get_random_user_agent


class TenMinEmail(EmailAgent):
    """10minemail.com email agent"""

    def generate_email(self) -> Optional[str]:
        """Generates an email using the config with fake data

        Returns:
            str: The generated email
            None: If some error occurred
        """
        self.session = httpx.Client(
            base_url="https://web2.10minemail.com",
            headers={
                "User-Agent": get_random_user_agent(),
                "Content-Type": "application/json",
                "Referer": "https://10minemail.com",
            },
        )

        res = self.session.post("/mailbox")
        try:
            data = res.json()
        except json.decoder.JSONDecodeError:
            return None

        self.session.headers["Authorization"] = f"Bearer {data['token']}"

        self.email = data["mailbox"]

        return self.email

    def get_code_confirmation(self) -> Optional[str]:
        """Get the received code confirmation

        Returns:
            Optional[str]: The received code
            None: If the code was not received
        """
        messages = self.session.get("/messages").json()["messages"]

        message_code_subject = next(
            (
                message["subject"]
                for message in messages
                if "instagram" in message["from"].lower()
            ),
            None,
        )
        if message_code_subject is None:
            return None

        # The subject follows this pattern: "123456 is your Instagram code"
        return message_code_subject.split(maxsplit=1)[0]
