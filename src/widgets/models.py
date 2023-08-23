import openai
import requests
import json
from data import History, Models, Widgets
from typing import Literal, TypedDict

class Message(TypedDict):
    role: Literal["admin"] | Literal["user"]
    content: str

def ai(ModelID: str, question_in: str):
    response = ""
    openai.api_base = (Models.get(Models.name == ModelID).url)
    messages = []
    for r in History.select().where(History.Model == ModelID):
        r: History
        assert isinstance(r.UserInput, str)
        assert isinstance(r.response, str)
        question: Message = {"role": "user", "content": r.UserInput}
        response_model: Message = {"role": "assistant", "content": r.response}
        messages.append(question)
        messages.append(response_model)
    question: Message = {"role": "user", "content": question_in}
    messages.append(question)
    openai.api_key = (
        Models.get(Models.name == ModelID).api_key
    )
    for chunk in openai.ChatCompletion.create(
        model=ModelID,
        messages=messages,
        stream=True,
        temperature=0,
    ):
        if hasattr(chunk.choices[0].delta, "content"):
            print(chunk.choices[0].delta.content, end="", flush=True)
            response = response + chunk.choices[0].delta.content
    response = str.replace(response,"\n","<br/>")
    last_code_block_index: int = -1
    is_code_block_start = True
    while (last_code_block_index := response.find("```")) != -1:
        if is_code_block_start:
            response=response.replace("```", "<pre>", 1)
        else:
            response=response.replace("```", "</pre>", 1)
        last_code_block_index=-1
        is_code_block_start=not is_code_block_start
    return response


def llm(ModelID: str, question: str):
    response = requests.post(
        url=Models.get(Models.name == ModelID).url,
        data=json.dumps({"prompt": question, "history": []}),
        headers={"Content-Type": "application/json"},
    )
    response = str.replace(response.json()["history"][0][1],"\n","<br/>")
    last_code_block_index: int = -1
    is_code_block_start = True
    while (last_code_block_index := response.find("```")) != -1:
        if is_code_block_start:
            response=response.replace("```", "<pre>", 1)
        else:
            response=response.replace("```", "</pre>", 1)
        last_code_block_index=-1
        is_code_block_start=not is_code_block_start
    return response


