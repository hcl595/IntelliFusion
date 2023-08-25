# main.py | Intellifusion Version 0.2.0(2023082412000) Developer Alpha
# headers
import ctypes
import ipaddress
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Literal, TypedDict
from urllib.parse import urlparse
import socketserver

import jieba
import openai
import psutil
import requests
import validators
from flask import Flask, stream_with_context, json, jsonify, render_template, request
from flaskwebgui import FlaskUI, close_application
from loguru import logger
from playhouse.shortcuts import model_to_dict
from thefuzz import fuzz, process
from peewee import fn

from config import Prompt, Settings
from data import History, Models, Widgets
from setup import setup

pool = ThreadPoolExecutor()

# configs
app = Flask(__name__)
app.config.from_object(__name__)
APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
DICT_DIR = APP_DIR / "dicts" / "dict.txt"
LOG_FILE = DATA_DIR / "models.log"

# setup
setup()
jieba.set_dictionary(DICT_DIR)
jieba.initialize()
logger.add(LOG_FILE)
cfg = Settings()
pmt = Prompt()
login_error = ""

def get_free_port():
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
    return free_port

api_port = get_free_port()

# main
@app.route("/")  # 根目录
def root():
    return render_template("main.html")


@app.get("/get_api_port")
def get_api_port():
    return api_port


@app.post("/request_models_stream")
@stream_with_context
def request_models_stream():
    InputInfo = request.form.get("userinput")
    InputModel = request.form["modelinput"]
    try:
        Model_response = ai(InputModel, InputInfo, "stream")
        for r in Model_response:
            yield r
        History.create(
            Model=InputModel,
            UserInput = InputInfo,
            response=r,
        )
    except openai.error.AuthenticationError:
        yield "Check Your API Key"


@app.post("/requestmodels")
def Request_Models():
    InputInfo = request.form["userinput"]
    InputModel = request.form["modelinput"]
    if Models.get(Models.name == InputModel).type == "OpenAI":
        try:
            Model_response = ai(InputModel, InputInfo, "normal")
            History.create(
                Model=InputModel,
                UserInput = InputInfo,
                response=Model_response,
            )
        except openai.error.AuthenticationError:
            Model_response = "Check Your API Key"
        except UnboundLocalError:
            Model_response = "DataBase Error,get support from Developer!"
        # except IntegrityError:
    elif Models.get(Models.name == InputModel).type == "API":
            Model_response = llm(InputModel, InputInfo)
            # response = html.escape(response)
            History.create(
                Model=InputModel,
                UserInput = InputInfo,
                response=Model_response,
            )
    return jsonify({"response": Model_response})


@app.post("/GetHistory")
def GetHistorys():
    h_id = request.form.get("id")
    model = Models.get(Models.id == h_id).name
    history = History.select().where(History.Model == model)
    history_json = [model_to_dict(h) for h in history]
    return jsonify(history_json)


@app.post("/GetActiveWidgets")
def GetActiveWidgets():
    ActiveWidgets = Widgets.select().order_by(Widgets.order).where(Widgets.available == "True")
    ActiveWidgets_json = [model_to_dict(Model) for Model in ActiveWidgets]
    return jsonify(ActiveWidgets_json)


@app.post("/GetWidgets")
def GetWidgets():
    ActiveWidgets = Widgets.select().order_by(Widgets.order)
    ActiveWidgets_json = [model_to_dict(Model) for Model in ActiveWidgets]
    logger.debug(ActiveWidgets_json)
    return jsonify(ActiveWidgets_json)


@app.post("/EditWidgetsOrder")
def EditWidgetsOrder():
    Temp = Widgets.update({
        Widgets.order : request.form.get("order")
    }).where(Widgets.id == request.form.get("id"))
    Temp.execute()
    return jsonify({"response":True,})


@app.post("/EditSetting")  # 编辑设置
def EditSetting():
    cfg.write("BaseConfig","Theme", request.form.get("Theme"))
    cfg.write("BaseConfig","Language", request.form.get("Language"))
    cfg.write("BaseConfig","Timeout", request.form.get("Timeout"))
    cfg.write("BaseConfig","ActiveExamine", request.form.get("ActiveExamine"))
    cfg.write("BaseConfig", "Develop", request.form.get("Develop"))
    cfg.write("RemoteConfig", "Host", request.form.get("Host"))
    cfg.write("RemoteConfig", "Port", request.form.get("Port"))
    return jsonify({"response": True,})


@app.post("/GetSetting")
def GetSetting():
    return jsonify({
        "response": "true",
        "Theme": cfg.read("BaseConfig","Theme"),
        "Language": cfg.read("BaseConfig","Language"),
        "ActiveExamine": cfg.read("BaseConfig","ActiveExamine"),
        "Timeout": cfg.read("BaseConfig","Timeout"),
        "Host": cfg.read("RemoteConfig","Host"),
        "Port": cfg.read("RemoteConfig","Port"),
        "Develop": cfg.read("BaseConfig","Develop"),
        })


