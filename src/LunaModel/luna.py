
from LunaModel.cli_demo import chat


class LunaKit():
    # 定义一个函数，用于概括输入的文本
    def summary(self, summary:str):
        # 调用chat函数，将输入的文本作为参数传入，并将返回的结果赋值给modelOutput变量
        modelOutput = chat("概括以下内容"+summary)
        # 返回modelOutput变量的值
        return modelOutput

    def mergeMessages(self, messages:list):
        modelOutput = chat("合并以下内容为一段完整内容："+messages)
        return modelOutput




