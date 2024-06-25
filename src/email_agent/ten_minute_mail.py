import json
from typing import Optional

import httpx
from src.email_agent.base import EmailAgent
from src.utils.common import get_random_user_agent


class TenMinuteMail(EmailAgent):
    """10MinuteMail.com email agent"""

    def generate_email(self) -> Optional[str]:
        """Generates an email using the config with fake data

        Returns:
            str: The generated email
            None: If some error occurred
        """
        self.session = httpx.Client(
            base_url="https://web2.10minutemail.com",
            headers={
                "User-Agent": get_random_user_agent(),
                "Content-Type": "application/json",
            },
        )

        res = self.session.post("/mailbox")
        try:
            data = res.json()
        except json.decoder.JSONDecodeError:
            return None

        self.session.headers["Authorization"] = f"Bearer {data['token']}"

        self.email = data["email"]

        return self.email

    def get_code_confirmation(self) -> Optional[str]:
        """Get the received code confirmation

        Returns:
            Optional[str]: The received code
            None: If the code was not received
        """
        messages = self.session.get("/messages").json()["messages"]

        # TODO: rewrite this to parse a real case of a instagram signup sent code.
        return next(
            (
                message["body"]
                for message in messages
                if "Confirm" in message["subject"]
            ),
            None,
        )
