#headers
from flask import Flask

#configs
app = Flask(__name__)
app.config.from_object(__name__)

#setup
response = {
        'response': 'micro-python和Ardu',
        'history': [['你好', '你好👋！我是人工智能助手 ChatGLM-6B，很高兴见到你，欢迎问我任何问题。']],
        'status': 200,
        'time': '2023-05-13 18:56:53'}
port = "18365"
host = "127.0.0.1"

@app.post('/')
def upload():
    return response

if __name__ == '__main__':
    app.run(debug=True,port=port,host=host)
