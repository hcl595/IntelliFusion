# config.py | Realizer Version 0.1.7(202307182000) Developer Alpha
import json
from pathlib import Path
from typing import Any

APP_DIR = Path(__file__).parent
CONFIG_FILE = APP_DIR / "config.json"


class Settings:
    def __init__(self):
        if not CONFIG_FILE.exists():
            data = {
                "BaseConfig": {"devmode": False, "debug": False, "keeplogin": True, "TimeOut": 60},
                "RemoteConfig": {"host": "127.0.0.1", "port": "5000"},
                "ModelConfig": {
                    "DefaultModel": "text-davinci-002",
                    "SecondModel": None,
                    "ThirdModel": None,
                },
            }
            with CONFIG_FILE.open("w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
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