@app.post("/edit_widgets")
def edit_widgets():
    widgets_id = request.form.get("id")
    widgets_name = request.form.get("name")
    widgets_url = request.form.get("url")
    available = request.form.get("ava")
    if widgets_id == "-1":
        try:
            w = Widgets(
                order =  Widgets.select(fn.MAX(Widgets.order)).get().order + 1,
                widgets_name = widgets_name,
                widgets_url = widgets_url,
                available = available,
            )
            w.save()
            return jsonify({"response": True, "message": "添加成功"})
        except:
            return jsonify({"response": False, "message": "添加失败"})
    else:
        if request.form.get("operation") == "edit":
            try:
                u = Widgets.update({
                    Widgets.widgets_name: widgets_name,
                    Widgets.widgets_url: widgets_url,
                    Widgets.available: available,
                }).where(Widgets.id == widgets_id)
                u.execute()
                return jsonify({"response": True, "message": "更改成功"})
            except:
                return jsonify({"response": False, "message": "更改失败"})
        elif request.form.get("operation") == "del":
            try:
                w = Widgets.get(Widgets.id == widgets_id)
                w.delete_instance()
                return jsonify({"response": True, "message": "更改成功"})
            except:
                return jsonify({"response": False, "message": "更改失败"})


@app.post("/exchange")
def AddModel():
    InputState = request.form.get("state")
    InputID = request.form.get("number")
    InputType = request.form.get("type")
    InputComment = request.form.get("comment")
    InputUrl = request.form.get("url")
    InputAPIkey = request.form.get("APIkey")
    LaunchCompiler = request.form.get("LcCompiler")
    LaunchPath = request.form.get("LcUrl")
    try:
        port = int(urlparse(InputUrl).port)
    except:
        port = 80
    if InputState == "edit":
        try:
            logger.info("User Inputs: {}, {}, {}", InputType, InputID,InputAPIkey)
            u = Models.update({
                Models.name: InputComment,
                Models.url: InputUrl,
                Models.api_key: InputAPIkey,
                Models.launch_compiler: LaunchCompiler,
                Models.launch_path: LaunchPath,
                Models.type: InputType,
            }).where(Models.id == InputID)
            u.execute()
            return jsonify({"response": True,
                            "message":"编辑成功",})
        except:
            return jsonify({"response": False,
                            "message":"编辑失败",})
    elif InputState == "del":
        try:
            u = Models.get(Models.id == InputID)
            u.delete_instance()
            return jsonify({"response": True,
                            "message":"删除成功",})
        except:
            return jsonify({"response": False,})
    elif InputState == "run":
        if request.form.get("LcCompiler") == "/" or request.form.get("LcUrl") == "/":
            return jsonify({"response": False,
                            "message":"运行失败,原因:请输入正确的启动方式",})
        else:
            launchCMD = request.form.get("LcCompiler") + " " + request.form.get("LcUrl")
            pool.submit(subprocess.run, launchCMD)
            count = 0
            while True:
                for conn in psutil.net_connections():
                    if conn.laddr.port == port:
                        return jsonify({"response": True,
                                        "message":"运行成功",})
                count += 1
                time.sleep(1)
                if count == cfg.read("BaseConfig", "TimeOut"):
                    logger.error(
                        "Model: {} launch maybe failed,because of Time Out({}),LaunchCompilerPath: {},LaunchFile: {}",
                        InputComment,
                        cfg.read("BaseConfig", "TimeOut"),
                        LaunchCompiler,
                        LaunchPath,
                    )
                    return jsonify({"response": False,
                                    "message":"运行失败,原因:超时",})
    elif InputState == "stop":
        try:
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    pid = conn.pid
                    p = psutil.Process(pid)
                    p.kill()
                    break
            return jsonify({"response": True,
                            "message":"停止成功",})
        except:
            return jsonify({"response": False,
                            "message":"停止失败成功",})
    elif InputState == "add":
        try:
            Models.create(
                type=InputType,
                name=InputComment,
                url=InputUrl,
                api_key=InputAPIkey,
                launch_compiler=LaunchCompiler,
                launch_path=LaunchPath,
            )
            return jsonify({"response": True,
                            "message": "添加成功"})
        except:
            return jsonify({"response": False,
                            "message": "添加失败"})


@app.get("/close")  # 关闭
def logout():
    logger.info("Application Closed")
    close_application()


@app.post("/prompts")
def Prompts():
    userinput = request.form.get("text")
    if userinput:
        prompts = pmt.read_config()
        prompt = {i["act"]:i["prompt"] for i in prompts}
        keywords = jieba.lcut_for_search(userinput)
        keywords = " ".join(keywords)
        result = process.extract(
            keywords, prompt.keys(), limit=5, scorer=fuzz.partial_token_sort_ratio
        )
        result = {t:prompt[t] for (t,_) in result}
    else:
        result = {}
    logger.info("{}",result)
    return jsonify(result)


@app.post("/GetModelList")
def GetModelList():
    try:
        ModelList = Models.select()
    except:
        ModelList = {}
    ModelList_json = [model_to_dict(Model) for Model in ModelList]
    logger.info("{}", ModelList_json)
    return jsonify(ModelList_json)


