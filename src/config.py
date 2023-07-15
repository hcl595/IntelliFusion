#config.py | Realizer Version 0.1.6(202307152000) Developer Alpha
import configparser
from pathlib import Path
import os

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
CONFIG_FILE = DATA_DIR / "config.cfg"

class Settings(object):
    def __init__(self):
        if not DATA_DIR.exists():
            DATA_DIR.mkdir()
        if not CONFIG_FILE.exists():
            print("Config does not exist and is being created automatically...")
            f = open(CONFIG_FILE,'w')
            f.write('[BaseConfig]\n')
            f.write('devmode = False\n')
            f.write('debug = False\n')
            f.write('keeplogin = True\n')
            f.write('\n')
            f.write('[RemoteConfig]\n')
            f.write('host = 127.0.0.1\n')
            f.write('port = 5000\n')
            f.write('\n')
            f.write('[ModelConfig]\n')
            f.write('DefaultModel = text-davinci-002\n')
            f.write('SecondModel = None\n')
            f.write('ThirdModel = None\n')
            f.write('\n')
            f.close()
            print("config is created successfully!")
        self.cfg = configparser.ConfigParser()
        self.cfg.read(CONFIG_FILE)

    def write(self, section, option, value):
        value = str(value)
        self.cfg.set(section,option,value)
        self.cfg.write(open(CONFIG_FILE, "w"))

    def read(self, section, option):
        out = self.cfg.get(section,option)
        return out
    