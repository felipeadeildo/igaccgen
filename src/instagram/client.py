import random
import time
from datetime import datetime
from typing import Optional

import httpx
from icecream import ic

from src.instagram.constants import INSTAGRAM_APP_ID, INSTGARAM_ASBD_ID, SIGNUP_PAGE
from src.utils import get_email_agent
from src.utils.common import get_random_user_agent
from src.utils.data_generator import get_fake_person_generator
from src.utils.proxy import get_random_proxy

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
        self.person_generator = get_fake_person_generator(config)

    def generate_account(self) -> Optional[IgAccount]:
        """Generates an account using the config with fake data

        Returns:
            IgAccount: The generated account
            None: If some error occurred
        """
        self.person = self.person_generator.generate_person()
        self.email = self.email_agent.generate_email()
        if self.email is None:
            raise ValueError("Email was not generated")

        steps = [
            self.__create_session,
            self.__send_signup_request,
            self.__send_birth_date_request,
            self.__send_verify_email_request,
            self.__check_confirmation_code,
            self.__finish_signup,
        ]

        for step in steps:
            time.sleep(random.randint(1, 5))
            step()

        return IgAccount(
            name=self.person.first_name,
            username=self.person.username,
            email=self.email,
            password=self.person.password,
            birth=self.person.birthday,
        )

    def __create_session(self):
        """Create the session to be used with optional proxy for the account generation"""
        proxy = get_random_proxy(self.config)
        self.session = httpx.Client(
            base_url="https://www.instagram.com/api/v1",
            headers={
                "Authority": "www.instagram.com",
                "Referer": SIGNUP_PAGE,
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": get_random_user_agent(),
            },
            proxy=str(proxy) if proxy is not None else proxy,
            follow_redirects=True,
            timeout=30,
        )

        res = self.session.get(SIGNUP_PAGE)
        self.__parse_signup_page(res)

    def __parse_signup_page(self, res: httpx.Response):
        """Parses the signup page informations and set on the session

        Args:
            res (httpx.Response): The response to be parsed
        """
        self.session.headers.update(
            {
                "X-ASBD-ID": INSTGARAM_ASBD_ID,
                "X-CSRFToken": res.cookies["csrftoken"],
                "X-IG-App-ID": INSTAGRAM_APP_ID,
                "X-IG-WWW-Claim": "0",
            }
        )

        ic(self.session.headers)

        # set more cookies
        res = self.session.get("/web/login_page/")

        ic(res.cookies)
        # regex bruteforce :D
        self._machine_id = res.text.split('"machine_id":"')[1].split('"')[0]

        ic(self._machine_id)

    def __send_signup_request(self):
        """Do the sinup itself"""

        payload = {
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{self.person.password}",
            "email": self.email,
            "first_name": self.person.first_name,
            "username": self.person.username,
            "client_id": self._machine_id,
            "seamless_login_enabled": "1",
            "otp_into_one_tap": "false",
        }

        res = self.session.post("/web/accounts/web_create_ajax/attempt/", data=payload)
        data = res.json()
        ic(data)

        if data.get("username_suggestions") is not None and data.get("errors"):
            self.person.username = random.choice(data["username_suggestions"])
            self.__send_signup_request()

    def __send_birth_date_request(self):
        """Sends the birth date request"""
        payload = {
            "day": self.person.birthday.day,
            "month": self.person.birthday.month,
            "year": self.person.birthday.year,
        }

        res = self.session.post("/web/consent/check_age_eligibility/", data=payload)
        data = res.json()
        ic(data)

    def __send_verify_email_request(self):
        """Sends the verify email request"""
        payload = {
            "device_id": self._machine_id,
            "email": self.email,
        }
        res = self.session.post("/accounts/send_verify_email/", data=payload)
        data = res.json()
        ic(data)

    def __check_confirmation_code(self):
        """Checks if the confirmation code was received"""

        while self.email_agent.get_code_confirmation() is None:
            time.sleep(2)

        verification_code = self.email_agent.get_code_confirmation()

        payload = {
            "code": verification_code,
            "device_id": self._machine_id,
            "email": self.email,
        }

        res = self.session.post("/accounts/check_confirmation_code/", data=payload)
        data = res.json()
        ic(data)
        self.signup_code = data["signup_code"]

    def __finish_signup(self):
        """Finishes the signup process"""
        payload = {
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{self.person.password}",
            "day": self.person.birthday.day,
            "month": self.person.birthday.month,
            "year": self.person.birthday.year,
            "client_id": self._machine_id,
            "email": self.email,
            "username": self.person.username,
            "first_name": self.person.first_name,
            "seamless_login_enabled": "1",
            "force_sign_up_code": self.signup_code,
            "tos_version": "row",
        }

        res = self.session.post("/web/accounts/web_create_ajax/", data=payload)
        data = res.json()

        ic(data)

        return data.get("account_created")
