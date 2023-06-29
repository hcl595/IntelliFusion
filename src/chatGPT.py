import openai
import time
from config import Settings

cfg = Settings()

def ai(question:str):
  openai.api_base = "https://ai.fakeopen.com/v1"
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


  print(f"OpenAI({model}) :  ",end="")
  for chunk in response:
    time.sleep(0.1)
    message = chunk["choices"][0]["delta"].get("content","")
    print(message,end="")

    

    collected_chunks.append(chunk)

    chunk_message = chunk["choices"][0]["delta"]
    collected_messages.append(chunk_message)

  # full_reply_content = ''.join([m.get("content","") for m in collected_messages])
  # print(full_reply_content)

if __name__ == '__main__':
  while True:
    question = input("[提问]: ")
    startTime = time.time()

    # 请求
    ai(question)

    print("耗时:",time.time()-startTime)