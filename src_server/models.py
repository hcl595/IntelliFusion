from data import Models, Sessions, History
import subprocess
import psutil
from concurrent.futures import ProcessPoolExecutor
from typing import TypedDict
import mistune
import requests
import json

from config import Settings
setting = Settings()
Version = setting.read("package","Version")

if setting.read("AdvancedConfig","Luna") == "True":
    from LunaModel.luna import summary

class Message(TypedDict):
    role: str
    content: str

def create_session(model_id:int, model_summary:bool = True,):
    '''
    comment是输入时的备注 用于给会话命名
    model_id是输入会话所使用的模型在数据库中的ID
    '''
    if model_id is None:
        raise ValueError
    if model_summary:
        model_comment = Models.get(Models.id == model_id).modelName
        # 创建会话
        Sessions.create(
            model_id = model_id,
            modelSummary = model_summary,
            comment = model_comment,
            )
        return "Succeed"
    else:
        # 创建会话
        Sessions.create(
            model_id = model_id,
            modelSummary = model_summary,
            comment = model_comment,
            )
        model_summary = False
        return "Succeed"

def update_session(SessionID: int):
    '''
    SessionID 会话在数据库中的ID
    '''
    if SessionID is None:
        raise ValueError

    model_comment = summary(getHistory(SessionID))
    # model_comment = summary(History.select().where(History.session_id == Sessions.get(Sessions.id == SessionID).id))
    Sessions.update(comment = model_comment).where(Sessions.id == SessionID).execute()
    return "Succeed"


def getHistory(SessionID: int) -> list[Message]:
    '''
    SessionID 会话在数据库中的ID
    '''
    messages = []
    for r in History.select().where(History.session_id == SessionID):
        r: History
        assert isinstance(r.UserInput, str)
        assert isinstance(r.response, str)
        question: Message = {"role": "user", "content": r.UserInput}
        response_model: Message = {"role": "assistant", "content": r.response}
        messages.append(question)
        messages.append(response_model)    
    return messages


def request_OpenAI(SessionID: int, Userinput: str,stream: bool = True):
    '''
    SessionID 会话在数据库中的ID
    Userinput 用户输入的内容
    stream    是否需要流式传输
    '''
    #Setup
    messages = getHistory(SessionID)
    response = ""
    if SessionID is None or Userinput is None:
        raise ValueError

    #Check lib & auto install
    try:
        from openai import OpenAI
        
    except ImportError:
        with ProcessPoolExecutor() as p:
            try:
                p.submit(subprocess.run, "pip install "+"openai")
            except psutil.AccessDenied:
                raise ImportError("No moduel named"+"openai")

    #Get API KEY
    try:
        Model_ID = Models.get(Models.id == Sessions.get(Sessions.id == SessionID).model_id)
    except:
        raise Models

    #Request ai
    question: Message = {"role": "user", "content": Userinput}
    messages.append(question)
    # TODO: The 'openai.api_base' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(base_url=(Model_ID.url))'
    # openai.api_base = (Model_ID.url)
    client = OpenAI(base_url=Model_ID.url,api_key=Model_ID.api_key)
    for chunk in client.chat.completions.create(model=Model_ID.name,
    messages=messages,
    stream=True,
    temperature=0):
        if stream == True:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="", flush=True)
                response = response + chunk.choices[0].delta.content
                response_out = mistune.html(response)
                yield response_out
        else:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="", flush=True)
                response = response + chunk.choices[0].delta.content
                response = mistune.html(response)
            return response

    #Save conversation
    History.create(
        session_id = SessionID,
        UserInput = Userinput,
        response = response_out,
    )
    update_session(SessionID)

def request_ZhipuAI(SessionID: int, Userinput: str,stream: bool = True):
    '''
    SessionID 会话在数据库中的ID
    Userinput 用户输入的内容
    stream    是否需要流式传输
    '''
    #Setup
    messages = getHistory(SessionID)
    # messages = []
    response = ""
    if SessionID is None or Userinput is None:
        raise ValueError

    #Check lib & auto install
    try:
        from zhipuai import ZhipuAI
    except ImportError:
        with ProcessPoolExecutor() as p:
            try:
                p.submit(subprocess.run, "pip install "+"zhipuai")
            except psutil.AccessDenied:
                raise ImportError("No moduel named"+"zhipuai")

    #Get API KEY
    try:
        Model_ID = Models.get(Models.id == Sessions.get(Sessions.id == SessionID).model_id)
    except:
        raise Models

    #Request AI
    question: Message = {"role": "user", "content": Userinput}
    messages.append(question)
    client = ZhipuAI(api_key = Model_ID.api_key)
    ZhipuAI.api_base = (Model_ID.url)
    for chunk in client.chat.completions.create(
        model=Model_ID.name,
        messages=messages,
        stream=True,
        temperature=0,
    ):
        if stream == True:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="", flush=True)
                response = response + chunk.choices[0].delta.content
                response_out = mistune.html(response)
                yield response_out
        else:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="", flush=True)
                response = response + chunk.choices[0].delta.content
                response = mistune.html(response)
            return response

    #Save conversation
    History.create(
        session_id = SessionID,
        UserInput = Userinput,
        response = response_out,
    )
    update_session(SessionID)


def request_Ollama(SessionID: int, Userinput: str,stream: bool = True):
    '''
    SessionID 会话在数据库中的ID
    Userinput 用户输入的内容
    stream    是否需要流式传输
    '''
    #Setup
    messages = getHistory(SessionID)
    # messages = []
    response = ""
    if SessionID is None or Userinput is None:
        raise ValueError

    #Check lib & auto install
    try:
        from ollama import Client
    except ImportError:
        with ProcessPoolExecutor() as p:
            try:
                p.submit(subprocess.run, "pip install "+"ollama")
            except psutil.AccessDenied:
                raise ImportError("No moduel named"+"zhipuai")

    #Get API KEY
    try:
        Model_ID = Models.get(Models.id == Sessions.get(Sessions.id == SessionID).model_id)
    except:
        raise

    #Request AI
    question: Message = {"role": "user", "content": Userinput}
    messages.append(question)

    for chunk in Client(host=Models.get(Models.id == Model_ID).url).chat(
        model=Model_ID.name,
        messages=messages,
        stream=stream,
        ):

        print(chunk['message']['content'], end='', flush=True)
        if stream == True:
            if hasattr(chunk.message, "content"):
                print(chunk.message.content, end="", flush=True)
                response = response + chunk.message.content
                response_out = mistune.html(response)
                yield response_out
            else:
                yield "I'm a chat robot, How can I assist you today?"
        else:
            if hasattr(chunk.choices[0].delta, "content"):
                print(chunk.choices[0].delta.content, end="", flush=True)
                response = chunk.choices[0].delta.content
                response = mistune.html(response)
                return response
            else:
                return "I'm a chat robot, How can I assist you today?"

    #Save conversation
    History.create(
        session_id = SessionID,
        UserInput = Userinput,
        response = response_out,
    )
    update_session(SessionID)


def request_Json(SessionID: int, Userinput: str):
    if SessionID is None or Userinput is None:
        raise ValueError
    try:
        Model_ID = Models.get(Models.id == Sessions.get(Sessions.id == SessionID).model_id).id
    except:
        raise ValueError("SessionID Error")
    response = requests.post(
        url=Models.get(Models.id == Model_ID).url,
        data=json.dumps({"prompt": Userinput, "history": []}),
        headers={"Content-Type": "application/json"},
    )
    response_out = mistune.html(response.json()["history"][0][1])
    History.create(
        session_id= SessionID,
        UserInput = Userinput,
        response=response_out,
    )
    return response_out


