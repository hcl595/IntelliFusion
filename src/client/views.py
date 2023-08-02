import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

import openai
import psutil
import requests
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, request
from django.shortcuts import render
from flaskwebgui import close_application
from loguru import logger

from client.config import Settings
from client.models import ModelList

# Create your views here.
LLM_response = []
GLM_response = []
result = None
NeedLogin = True

#SetUp
cfg = Settings()
pool=ThreadPoolExecutor()
logger.add('./data/log.log')

#main
def root(InputRequest):
    Models = ModelList.objects.all().values("id","order","type","name","url","APIKey","LaunchCompiler","LaunchPath")
    logger.debug(type(Models[0]))
    try:
        ThirdBoxURL = ModelList.objects.filter(ModelList.name == cfg.read("ModelConfig","ThirdModel")).first()
    except:
        ThirdBoxURL = None
    return render(InputRequest,'main.html',
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
                'TimeOut' : cfg.read("BaseConfig","TimeOut"),
                'username' : 'NONE'})

def request_api_response(InputRequest):
    global result,LLM_response
    InputInfo = request.POST['userinput']
    InputModel =request.POST["modelinput"]
    print(InputInfo,InputModel)
    LLM_response = llm(InputModel,InputInfo)
    return JsonResponse(InputRequest,{'response': LLM_response})

def request_openai_response(InputRequest):
    global GLM_response
    InputInfo = InputRequest.POST.get('userinput')
    InputModel = InputRequest.POST.get("modelinput")
    logger.debug("request:{}.model:{}",InputInfo,InputModel)
    openai_response = ai(InputModel,InputInfo)
    return JsonResponse(InputRequest,{'response': openai_response})#ajax返回

def EditSetting(InputRequest):
    InputDefaultModel = InputRequest.POST.get("DefaultModel")
    InputSecondModel = InputRequest.POST.get("SecondModel")
    InputThirdModel = InputRequest.POST.get("ThirdModel")
    InputiPv4 = InputRequest.POST.get("iPv4")
    InputPort = InputRequest.POST.get("Port")
    InputWebMode = InputRequest.POST.get("Mode")
    InputclientMode = InputRequest.POST.get("BugM")
    cfg.write("BaseConfig","devmode",InputWebMode)
    cfg.write("BaseConfig","client",InputclientMode)
    cfg.write("RemoteConfig","host",InputiPv4)
    cfg.write("RemoteConfig","port",InputPort)
    cfg.write("ModelConfig","DefaultModel",InputDefaultModel)
    cfg.write("ModelConfig","SecondModel",InputSecondModel)
    cfg.write("ModelConfig","ThirdModel",InputThirdModel)
    return HttpResponseRedirect("/")

def ManageModel(InputRequest):
    InputState = InputRequest.POST.get("state")
    InputID = InputRequest.POST.get("number")
    InputType = InputRequest.POST.get("type")
    InputName = InputRequest.POST.get("comment")
    InputUrl = InputRequest.POST.get("url")
    InputAPIkey = InputRequest.POST.get("APIkey")
    LaunchCompiler = InputRequest.POST.get("LcCompiler")
    LaunchPath = InputRequest.POST.get("LcUrl")
    logger.debug(InputID)
    try:
        port = int(urlparse(InputUrl).port)
    except:
        port = 80
    if InputState == "edit":
        ModelList.objects.filter(ModelList.id == InputID).update(
            ModelList.type == InputType,
            ModelList.name == InputName,
            ModelList.url == InputUrl,
            ModelList.APIKey == InputAPIkey,
            ModelList.LaunchCompiler == LaunchCompiler,
            ModelList.LaunchPath == LaunchPath,
        )
        return JsonResponse({'response': "complete"})
    elif InputState == "del":
        ModelList.objects.filter(ModelList.id == InputID).delete()
        return JsonResponse({'response': "complete"})
    elif InputState == "run":
        launchCMD = InputRequest.POST.get("LcCompiler") + " " + InputRequest.POST.get("LcUrl")
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
                             ,InputName,cfg.read('BaseConfig',"TimeOut"),LaunchCompiler,LaunchPath)
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
        n =  ModelList.objects.create(
            name = InputName,
            order = 1,
            type = InputType,
            url = InputUrl,
            APIKey = InputAPIkey,
            LaunchCompiler = LaunchCompiler,
            LaunchPath = LaunchPath,
        )
        n.save()
        return JsonResponse({'response': "complete"})
    

def logout(InputRequest):
    logger.info('Application Closed')
    close_application()

def js(InputRequest):
    with open("src\static\js\echarts.min.js", "rb") as f:
        data = f.read().decode()
    return data

def test(InputRequest):
    a = InputRequest.POST.get("")
    return render(InputRequest,'test.html')

#functions
def ai(ModelID:str,question:str): #TODO:把response转化为json
    response = ""
    openai.api_base = ModelList.objects.filter(ModelList.name == ModelID).get(ModelList.url)
    openai.api_key = ModelList.objects.filter(ModelList.name == ModelID).get(ModelList.APIKey)
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
                ,ModelID,ModelList.objects.filter(ModelList.name == ModelID).get(ModelList.url),question,response)
    return response

def llm(ModelID:str,question:str):
    response = requests.post(
        url = ModelList.objects.filter(ModelList.name == ModelID).get(ModelList.url),
        data=json.dumps({"prompt": question,"history": []}),
        headers={'Content-Type': 'application/json'})
    return response.json()['history'][0][1]

