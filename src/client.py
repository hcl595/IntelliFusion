# main.py | Intellifusion Version 0.1.9(2023080512000) Developer Alpha
# headers
from thefuzz import process, fuzz
import ctypes
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import ipaddress
from urllib.parse import urlparse
from playhouse.shortcuts import model_to_dict

import openai
import jieba
import psutil
import requests
import validators
from flask import (Flask, json, jsonify, redirect, render_template, request,
                   session)
from flaskwebgui import FlaskUI, close_application
from loguru import logger

from config import Settings, Prompt
from data import Models
from setup import setup

pool = ThreadPoolExecutor()

# configs
app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "UMAVERSIONZPONEPEHT"
APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
LOG_FILE = DATA_DIR / "models.log"

# setup
setup()
logger.add(LOG_FILE)
cfg = Settings()
pmt = Prompt()
login_error = ""
response = {
    "response": "",
    "history": [["", ""]],
    "status": 200,
    "time": "1234-05-06 07:08:09",
}
GPT_response = []
LLM_response = []
GLM_response = []
result = None
NeedLogin = True
historys = response["history"]


# main
@app.route("/")  # 根目录
def root():
    logger.debug("login error: {}".format(login_error))
    try:
        ModelList = Models.select()
    except:
        ModelList = {}
    logger.debug("ModelList: {}",list(ModelList))
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
                logger.debug("model_ports: {}", model_ports[port])
        logger.debug("ActiveModels: {}", ActiveModels)
    else:
        ActiveModels = ModelList
    return render_template(
        "main.html",
        result=result,
        NeedLogin=NeedLogin,
        ActiveModels=ActiveModels,
        ModelList=list(ModelList),
        ModelCount=len(ModelList) + 1,
        historys=LLM_response,
        host=cfg.read("RemoteConfig", "host"),
        port=cfg.read("RemoteConfig", "port"),
        devMode=cfg.read("BaseConfig", "devmode"),
        TimeOut=cfg.read("BaseConfig", "TimeOut"),
        username=session.get("username"),
    )


@app.post("/requestmodels")
def Request_Models():
    InputInfo = request.form["userinput"]
    InputModel = request.form["modelinput"]
    if Models.get(Models.name == InputModel).type == "OpenAI":
        try:
            ai(InputModel, InputInfo)
        except:
            Model_response = "Check Your API and APIkey"
    elif Models.get(Models.name == InputModel).type == "API":
        try:
            Model_response = llm(InputModel, InputInfo)
        except:
            Model_response = "check your application is opened."
    return jsonify({"response": Model_response})


@app.post("/EditSetting")  # 编辑设置
def EditSetting():
    InputiPv4 = request.form.get("iPv4")
    InputPort = request.form.get("Port")
    InputWebMode = request.form.get("Mode")
    InputDebugMode = request.form.get("BugM")
    cfg.write("BaseConfig", "devmode", InputWebMode)
    cfg.write("BaseConfig", "debug", InputDebugMode)
    cfg.write("RemoteConfig", "host", InputiPv4)
    cfg.write("RemoteConfig", "port", InputPort)
    return redirect("/")


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
    logger.debug(LaunchCompiler)
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
            u = Models.get(id = InputID)
            u.delete_instance()
            return jsonify({"response": True,
                            "message":"删除成功",})
        except:
            return jsonify({"response": False,})
    elif InputState == "run":
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
            return jsonify({"response": True,})
        except:
            return jsonify({"response": False,})


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
    logger.debug("ModelList: {}",list(ModelList))
    ActiveModelList = ModelList
    ActiveModelList_json = [model_to_dict(Model) for Model in ActiveModelList]
    logger.info("{}", ActiveModelList_json)
    return jsonify(ActiveModelList_json)

if cfg.read("BaseConfig", "devmode") == "True":
    @app.route("/test")
    def DevTest():
        return render_template("test.html")


@app.errorhandler(404)
def error404(error):
    return render_template("404.html"), 404

from widgets import widgets_blue

app.register_blueprint(widgets_blue)


# functions
def ai(ModelID: str, question: str):
    response = ""
    logger.debug("{}", Models.get(Models.name == ModelID).url)
    openai.api_base = (Models.get(Models.name == ModelID).url)
    openai.api_key = (
        Models.get(Models.name == ModelID).api_key
    )
    for chunk in openai.ChatCompletion.create(
        model=ModelID,
        messages=[{"role": "user", "content": question}],
        stream=True,
        temperature=0,
    ):
        if hasattr(chunk.choices[0].delta, "content"):
            print(chunk.choices[0].delta.content, end="", flush=True)
            response = response + chunk.choices[0].delta.content
            print(type(chunk.choices[0].delta.content))
    print(type(response))
    logger.info(
        "model: {},url: {}/v1/completions.\nquestion: {},response: {}.",
        ModelID,
        Models.get(Models.name == ModelID).url,
        question,
        response,
    )
    return response


def llm(ModelID: str, question: str):
    response = requests.post(
        url=Models.get(Models.name == ModelID).url,
        data=json.dumps({"prompt": question, "history": []}),
        headers={"Content-Type": "application/json"},
    )
    return response.json()["history"][0][1]


def get_ports(url: str):
    port = urlparse(url).port
    if port == None:
        if not validators.url(url):
            pass
        else:
            port = "url"
    logger.debug("parse ports: {}", port)
    return port

# launch
if __name__ == "__main__":
    logger.info(
        "Application(v0.1.9a) Launched!", cfg.read("BaseConfig", "devmode")
    )
    if cfg.read("BaseConfig", "devmode") == "True":
        logger.level("DEBUG")
        logger.debug("run in debug mode")
        app.run(
            debug=cfg.read("BaseConfig", "devmode"),
            port=cfg.read("RemoteConfig", "port"),
            host=cfg.read("RemoteConfig", "host"),
        )
    elif cfg.read("BaseConfig", "devmode") == "False" or cfg.read("BaseConfig", "devmode") == False:
        logger.debug("run in GUI mode")
        print(cfg.read("BaseConfig", "devmode"))
        try:
            ctypes.windll.user32.ShowWindow(
                ctypes.windll.kernel32.GetConsoleWindow(), 0
            )
        except:
            pass
        FlaskUI(
            app=app,
            server="flask",
            port=cfg.read("RemoteConfig", "port"),
            width=1800,
            height=1000,
        ).run()
