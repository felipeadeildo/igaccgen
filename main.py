import tomllib

from constants import CONFIG_PATH
from ig import InstagramClient


def main() -> None:
    """
    Main function
    """

    if CONFIG_PATH.exists():
        config = tomllib.load(CONFIG_PATH.open("rb"))
    else:
        config = dict()

    for _ in range(config.get("account_ammount", 1)):
        ig = InstagramClient(config)
        account = ig.generate_account()
        if account is not None:
            print(account.export())


if __name__ == "__main__":
    main()
