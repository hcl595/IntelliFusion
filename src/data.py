# data.py | IntelliFusion Version 0.1.7(202307292000) Developer Alpha
from pathlib import Path
from peewee import *

APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DATABASE_FILE = DATA_DIR / "models.sqlite"


db = SqliteDatabase(DATABASE_FILE)


class UnknownField(object):
    def __init__(self, *_, **__):
        pass


class BaseModel(Model):
    class Meta:
        database = db


class Models(BaseModel):
    api_key = IntegerField(column_name="APIkey")
    display = CharField(column_name="Display", null=True)
    launch_compiler = CharField(column_name="LaunchCompiler", null=True)
    launch_path = CharField(column_name="LaunchUrl", null=True)
    name = CharField()
    type = CharField()
    url = CharField()

    class Meta:
        table_name = "models"


def SetupDatabase():
    db.create_tables([Models])
    Models.create(
        order=1,
        type="OpenAI",
        name="text-davinci-003",
        url=r"https://ai.fakeopen.com:12345/v1",
        api_key="None",
        LaunchCompiler="NONE",
        LaunchUrl="NONE",
    )


if __name__ == "__main__":
    SetupDatabase()
