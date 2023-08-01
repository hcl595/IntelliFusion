# main.py | Intellifusion Version 0.1.7(202307292000) Developer Alpha
# headers
import ctypes
import json
import subprocess
import time
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
app.config["SECRET_KEY"] = "UMAVERSIONZPONEPSEV"
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
    # breakpoint()
    logger.debug("login error: {}".format(login_error))
    ModelList = Models.select()
    ActiveModels = []
    model_ports = {port: m for m in ModelList if (port := urlparse(m.url).port)}
    for conn in psutil.net_connections():
        port = conn.laddr.port
        if port in model_ports:
            ActiveModels.append(model_ports[port])
    logger.debug("ActiveModels: {}", ActiveModels)
    return render_template(
        "main.html",
        result=result,
        NeedLogin=NeedLogin,
        ActiveModels=ActiveModels,
        ModelList=ModelList,
        ModelCount=len(ModelList) + 1,
        historys=LLM_response,
        host=cfg.read("RemoteConfig", "host"),
        port=cfg.read("RemoteConfig", "port"),
        Mode=cfg.read("BaseConfig", "devmode"),
        BugM=cfg.read("BaseConfig", "debug"),
        TimeOut=cfg.read("BaseConfig", "debug"),
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
    LaunchUrl = request.form.get("LcUrl")
    try:
        port = int(urlparse(InputUrl).port)
    except:
        port = 80
    logger.debug(LaunchCompiler)
    if InputState == "edit":
        db.session.query(db.models).filter(models.id == InputID).update(
            {
                db.models.type: InputType,
                db.models.name: InputComment,
                db.models.url: InputUrl,
                db.models.APIkey: InputAPIkey,
                db.models.LaunchCompiler: LaunchCompiler,
                db.models.LaunchUrl: LaunchUrl,
            }
        )
        db.session.commit()
        return jsonify({"response": "complete"})
    elif InputState == "del":
        db.session.query(models).filter(models.id == InputID).delete()
        db.session.commit()
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
                    LaunchUrl,
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
        info = db.models(
            type=InputType,
            name=InputComment,
            url=InputUrl,
            APIkey=InputAPIkey,
            LaunchCompiler=LaunchCompiler,
            LaunchUrl=LaunchUrl,
        )
        db.session.add(info)
        db.session.commit()
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


# functions
def ai(ModelID: str, question: str):  # TODO:把response转化为json
    response = ""
    openai.api_base = (
        db.session.query(models.url).filter(models.name == ModelID).first()[0]
    )
    openai.api_key = (
        db.session.query(models.APIkey).filter(models.name == ModelID).first()[0]
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
        db.session.query(models.url).filter(models.name == ModelID).first()[0],
        question,
        response,
    )
    return response


def llm(ModelID: str, question: str):
    response = requests.post(
        url=db.session.query(models.url).filter(models.name == ModelID).one()[0],
        data=json.dumps({"prompt": question, "history": []}),
        headers={"Content-Type": "application/json"},
    )
    return response.json()["history"][0][1]


# launch
if __name__ == "__main__":
    logger.info(
        "Application Launched by Dev Mode {}!", cfg.read("BaseConfig", "devmode")
    )
    if cfg.read("BaseConfig", "debug") == "True":
        logger.level("DEBUG")
        logger.debug("run in debug mode")
    if cfg.read("BaseConfig", "devmode") == "True":
        logger.debug("run in web mode")
        app.run(
            debug=cfg.read("BaseConfig", "debug"),
            port=cfg.read("RemoteConfig", "port"),
            host=cfg.read("RemoteConfig", "host"),
        )
    elif cfg.read("BaseConfig", "devmode") == "False":
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
