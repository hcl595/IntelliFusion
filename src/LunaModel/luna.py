try:
    from cli_demo import chat
    
    def summary(summary:str) -> str:
        modelOutput = chat("概括以下内容"+summary)
        return modelOutput
    
    def mergeMessages(messages:list) -> str:
        modelOutput = chat("合并以下内容为一段完整内容："+messages)
        return modelOutput
    
    
    
except:
    def summary(summary:str) -> str:
        return "modelOutput"



