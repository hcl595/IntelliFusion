import json
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import openai
import psutil
import requests
from client.config import Settings
from client.models import ModelList
from django.http import ( HttpResponseRedirect, JsonResponse,
                         request)
from django.shortcuts import render
from flaskwebgui import  close_application
from loguru import logger
from pyecharts.charts import Pie

logger.add('./data/log.log')

# Create your views here.
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

cfg = Settings()
pool=ThreadPoolExecutor()

#main
def root(request):
    print(login_error)
    Models = ModelList.objects.all()
    try:
        ThirdBoxURL = ModelList.objects.filter(ModelList.name == cfg.read("ModelConfig","ThirdModel")).first()
    except:
        ThirdBoxURL = None
    return render(request,'main.html',
                {'result' : result,
                'NeedLogin' : NeedLogin,
                'ModelList' : Models,
                'ModelCount' : 3,
                'historys' : LLM_response,
                'ThirdBoxURL' : ThirdBoxURL,
                'host' : cfg.read("RemoteConfig","host"),
                'port' : cfg.read("RemoteConfig","port"),
                'Mode' : cfg.read("BaseConfig","devmode"),
                'BugM' : cfg.read("BaseConfig","client"),
                'DefaultModel' : cfg.read("ModelConfig","DefaultModel"),
                'SecondModel' : cfg.read("ModelConfig","SecondModel"),
                'ThirdModel' : cfg.read("ModelConfig","ThirdModel"),
                'username' : 'NONE'})

def request_api_response():
    global result,LLM_response
    InputInfo = request.form['userinput']
    InputModel =request.form["modelinput"]
    print(InputInfo,InputModel)
    LLM_response = llm(InputModel,InputInfo)
    return JsonResponse({'response': LLM_response})

def request_openai_response():
    global GLM_response
    InputInfo = request.form['userinput']
    InputModel = request.form["modelinput"]
    logger.client("request:{}.model:{}",InputInfo,InputModel)
    openai_response = ai(InputModel,InputInfo)
    return JsonResponse({'response': openai_response})#ajax返回

def EditSetting():
    InputDefaultModel = request.POST.get("DefaultModel")
    InputSecondModel = request.form.get("SecondModel")
    InputThirdModel = request.form.get("ThirdModel")
    InputiPv4 = request.form.get("iPv4")
    InputPort = request.form.get("Port")
    InputWebMode = request.form.get("Mode")
    InputclientMode = request.form.get("BugM")
    cfg.write("BaseConfig","devmode",InputWebMode)
    cfg.write("BaseConfig","client",InputclientMode)
    cfg.write("RemoteConfig","host",InputiPv4)
    cfg.write("RemoteConfig","port",InputPort)
    cfg.write("ModelConfig","DefaultModel",InputDefaultModel)
    cfg.write("ModelConfig","SecondModel",InputSecondModel)
    cfg.write("ModelConfig","ThirdModel",InputThirdModel)
    return HttpResponseRedirect("/")

def ManageModel():
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
    logger.client(LaunchCompiler)
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
        return JsonResponse({'response': "complete"})
    elif InputState == "del":
        db.session.query(models).filter(models.id == InputID).delete()
        db.session.commit()
        return JsonResponse({'response': "complete"})
    elif InputState == "run":
        launchCMD = request.form.get("LcCompiler") + " " + request.form.get("LcUrl")
        pool.submit(subprocess.run, launchCMD)
        count = 0
        while True:
            for conn in psutil.net_connections():
                if conn.laddr.port == port:
                    return JsonResponse({'response': "complete"})
            count += 1
            time.sleep(1)
            if count == cfg.read('BaseConfig',"TimeOut"):
                logger.error('Model: {} launch maybe failed,because of Time Out({}),LaunchCompilerPath: {},LaunchFile: {}'
                             ,InputComment,cfg.read('BaseConfig',"TimeOut"),LaunchCompiler,LaunchUrl)
                return JsonResponse({'response': "TimeOut"})
    elif InputState == "stop":
        for conn in psutil.net_connections():
            if conn.laddr.port == port:
                pid = conn.pid
                p = psutil.Process(pid)
                p.kill()
                break
        return JsonResponse({'response': "complete"})
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
        return JsonResponse({'response': "complete"})

# def login_check():
#     global login_error,choose,page
#     account = request.form.get("logid")
#     password = request.form.get("password")
#     acc_result = db.session.query(userInfo.account).filter(userInfo.account == account).first()
#     pwd_result = db.session.query(userInfo.password).filter(userInfo.account == account,userInfo.password == password).first()
#     if account and password:
#         if acc_result:
#             if pwd_result:
#                 session['username']=account
#                 session['password']=password
#                 uid =db.session.query(userInfo.id).filter(userInfo.account==account,userInfo.password==password).first()
#                 uid = uid[0]
#                 session['uid']= uid
#                 if cfg.read("BaseConfig","KeepLogin") == 'True':
#                     session.permanent=True
#                 login_error = "已登录"
#                 choose = 0
#                 return HttpResponseRedirect('/')
#             else:
#                 page = 'login'
#                 login_error = "密码错误"
#                 return HttpResponseRedirect('/')
#         else:
#             page = 'login'
#             login_error = "未知用户名"
#             return HttpResponseRedirect('/')
#     else:
#         page = 'login'
#         login_error = "请写入信息"
#         return HttpResponseRedirect('/')
    
# def register():
#     global login_error,page
#     account = request.form.get("reg_txt")
#     mail = request.form.get("email")
#     password = request.form.get("set_password")
#     check_password = request.form.get("check_password")
#     if account and password and mail:
#         if password == check_password:
#             info = db.userInfo(
#                             account=account,
#                             password=password,
#                             mail=mail,)
#             db.session.add(info)
#             db.session.commit()
#             login_error = '注册成功'
#             logger.info('User: {account} ,has created an account.Password: {password}',account=account,password=password)
#             page = 'login'
#         else:
#             login_error = '两次密码不一'
#     else:
#         page = "register"
#         login_error = '完整填写信息'
#     return HttpResponseRedirect('/')

def logout():
    logger.info('Application Closed')
    close_application()

def WidgetsCorePercent():
    cpu_percent = psutil.cpu_percent()
    c = Pie().add("", [["占用", cpu_percent], ["空闲", 100 - cpu_percent]])
    return c.render_embed().replace(
        "https://assets.pyecharts.org/assets/v5/echarts.min.js",
        "./static/js/echarts.min.js",
    )

def WigetsRamPercent():
    memory_percent = psutil.virtual_memory().percent
    c = Pie().add("", [["占用", memory_percent], ["空闲", 100 - memory_percent]])
    return c.render_embed().replace(
        "https://assets.pyecharts.org/assets/v5/echarts.min.js",
        "/static/js/echarts.min.js",
    )

def js():
    with open("src\static\js\echarts.min.js", "rb") as f:
        data = f.read().decode()
    return data

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

