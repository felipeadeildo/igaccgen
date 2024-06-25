import os
from pathlib import Path

CLEAR_SCREEN_CMD = "cls" if os.name == "nt" else "clear"
"""Command to clear the screen"""


CONFIG_PATH = Path(__file__).parent / "config.toml"
"""Path to the config file"""