# config.py | IntelliFusion Version 0.1.7(202307292000) Developer Alpha
import json
from pathlib import Path
from typing import Any

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
PROM_DIR = APP_DIR / "prompt"
CONFIG_FILE = DATA_DIR / "config.json"


class Settings:
    def __init__(self):
        with CONFIG_FILE.open(encoding="utf-8") as f:
            self.cfg = json.load(f)

    def write(self, section: str, option: str, value: Any) -> Any:
        self.cfg[section][option] = value
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(self.cfg, f, ensure_ascii=False, indent=4)

    def read(self, section: str, option: str) -> Any:
        return self.cfg.get(section).get(option)

class Prompt:
    def __init__(self):
        PROMPT_FILE = (PROM_DIR / Settings().read("BaseConfig","Language")).with_suffix(".json")
        with PROMPT_FILE.open(encoding="utf-8") as f:
            self.cfg = json.load(f)
    
    def read_config(self):
        PROMPT_FILE = (PROM_DIR / Settings().read("BaseConfig","Language")).with_suffix(".json")
        with PROMPT_FILE.open(encoding="utf-8") as f:
            self.cfg = json.load(f)
        return self.cfg