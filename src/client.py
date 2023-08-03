# main.py | Intellifusion Version 0.1.9(202308032000) Developer Alpha
# headers
import ctypes
import json
import subprocess
import time
import validators
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlparse

import openai
import psutil
import requests
from flask import Flask, json, jsonify, redirect, render_template, request, session
from flaskwebgui import FlaskUI, close_application
from loguru import logger

from config import Settings
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
    ModelList = Models.select()
    logger.debug("ModelList: {}",list(ModelList))
    ActiveModels = []
    model_ports = {port: m for m in ModelList if (port := get_ports(m.url))}
    if cfg.read("BaseConfig","ActiveExamine") == "True":
        for conn in psutil.net_connections():
            port = conn.laddr.port
            if port in model_ports:
                ActiveModels.append(model_ports[port])
                logger.debug("model_ports: {}", model_ports[port])
        if 12140 in model_ports:
            ActiveModels.append(model_ports[12140])
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
        Mode=cfg.read("BaseConfig", "devmode"),
        BugM=cfg.read("BaseConfig", "debug"),
        TimeOut=cfg.read("BaseConfig", "TimeOut"),
        username=session.get("username"),
    )


@app.post("/llm")
def upload():  # GLM请求与回复1
    global result, LLM_response
    InputInfo = request.form["userinput"]
    InputModel = request.form["modelinput"]
    print(InputInfo, InputModel)
    LLM_response = llm(InputModel, InputInfo)
    return jsonify({"response": LLM_response})


@app.route("/openai", methods=["POST"])
def get_glm_response():  # openAI请求端口
    global GLM_response
    InputInfo = request.form["userinput"]
    InputModel = request.form["modelinput"]
    logger.debug("request:{}.model:{}", InputInfo, InputModel)
    openai_response = ai(InputModel, InputInfo)
    return jsonify({"response": openai_response})  # ajax返回


@app.post("/EditSetting")  # 编辑设置
def EditSetting():
    InputDefaultModel = request.form.get("DefaultModel")
    InputSecondModel = request.form.get("SecondModel")
    InputThirdModel = request.form.get("ThirdModel")
    InputiPv4 = request.form.get("iPv4")
    InputPort = request.form.get("Port")
    InputWebMode = request.form.get("Mode")
    InputDebugMode = request.form.get("BugM")
    cfg.write("BaseConfig", "devmode", InputWebMode)
    cfg.write("BaseConfig", "debug", InputDebugMode)
    cfg.write("RemoteConfig", "host", InputiPv4)
    cfg.write("RemoteConfig", "port", InputPort)
    cfg.write("ModelConfig", "DefaultModel", InputDefaultModel)
    cfg.write("ModelConfig", "SecondModel", InputSecondModel)
    cfg.write("ModelConfig", "ThirdModel", InputThirdModel)
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
    logger.info("User Inputs: {}, {}, {}", InputState, InputID,InputAPIkey)
    try:
        port = int(urlparse(InputUrl).port)
    except:
        port = 80
    logger.debug(LaunchCompiler)
    if InputState == "edit":
        u = Models.update({
            Models.type: InputType,
            Models.name: InputComment,
            Models.url: InputUrl,
            Models.api_key: InputAPIkey,
            Models.launch_compiler: LaunchCompiler,
            Models.launch_path: LaunchPath,
        }).where(Models.id == InputID)
        u.execute()
        return jsonify({"response": "complete"})
    elif InputState == "del":
        u = Models.get(id = InputID)
        u.delete_instance()
        return jsonify({"response": "complete"})
    elif InputState == "run":
        launchCMD = request.form.get("LcCompiler") + " " + request.form.get("LcUrl")
        pool.submit(subprocess.run, launchCMD)
        count = 0
        while True:
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    return jsonify({"response": "complete"})
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
                return jsonify({"response": "TimeOut"})
    elif InputState == "stop":
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                pid = conn.pid
                p = psutil.Process(pid)
                p.kill()
                break
        return jsonify({"response": "complete"})
    elif InputState == "add":
        Models.create(
            type=InputType,
            name=InputComment,
            url=InputUrl,
            api_key=InputAPIkey,
            launch_compiler=LaunchCompiler,
            launch_path=LaunchPath,
        )
        return jsonify({"response": "complete"})


@app.get("/close")  # 关闭
def logout():
    logger.info("Application Closed")
    close_application()


@app.route("/CorePercent")
def WidgetsCorePercent():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent


@app.route("/RamPercent")
def WigetsRamPercent():
    memory_percent = psutil.virtual_memory().percent
    return memory_percent


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
def ai(ModelID: str, question: str):  # TODO:把response转化为json
    response = ""
    openai.api_base = (
        Models.get(Models.id == ModelID).url
    )
    openai.api_key = (
        Models.get(Models.id == ModelID).api_key
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
        Models.get(Models.id == ModelID).url,
        question,
        response,
    )
    return response


def llm(ModelID: str, question: str):
    response = requests.post(
        url=Models.get(Models.id == ModelID).url,
        data=json.dumps({"prompt": question, "history": []}),
        headers={"Content-Type": "application/json"},
    )
    return response.json()["history"][0][1]


def get_ports(url: str):
    port = urlparse(url).port
    if port == None:
        # try:
        #     context = ssl._create_default_https_context()
        #     url_request.urlopen(url[0:-4], context=context)
        #     port = 12140
        # except url_error.URLError:
        #     port = None
        if not validators.url(url):
            pass
        else:
            port = 12140
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
            debug=cfg.read("BaseConfig", "debug"),
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
            width=1000,
            height=800,
        ).run()
