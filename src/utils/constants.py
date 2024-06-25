import os
from pathlib import Path

CLEAR_SCREEN_CMD = "cls" if os.name == "nt" else "clear"
"""Command to clear the screen"""

CONFIG_PATH = Path(os.getcwd()) / "config.toml"
"""Path to the config file"""
