#headers
from flask import Flask, render_template, redirect, request
from flaskwebgui import FlaskUI
import ctypes
import requests
import json

#configs
app = Flask(__name__)
app.config.from_object(__name__)

#setup
global result,historys
response = {
        'response': '你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。',
        'history': [['你好', '你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。']],
        'status': 200,
        'time': '2023-05-13 18:56:53'}
result = None
historys = response['history']
historysO = []
historysA = []
dev_mode = 'True'
port = "8000"
host = "127.0.0.1"

@app.route('/show')
def show():
    return render_template('show.html')

@app.route('/')
def root():
    return render_template('main.html',
                           result = result,
                           historys = historysA,
                           username = "Login",)

@app.post('/')
def upload():
    global result,historys,historysO
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
    historysA.append(historys[0])
    print(historysA)
    return redirect('/')

@app.post('/chatgpt')
def gpt_response():
    message = request.form['message']
    response = send_message(message)
    print(response)
    return response



#functions
def send_message(message):
    api_key = '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'  # 将YOUR_API_KEY替换为你的OpenAI API密钥

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

@app.errorhandler(404)
def error404(error):
    return render_template('404.html'),404

if __name__ == '__main__':
    if dev_mode == "True":
    #WEB MODE
        app.run(debug=True,port=port,host=host)
    #GUI MODE
    else:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        FlaskUI(app=app,server='flask',port=port,width=1000,height=800).run()
