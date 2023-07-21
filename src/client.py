#main.py | Realizer Version 0.1.7(202307182000) Developer Alpha
#headers
import ctypes
import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse
from loguru import logger

from pyecharts.charts import Pie
import openai
import psutil
import requests
from flask import (Flask, json, jsonify, redirect, render_template, request,
                   session)
from flaskwebgui import FlaskUI, close_application

import data as db
from config import Settings
from data import models, userInfo
from setup import setup
from pathlib import Path

pool=ThreadPoolExecutor()

#configs
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'UMAVERSIONZPONEPSEV'
APP_DIR = Path(__file__).parent
DATA_DIR = APP_DIR / "data"
LOG_FILE = DATA_DIR / "models.log"

#setup
setup()
logger.add(LOG_FILE)
cfg = Settings()
global historys,NeedLogin,GPT_response,login_error
login_error = ""
response = {
        'response': '',
        'history': [['', '']],
        'status': 200,
        'time': '1234-05-06 07:08:09'}
GPT_response = []
LLM_response = []
GLM_response = []
result = None
NeedLogin = True
historys = response['history']

#main
@app.route('/')#根目录
def root():
    print(login_error)
    ModelList = db.session.query(
                models.id,
                models.type,
                models.name,
                models.url,
                models.APIkey,  
                models.LaunchCompiler,
                models.LaunchUrl,).all()
    try:
        ThirdBoxURL = db.session.query(models.url).filter(models.name == cfg.read("ModelConfig","ThirdModel")).first()
    except:
        ThirdBoxURL = None
    return render_template('main.html',
                            result = result,
                            NeedLogin = NeedLogin,
                            ModelList = ModelList,
                            ModelCount = len(ModelList) + 1,
                            historys = LLM_response,
                            ThirdBoxURL = ThirdBoxURL,
                            host = cfg.read("RemoteConfig","host"),
                            port = cfg.read("RemoteConfig","port"),
                            Mode = cfg.read("BaseConfig","devmode"),
                            BugM = cfg.read("BaseConfig","debug"),
                            DefaultModel = cfg.read("ModelConfig","DefaultModel"),
                            SecondModel = cfg.read("ModelConfig","SecondModel"),
                            ThirdModel = cfg.read("ModelConfig","ThirdModel"),
                            username = session.get('username'),)

@app.post('/llm')#GLM请求与回复1
def upload():
    global result,LLM_response
    InputInfo = request.form['userinput']
    InputModel =request.form["modelinput"]
    print(InputInfo,InputModel)
    LLM_response = llm(InputModel,InputInfo)
    return jsonify({'response': LLM_response})

@app.route('/openai', methods=['POST'])#openAI请求端口
def get_glm_response():
    global GLM_response
    InputInfo = request.form['userinput']
    InputModel = request.form["modelinput"]
    logger.debug("request:{}.model:{}",InputInfo,InputModel)
    openai_response = ai(InputModel,InputInfo)
    return jsonify({'response': openai_response})#ajax返回

@app.post('/EditSetting')#编辑设置
def EditSetting():
    InputDefaultModel = request.form.get("DefaultModel")
    InputSecondModel = request.form.get("SecondModel")
    InputThirdModel = request.form.get("ThirdModel")
    InputiPv4 = request.form.get("iPv4")
    InputPort = request.form.get("Port")
    InputWebMode = request.form.get("Mode")
    InputDebugMode = request.form.get("BugM")
    cfg.write("BaseConfig","devmode",InputWebMode)
    cfg.write("BaseConfig","debug",InputDebugMode)
    cfg.write("RemoteConfig","host",InputiPv4)
    cfg.write("RemoteConfig","port",InputPort)
    cfg.write("ModelConfig","DefaultModel",InputDefaultModel)
    cfg.write("ModelConfig","SecondModel",InputSecondModel)
    cfg.write("ModelConfig","ThirdModel",InputThirdModel)
    return redirect("/")

@app.post('/exchange')
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
        db.session.query(db.models).filter(models.id == InputID).update({
                                db.models.type: InputType,
                                db.models.name: InputComment,
                                db.models.url: InputUrl,
                                db.models.APIkey: InputAPIkey,
                                db.models.LaunchCompiler: LaunchCompiler,
                                db.models.LaunchUrl: LaunchUrl,
                                })
        db.session.commit()
        return jsonify({'response': "complete"})
    elif InputState == "del":
        db.session.query(models).filter(models.id == InputID).delete()
        db.session.commit()
        return jsonify({'response': "complete"})
    elif InputState == "run":
        launchCMD = request.form.get("LcCompiler") + " " + request.form.get("LcUrl")
        pool.submit(subprocess.run, launchCMD)
        count = 0
        while True:
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    return jsonify({'response': "complete"})
            count += 1
            time.sleep(1)
            if count == cfg.read('BaseConfig',"TimeOut"):
                logger.error('Model: {} launch maybe failed,because of Time Out({}),LaunchCompilerPath: {},LaunchFile: {}'
                             ,InputComment,cfg.read('BaseConfig',"TimeOut"),LaunchCompiler,LaunchUrl)
                return jsonify({'response': "TimeOut"})
    elif InputState == "stop":
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                pid = conn.pid
                p = psutil.Process(pid)
                p.kill()
                break
        return jsonify({'response': "complete"})
    elif InputState == "add":
        info = db.models(
                    type = InputType,
                    name = InputComment,
                    url = InputUrl,
                    APIkey = InputAPIkey,
                    LaunchCompiler = LaunchCompiler,
                    LaunchUrl = LaunchUrl,)
        db.session.add(info)
        db.session.commit()
        return jsonify({'response': "complete"})

