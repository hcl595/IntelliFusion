#headers
from flask import Flask, render_template, redirect, request, session
from flaskwebgui import FlaskUI
from config import Settings
import data as db
from data import userInfo,models
import ctypes
import requests
import json

#configs
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'UMAVERSIONOPONEPONE'

#setup
cfg = Settings()
global historys,NeedLogin,KeepLogin
response = {
        'response': '你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。',
        'history': [['你好', '你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。']],
        'status': 200,
        'time': '2023-05-13 18:56:53'}
result = None
NeedLogin = True
historys = response['history']
historysO = []
historysA = []
dev_mode = cfg.read("BaseConfig","DevMode")
KeepLogin = cfg.read("BaseConfig","KeepLogin")
host = cfg.read("RemoteConfig","host")
port = cfg.read("RemoteConfig","port")
api_key = cfg.read("ModelConfig","APIKEY")



@app.route('/')
def root():
    return render_template('main.html',
                           result = result,
                           NeedLogin = NeedLogin,
                           historys = historysA,
                           username = session.get('username'),)

@app.post('/')
def upload():
    global result,historys,historysO
    input = request.form.get('inputInfo')
    response = requests.post('http://127.0.0.1:1365/',data=json.dumps({"prompt": input,"history": []}),headers={'Content-Type': 'application/json'})
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
    historysA.append(historys[0])
    print(historysA)
    return redirect('/')

@app.post('/chatgpt')
def gpt_response():
    message = request.form['message']
    response = send_message(message)
    print(response)
    return response


@app.get('/settings')
def UpdateSettings():
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
                if KeepLogin == 'True':
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
def send_message(message):
    api_key = api_key  # 将YOUR_API_KEY替换为你的OpenAI API密钥

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    data = {
        'messages': [{'role': 'system', 'content': 'You are a user'}, {'role': 'user', 'content': message}]
    }

    response = requests.post('https://chatgpt-api.shn.hk/v1/', headers=headers, json=data)
    reply = response.json()['choices'][0]['message']['content']
    return reply

if __name__ == '__main__':
    if dev_mode == "True":
    #WEB MODE
        app.run(debug=True,port=port,host=host)
    #GUI MODE
    else:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        FlaskUI(app=app,server='flask',port=port,width=1000,height=800).run()
