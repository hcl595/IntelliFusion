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

#configs
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'UMAVERSIONOPONEPTWO'

#setup
setup()
cfg = Settings()
global historys,NeedLogin,GPT_response
response = {
        'response': '',
        'history': [['', '']],
        'status': 200,
        'time': '1234-05-06 07:08:09'}
GPT_response = {
        'response': '',
        'history': [['', '']],
        'status': 200,
        'time': '1234-05-06 07:08:09'}
result = None
NeedLogin = True
historys = response['history']
OldHistorys = []
AllHistorys = []

#main
@app.route('/')#根目录
def root():
    ModelList = db.session.query(
                models.id,
                models.type,
                models.comment,
                models.url,
                models.port,
                models.LaunchUrl,).all()
    return render_template('main.html',
                           GPT_response = GPT_response,
                           result = result,
                           NeedLogin = NeedLogin,
                           ModelList = ModelList,
                           historys = AllHistorys,
                           username = session.get('username'),)

@app.post('/')#GLM请求与回复
def upload():
    global result,AllHistorys,OldHistorys
    input = request.form.get('inputInfo')
    response = requests.post('http://127.0.0.1:18365/',data=json.dumps({"prompt": input,"history": []}),headers={'Content-Type': 'application/json'})
    SrResponse = response.json()
    historys = SrResponse['history']
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
    print(AllHistorys)
    return redirect('/')

@app.post('/chatgpt')#GPT请求与回复
def gpt_response():
    global GPT_response
    message = request.form['user-input']
    GPT_response = ai(message)
    print(GPT_response)
    return redirect('/')


@app.post('/add')#添加模型
def AddModel():
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
    db.session.commit()
    return redirect('/')


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


@app.get('/logout')#登出
def logout():
    global login_error
    session.clear()
    login_error = '登出成功'
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


@app.get('/ModelList')
def GetModelList():
    ModelList = db.session.query(
            models.id,
            models.type,
            models.comment,
            models.url,
            models.port,
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
def ai(question:str):
    openai.api_base = "https://ai.fakeopen.com/v1/"
    openai.api_key = cfg.read("ModelConfig","APIKEY")
    model = "gpt-3.5-turbo"
    response = openai.ChatCompletion.create(
    model = model,
    messages = [
        {'role': 'system', 'content': "你是一名开发者"}, # 给gpt定义一个角色，也可以不写
        {'role': 'user', 'content': question} # 问题
    ],
    temperature = 0,
    stream = True
    )

    collected_chunks = []
    collected_messages = []
    messages = []


    print(f"OpenAI({model}) :  ",end="")
    for chunk in response:
        message = chunk["choices"][0]["delta"].get("content","")
        print(message,end="")

        messages.append(message,end="")

        collected_chunks.append(chunk)

        chunk_message = chunk["choices"][0]["delta"]
        collected_messages.append(chunk_message)
    return messages


#launch
if __name__ == '__main__':
    if cfg.read("BaseConfig","DevMode") == "True":
    #WEB MODE
        app.run(debug=True,port=cfg.read("RemoteConfig","port"),host=cfg.read("RemoteConfig","host"))
    #GUI MODE
    else:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        FlaskUI(app=app,server='flask',port=cfg.read("RemoteConfig","port"),width=1000,height=800).run()
