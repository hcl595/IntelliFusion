#headers
from flask import Flask, render_template, redirect, request, session, json
import openai
from flaskwebgui import FlaskUI
from config import Settings
import data as db
from data import userInfo,models,setup
import ctypes
import requests
import json
import os

#configs
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'UMAVERSIONOPONEPTRE'

#setup
setup()
cfg = Settings()
global historys,NeedLogin,GPT_response
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

    ModelList = db.session.query(
                models.id,
                models.type,
                models.name,
                models.url,
                models.APIkey,  
                models.LaunchCompiler,
                models.LaunchUrl,).all()
    
    #Settings
    return render_template('main.html',
                            GPT_response = GPT_response,
                            GLM_response = GLM_response,
                            result = result,
                            NeedLogin = NeedLogin,
                            ModelList = ModelList,
                            historys = LLM_response,
                            host = cfg.read("RemoteConfig","host"),
                            port = cfg.read("RemoteConfig","port"),
                            Mode = cfg.read("BaseConfig","devmode"),
                            BugM = cfg.read("BaseConfig","debug"),
                            Key = cfg.read("ModelConfig","APIKEY"),
                            username = session.get('username'),)


@app.route("/exchange")
def LoadExchange():
    return redirect("/")


@app.post('/llm')#GLM请求与回复1
def upload():
    global result,LLM_response
    InputInfo = request.form.get('inputInfo')
    InputModel =request.form.get("InputMoel")
    LLM_response = llm(InputModel,InputInfo)
    return redirect('/')


@app.post('/openai')
def get_glm_response():
    global GLM_response
    InputInfo = request.form.get("user-input")
    InputModel =request.form.get("InputMoel")
    GLM_response = ai(InputModel,InputInfo)
    return redirect("/")


@app.post('/exchange')#添加模型
def AddModel():
    Number = request.form.get("id")
    if Number == "-1":
        InputType = request.form.get("type")
        InputComment = request.form.get("comment")
        InputUrl = request.form.get("url")
        InputPort = request.form.get("Port")
        LaunchUrl = request.form.get("LCurl")
        info = db.models(
                    type = InputType,
                    comment = InputComment,
                    url = InputUrl,
                    port = InputPort,
                    LaunchUrl = LaunchUrl,)
        db.session.add(info)
    else:
        InputState = request.form.get(Number + "state")
        if InputState == "edit":
            InputID = request.form.get("id")
            InputType = request.form.get("type")
            InputComment = request.form.get("comment")
            InputUrl = request.form.get("url")
            InputAPIkey = request.form.get("APIkey")
            LaunchCompiler = request.form.get("LcCompiler")
            LaunchUrl = request.form.get("LCurl")
            db.session.query(db.models).filter(models.id == InputID).update({
                    db.models.type: InputType,
                    db.models.name: InputComment,
                    db.models.url: InputUrl,
                    db.models.APIkey: InputAPIkey,
                    db.models.LaunchCompiler: LaunchCompiler,
                    db.models.LaunchUrl: LaunchUrl,
                    })
        elif InputState == "del":
            InputID = request.form.get("id")
            db.session.query(models).filter(models.id == InputID).delete()
        elif InputState == "run":
            InputID = request.form.get("id")
            launchCMD = "python " + request.form.get("LCurl")
            os.system(launchCMD)
            print(launchCMD)
    db.session.commit()
    return redirect('/')


@app.post("/UpdateSettings")
def UpdateSettings():
    UpdateHost = request.form.get("host")
    UpdatePort = request.form.get("port")
    UpdateMode = request.form.get("mode")
    UpdateKey = request.form.get("key")

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
    global login_error
    session.clear()
    login_error = '登出成功'
    return redirect('/')


@app.get('/ModelList')
def GetModelList():
    ModelList = db.session.query(
            models.id,
            models.type,
            models.name,
            models.url,
            models.APIkey,
            models.LaunchCompiler,
            models.LaunchUrl,).all()
    return ModelList


@app.get("/SettingData")
def GetSettingData():
    iPv4 = cfg.read("RemoteSetting","host")
    port = cfg.read("RemoteSetting","port")
    return iPv4,port


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
    openai.api_base = db.session.query(models.url).filter(models.id == ModelID).one()
    openai.api_key = db.session.query(models.APIkey).filter(models.id == ModelID).one()
    model = db.session.query(models.name).filter(models.id == ModelID).one()
    for chunk in openai.ChatCompletion.create(
        model="chatglm2-6b",
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
    AllHistorys = []
    response = requests.post(
        db.session.query(models.url).filter(models.id == ModelID).one(),
        data=json.dumps({"prompt": question,"history": []}),
        headers={'Content-Type': 'application/json'})
    SourceResponse = response.json()
    historys = SourceResponse['history']
    for i in range(len(historys)):
        history = historys[i]
        for i in range(len(history)):
            tmp = history[i]
            tmp = str.replace(tmp,"\n","<br/>")
            last_code_block_index: int = -1
            is_code_block_start = True
            while (last_code_block_index := tmp.find("```")) != -1:
                if is_code_block_start:
                    tmp=tmp.replace("```", "<pre>", 1)
                else:
                    tmp=tmp.replace("```", "</pre>", 1)
                last_code_block_index=-1
                is_code_block_start=not is_code_block_start
            history[i] = tmp
    AllHistorys.append(historys[0])
    return AllHistorys



#launch
if __name__ == '__main__':
    if cfg.read("BaseConfig","DevMode") == "True":
    #WEB MODE
        app.run(debug=cfg.read("BaseConfig","debug"),port=cfg.read("RemoteConfig","port"),host=cfg.read("RemoteConfig","host"))
    #GUI MODE
    else:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        FlaskUI(app=app,server='flask',port=cfg.read("RemoteConfig","port"),width=1000,height=800).run()