@app.post('/login')#登录
def login_check():
    global login_error,choose,page
    account = request.form.get("logid")
    password = request.form.get("password")
    acc_result = db.session.query(userInfo.account).filter(userInfo.account == account).first()
    pwd_result = db.session.query(userInfo.password).filter(userInfo.account == account,userInfo.password == password).first()
    if account and password:
        if acc_result:
            if pwd_result:
                session['username']=account
                session['password']=password
                uid =db.session.query(userInfo.id).filter(userInfo.account==account,userInfo.password==password).first()
                uid = uid[0]
                session['uid']= uid
                if cfg.read("BaseConfig","KeepLogin") == 'True':
                    session.permanent=True
                login_error = "已登录"
                choose = 0
                return redirect('/')
            else:
                page = 'login'
                login_error = "密码错误"
                return redirect('/')
        else:
            page = 'login'
            login_error = "未知用户名"
            return redirect('/')
    else:
        page = 'login'
        login_error = "请写入信息"
        return redirect('/')
    
@app.post('/register')#注册
def register():
    global login_error,page
    account = request.form.get("reg_txt")
    mail = request.form.get("email")
    password = request.form.get("set_password")
    check_password = request.form.get("check_password")
    if account and password and mail:
        if password == check_password:
            info = db.userInfo(
                            account=account,
                            password=password,
                            mail=mail,)
            db.session.add(info)
            db.session.commit()
            login_error = '注册成功'
            logger.info('User: {account} ,has created an account.Password: {password}',account=account,password=password)
            page = 'login'
        else:
            login_error = '两次密码不一'
    else:
        page = "register"
        login_error = '完整填写信息'
    return redirect('/')

@app.get('/logout')#登出
def logout():
    logger.info('Application Closed')
    close_application()

@app.route('/CorePercent')
def WidgetsCorePercent():
    cpu_percent = psutil.cpu_percent()
    c = Pie().add("", [["占用", cpu_percent], ["空闲", 100 - cpu_percent]])
    return c.render_embed().replace(
        "https://assets.pyecharts.org/assets/v5/echarts.min.js",
        "./static/js/echarts.min.js",
    )

@app.route('/RamPercent')
def WigetsRamPercent():
    memory_percent = psutil.virtual_memory().percent
    c = Pie().add("", [["占用", memory_percent], ["空闲", 100 - memory_percent]])
    return c.render_embed().replace(
        "https://assets.pyecharts.org/assets/v5/echarts.min.js",
        "/static/js/echarts.min.js",
    )

@app.route("/static/js/echarts.min.js")
def js():
    with open("src\static\js\echarts.min.js", "rb") as f:
        data = f.read().decode()
    return data

if cfg.read("BaseConfig","devmode") == "True":
    @app.route("/test")
    def DevTest():
        return render_template("test.html")

@app.before_request
def before_NeedLogin():
    global NeedLogin
    if 'username' in session:
        if request.path == '/':
            NeedLogin = False
        else:
            pass
    else:
        NeedLogin = True

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404


#functions
def ai(ModelID:str,question:str): #TODO:把response转化为json
    response = ""
    openai.api_base = db.session.query(models.url).filter(models.name == ModelID).first()[0]
    openai.api_key = db.session.query(models.APIkey).filter(models.name == ModelID).first()[0]
    for chunk in openai.ChatCompletion.create(
        model=ModelID,
        messages=[
            {"role": "user", "content": question}
        ],
        stream=True,
        temperature = 0,
    ):
        if hasattr(chunk.choices[0].delta, "content"):
            print(chunk.choices[0].delta.content, end="", flush=True)
            response = response + chunk.choices[0].delta.content
            print(type(chunk.choices[0].delta.content))
    print(type(response))
    logger.info('model: {},url: {}/v1/completions.\nquestion: {},response: {}.'
                ,ModelID,db.session.query(models.url).filter(models.name == ModelID).first()[0],question,response)
    return response

def llm(ModelID:str,question:str):
    response = requests.post(
        url = db.session.query(models.url).filter(models.name == ModelID).one()[0],
        data=json.dumps({"prompt": question,"history": []}),
        headers={'Content-Type': 'application/json'})
    return response.json()['history'][0][1]


#launch
if __name__ == '__main__':
    logger.info('Application Launched!')
    if cfg.read("BaseConfig","devmode") == "True":
    #WEB MODE
        app.run(debug=cfg.read("BaseConfig","debug"),port=cfg.read("RemoteConfig","port"),host=cfg.read("RemoteConfig","host"))
    #GUI MODE
    else:
        print(cfg.read("BaseConfig","devMode"))
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
        FlaskUI(app=app,server='flask',port=cfg.read("RemoteConfig","port"),width=1000,height=800).run()
