from datetime import datetime

import httpx
from bs4 import BeautifulSoup

from src.faker.base import FakePersonGenerator
from src.faker.person import Person
from src.utils.common import get_random_user_agent


class FakeNameGenerator(FakePersonGenerator):
    def __parse_data(self, res: httpx.Response) -> Person:
        """Parses the respone html data to extract the person data

        Args:
            res (httpx.Response): The response to be parsed

        Raises:
            ValueError: If no extra tag is found

        Returns:
            Person: The person data
        """
        soup = BeautifulSoup(res.text, "html.parser")
        data = dict()

        data["first_name"], data["last_name"] = (
            soup.find("h3").text.strip().split(maxsplit=1)  # type: ignore [fé]
        )

        extra_tag = soup.find("div", {"class": "extra"})
        if not extra_tag or isinstance(extra_tag, str):
            raise ValueError("No extra tag found")

        extra_data = {
            dt.text.strip().lower(): dd.text.strip()
            for dt, dd in zip(extra_tag.find_all("dt"), extra_tag.find_all("dd"))
        }
        data["birthday"] = datetime.strptime(extra_data["birthday"], "%B %d, %Y")

        data["username"], data["password"] = (
            extra_data["username"],
            extra_data["password"],
        )

        return Person(**data)

    def generate_person(self) -> Person:
        sesh = httpx.Client(
            base_url="https://www.fakenamegenerator.com",
            headers={"User-Agent": get_random_user_agent()},
            follow_redirects=True,
        )
        # TODO: define the country based on the self.config
        res = sesh.get("/gen-random-br-br.php")
        return self.__parse_data(res)
