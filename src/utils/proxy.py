import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class Proxy:
    """Proxy credentials data representation"""

    ip: str
    port: int = field(init=False)
    username: Optional[str] = None
    password: Optional[str] = None

    def __post_init__(self):
        self.port = int(self.port)


def get_random_proxy(config: dict) -> Optional[Proxy]:
    """Gets a random proxy credentials from the proxy file set in the config

    Args:
        config (dict): The config to be used
    """
    proxy_path = Path(config["proxy_path"])
    if not proxy_path.exists():
        return None
    proxies = proxy_path.read_text().split("\n")
    if not proxies:
        return None
    keys = Proxy.__dataclass_fields__.keys()
    proxy = random.choice(proxies).split(":")
    return Proxy(**dict(zip(keys, proxy)))
