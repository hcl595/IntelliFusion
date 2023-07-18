# config.py | Realizer Version 0.1.7(202307182000) Developer Alpha
import json
from pathlib import Path
from loguru import logger
from typing import Any

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
LOG_FILE = DATA_DIR / "models.log"
CONFIG_FILE = DATA_DIR / "config.json"


class Settings:
    def __init__(self):
        with CONFIG_FILE.open(encoding="utf-8") as f:
            self.cfg = json.load(f)

    def write(self, section: str, option: str, value: Any) -> Any:
        """
        >>> s = Settings()
        >>> s.write("BaseConfig", "devmode", True)
        >>> s.read("BaseConfig", "devmode")
        True
        """
        self.cfg[section][option] = value
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(self.cfg, f, ensure_ascii=False, indent=4)

    def read(self, section: str, option: str) -> Any:
        return self.cfg.get(section).get(option)
