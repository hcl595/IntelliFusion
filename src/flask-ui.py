#main.py | Realizer Version 0.1.6(202307152000) Developer Alpha
#headers
from flask import Flask, render_template, redirect, request, session, json, jsonify
import openai
from flaskwebgui import FlaskUI
from flaskwebgui import FlaskUI,close_application
from config import Settings
import data as db
from data import userInfo,models,setup
import ctypes
import requests
import json
import os
from urllib.parse import urlparse
import psutil

#configs
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'UMAVERSIONZPONEPSIX'

#setup
setup()
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
        ThirdBoxURL = db.session.query(models.url).filter(models.name == cfg.read("ModelConfig","ThirdModel")).one()[0]
    except:
        ThirdBoxURL = None
    return render_template('main.html',
                            result = result,
                            NeedLogin = NeedLogin,
                            ModelList = ModelList,
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
    print("model:",InputInfo,InputModel)
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
    print(InputDefaultModel,InputSecondModel,)
    cfg.write("BaseConfig","devmode",InputWebMode)
    cfg.write("BaseConfig","debug",InputDebugMode)
    cfg.write("RemoteConfig","host",InputiPv4)
    cfg.write("RemoteConfig","port",InputPort)
    cfg.write("ModelConfig","DefaultModel",InputDefaultModel)
    cfg.write("ModelConfig","SecondModel",InputSecondModel)
    cfg.write("ModelConfig","ThirdModel",InputThirdModel)
    return redirect("/")

@app.post('/exchange') #TODO: 适配前端ajax
def AddModel():
    Number = request.form["number"]
    if Number == "-1":
            InputType = request.form["type"]
            InputComment = request.form.get("comment")
            InputUrl = request.form.get("url")
            InputAPIkey = request.form.get("APIkey")
            LaunchCompiler = request.form.get("LcCompiler")
            LaunchUrl = request.form.get("LCurl")
            info = db.models(
                        type = InputType,
                        name = InputComment,
                        url = InputUrl,
                        APIkey = InputAPIkey,
                        LaunchCompiler = LaunchCompiler,
                        LaunchUrl = LaunchUrl,)
            db.session.add(info)
    else:
        InputState = request.form.get(Number + "state")
        print(InputState)
        if InputState == "edit":
            InputType = request.form.get("type")
            InputComment = request.form.get("comment")
            InputUrl = request.form.get("url")
            InputAPIkey = request.form.get("APIkey")
            LaunchCompiler = request.form.get("LcCompiler")
            LaunchUrl = request.form.get("LcUrl")
            db.session.query(db.models).filter(models.id == Number).update({
                    db.models.type: InputType,
                    db.models.name: InputComment,
                    db.models.url: InputUrl,
                    db.models.APIkey: InputAPIkey,
                    db.models.LaunchCompiler: LaunchCompiler,
                    db.models.LaunchUrl: LaunchUrl,
                    })
        elif InputState == "del":
            db.session.query(models).filter(models.id == Number).delete()
        elif InputState == "run":
            launchCMD = request.form.get("LcCompiler") + " " + request.form.get("LCurl")
            os.system(launchCMD)
        elif InputState == "stop":
            InputUrl = request.form.get("url")
            print(InputUrl)
            port = int(urlparse(InputUrl).port)
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    pid = conn.pid
                    p = psutil.Process(pid)
                    p.kill()
                    break
            return jsonify({'response': "YES"})
    return redirect("/")

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
            db.session.remove()
            login_error = '注册成功'
            page = 'login'
        else:
            login_error = '两次密码不一'
    else:
        page = "register"
        login_error = '完整填写信息'
    return redirect('/')

@app.get('/logout')#登出
def logout():
    close_application()

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
def ai(ModelID:str,question:str):
    response = ""
    openai.api_base = db.session.query(models.url).filter(models.name == ModelID).one()[0]
    openai.api_key = db.session.query(models.APIkey).filter(models.name == ModelID).one()
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
    print(response, flush=True)
    return response

def llm(ModelID:str,question:str):
    response = requests.post(
        url = db.session.query(models.url).filter(models.name == ModelID).one()[0],
        data=json.dumps({"prompt": question,"history": []}),
        headers={'Content-Type': 'application/json'})
    return response.json()['history'][0][1]


#launch
if __name__ == '__main__':
    if cfg.read("BaseConfig","DevMode") == "True":
    #WEB MODE
        app.run(debug=cfg.read("BaseConfig","debug"),port=cfg.read("RemoteConfig","port"),host=cfg.read("RemoteConfig","host"))
    #GUI MODE
    else:
        try:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        except:
            pass
        FlaskUI(app=app,server='flask',port=cfg.read("RemoteConfig","port"),width=1000,height=800).run()