@app.post("/GetActiveModels")
def GetActiveModels():
    try:
        ModelList = Models.select()
    except:
        ModelList = {}
    ActiveModels = []
    if cfg.read("BaseConfig","ActiveExamine") == "True":
        for i in ModelList:
            if validators.url(i.url):
                host = urlparse(i.url).hostname
                logger.info("{}",host)
                try:
                    ipaddress.ip_address(host)
                except:
                    ActiveModels.append(i)
        model_ports = {port: m for m in ModelList if (port := urlparse(m.url).port)}
        for conn in psutil.net_connections():
            port = conn.laddr.port
            if port in model_ports:
                ActiveModels.append(model_ports[port])
    else:
        ActiveModels = ModelList
    ActiveModelList_json = [model_to_dict(Model) for Model in ActiveModels]
    logger.info("{}", ActiveModelList_json)
    return jsonify(ActiveModelList_json)


@app.errorhandler(404)
def error404(error):
    return render_template("404.html"), 404


#Blue Prints
from widgets import widgets_blue

app.register_blueprint(widgets_blue)


# class
class Message(TypedDict):
    role: Literal["admin"] | Literal["user"]
    content: str


# functions
def ai(ModelID: str, question_in: str,method: str):
    response = ""
    openai.api_base = (Models.get(Models.name == ModelID).url)
    messages = []
    for r in History.select().where(History.Model == ModelID):
        r: History
        assert isinstance(r.UserInput, str)
        assert isinstance(r.response, str)
        question: Message = {"role": "user", "content": r.UserInput}
        response_model: Message = {"role": "assistant", "content": r.response}
        messages.append(question)
        messages.append(response_model)
    question: Message = {"role": "user", "content": question_in}
    messages.append(question)
    openai.api_key = (
        Models.get(Models.name == ModelID).api_key
    )
    for chunk in openai.ChatCompletion.create(
        model=ModelID,
        messages=messages,
        stream=True,
        temperature=0,
    ):
        if method == "stream":
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="", flush=True)
                response = response + chunk.choices[0].delta.content
                response = str.replace(response,"\n","<br/>")
                last_code_block_index: int = -1
                is_code_block_start = True
                while (last_code_block_index := response.find("```")) != -1:
                    if is_code_block_start:
                        response=response.replace("```", "<pre>", 1)
                    else:
                        response=response.replace("```", "</pre>", 1)
                    last_code_block_index=-1
                    is_code_block_start=not is_code_block_start
                logger.info("{}", response)
                yield response
        else:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="", flush=True)
                response = response + chunk.choices[0].delta.content
                response = str.replace(response,"\n","<br/>")
                last_code_block_index: int = -1
                is_code_block_start = True
                while (last_code_block_index := response.find("```")) != -1:
                    if is_code_block_start:
                        response=response.replace("```", "<pre>", 1)
                    else:
                        response=response.replace("```", "</pre>", 1)
                    last_code_block_index=-1
                    is_code_block_start=not is_code_block_start
                logger.info("{}", response)
            return response

def llm(ModelID: str, question: str):
    response = requests.post(
        url=Models.get(Models.name == ModelID).url,
        data=json.dumps({"prompt": question, "history": []}),
        headers={"Content-Type": "application/json"},
    )
    response = str.replace(response.json()["history"][0][1],"\n","<br/>")
    last_code_block_index: int = -1
    is_code_block_start = True
    while (last_code_block_index := response.find("```")) != -1:
        if is_code_block_start:
            response=response.replace("```", "<pre>", 1)
        else:
            response=response.replace("```", "</pre>", 1)
        last_code_block_index=-1
        is_code_block_start=not is_code_block_start
    return response

if cfg.read("BaseConfig", "Develop") == "True":
    try:
        id = Widgets.get(Widgets.widgets_name == "test").id
    except:
        w = Widgets(
            order = 4,
            widgets_name = "test",
            widgets_url = "/widgets/test",
            available = "true",
        )
        w.save()
    
    @app.route("/test")
    def DevTest():
        return render_template("test.html")
    
    @app.route("/offline")
    def offline():
        return render_template("offline.html")

# launch
if __name__ == "__main__":
    logger.info("Application(v0.1.9 ∆) Launched!")
    if cfg.read("BaseConfig", "Develop") == "True":
        logger.level("DEBUG")
        logger.debug("run in debug mode")
        if cfg.read("RemoteConfig", "Port") == "0":
            app.run(
                debug=cfg.read("BaseConfig", "Develop"),
                port=get_free_port(),
                host=cfg.read("RemoteConfig", "Host"),
            )
        else:
            app.run(
                debug=cfg.read("BaseConfig", "Develop"),
                port=cfg.read("RemoteConfig", "Port"),
                host=cfg.read("RemoteConfig", "Host"),
            )
    elif cfg.read("BaseConfig", "Develop") == "False" or cfg.read("BaseConfig", "Develop") == False:
        logger.debug("run in GUI mode")
        print(cfg.read("BaseConfig", "Develop"))
        try:
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0
            )
        except:
            pass
        FlaskUI(
            app=app,
            server="flask",
            port=cfg.read("RemoteConfig", "Port"),
            width=1800,
            height=1000,
        ).run()
