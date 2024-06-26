import random
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Proxy:
    """Proxy credentials data representation"""

    ip: str
    port: str
    username: Optional[str] = None
    password: Optional[str] = None

    def __str__(self):
        if self.username is None or self.password is None:
            return f"https://{self.ip}:{self.port}"
        else:
            return f"https://{self.username}:{self.password}@{self.ip}:{self.port}"


def get_random_proxy(config: dict) -> Optional[Proxy]:
    """Gets a random proxy credentials from the proxy file set in the config

    Args:
        config (dict): The config to be used
    """
    proxy_path = Path(config.get("proxy_path", "proxy.txt"))
    if not proxy_path.exists():
        return None
    proxies = proxy_path.read_text().split("\n")
    if not proxies:
        return None
    keys = Proxy.__dataclass_fields__.keys()
    proxy = random.choice(proxies).split(":")
    return Proxy(**dict(zip(keys, proxy)))
