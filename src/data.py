# data.py | IntelliFusion Version 0.1.7(202307292000) Developer Alpha
from pathlib import Path
from loguru import logger
from peewee import *

# 基础类
APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATABASE_FILE = DATA_DIR / "models.sqlite"

from peewee import *

db = SqliteDatabase(DATABASE_FILE)

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = db

class Models(BaseModel):
<<<<<<< Updated upstream
    apikey = IntegerField(column_name='APIkey')
    display = CharField(column_name='Display', null=True)
    launch_compiler = CharField(column_name='LaunchCompiler', null=True)
    launch_path = CharField(column_name='LaunchUrl', null=True)
=======
    api_key = IntegerField(column_name="APIkey", null=True)
    display = CharField(column_name="Display", null=True)
    launch_compiler = CharField(column_name="LaunchCompiler", null=True)
    launch_path = CharField(column_name="LaunchPath", null=True)
>>>>>>> Stashed changes
    name = CharField()
    type = CharField()
    url = CharField()

    class Meta:
        table_name = 'models'

def SetupDatabase():
    db.create_tables([Models])
    BaseModel = Models(
        order=1,
        type="OpenAI",
        name="text-davinci-003",
        url="https:\\\\ai.fakeopen.com\\v1",
        APIkey="None",
        LaunchCompiler="NONE",
        LaunchUrl="NONE",
    )
    BaseModel.save()


