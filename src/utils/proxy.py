import random
from pathlib import Path
from typing import Optional


def get_random_proxy(config: dict) -> Optional[str]:
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
    return random.choice(proxies)
