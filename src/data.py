# data.py | IntelliFusion Version 0.1.9(202308032000) Developer Alpha
from pathlib import Path
from peewee import *
from config import Settings

setting = Settings()


# 基础类
APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
Version = setting.read("package","Version")
DATABASE_FILE = DATA_DIR / f"data.{Version}.sqlite"

db = SqliteDatabase(DATABASE_FILE)

class BaseModel(Model):
    class Meta:
        database = db

class Models(BaseModel):
    apiKey = IntegerField(null=True, default="not_required")#To request Model
    launchCommand = CharField(null=True, default="")#To start model
    stream = BooleanField(null=True, default=True)#whether stream
    lunaBool = BooleanField(null=True, default=True)#whether participant luna model
    ollamaBool = BooleanField(null=True  , default=False)#whether add from ollama
    modelName = CharField()#Default Comment
    modelRemark = CharField(null=True  , default="")#Default Comment
    apiType = CharField()#To request Model
    requestUrl = CharField()#To request Model

    class Meta:
        table_name = 'models'

class APIs(BaseModel):
    requestFunctionName = CharField()

class Widgets(BaseModel):
    order = IntegerField(column_name="order", null=True)
    available =  CharField(column_name="available", default="True")
    size = CharField(null=True, default="medium")
    widgets_name = CharField(column_name="name",)
    widgets_url = CharField(column_name="URL",)

class History(BaseModel):
    session_id = IntegerField()# From Session.id
    UserInput = CharField()
    response = CharField()

class Sessions(BaseModel):
    #Session.id To History.session_id
    order = IntegerField(null=True) #Ordered Sessions
    model_id = CharField() #From Models.id
    comment = CharField(default="comment") #To Tab's Text
    modelSummary = BooleanField(default=True) #To Tab's Text

def SetupDatabase():
    db.create_tables([Models,Widgets,History,Sessions,APIs])
    BasicModel = Models(
        apiType="json",
        modelName="Luna",
        requestUrl="http://127.0.0.1:4230/",
        lunaBool=False,
        stream=False,
    )
    BasicModel.save()
    DefaultSession = Sessions(
        order = 1,
        model_id = 1,
        comment = "DefaultSession",
        modelSummary=True,
    )
    DefaultSession.save()
    DefaultAPI = APIs(
        requestFunctionName = "openai",
    )
    DefaultAPI.save()
    DefaultAPI = APIs(
        requestFunctionName = "ollama",
    )
    DefaultAPI.save()
    DefaultAPI = APIs(
        requestFunctionName = "json",
    )
    DefaultAPI.save()
    DefaultAPI = APIs(
        requestFunctionName = "WebUI",
    )
    DefaultAPI.save()
    BaseWidgets = Widgets(
        order=1,
        widgets_name="内置核心小组件",
        available = "True",
        widgets_url = "/widgets/CPU_Percent",
    )
    BaseWidgets.save()
    BaseWidgets = Widgets(
        order=2,
        widgets_name="内置内存小组件",
        available = "True",
        widgets_url = "/widgets/RAM_Percent",
    )
    BaseWidgets.save()
    BaseWidgets = Widgets(
        order=3,
        widgets_name="内置显存小组件",
        available = "True",
        widgets_url = "/widgets/GPU_Percent",
    )
    BaseWidgets.save()

