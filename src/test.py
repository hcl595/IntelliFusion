historys = [['用python写一段代码', '好的，以下是一个简单的 Python 代码，它会提示用户输入两个数字，然后计算它们的和并输出结果：\n\n```\nnum1 = int(input("请输入第一个数字： "))\nnum2 = int(input("请输入第二个数字： "))\n\nsum = num1 + num2\n\nprint("这两个数字的和是： ", sum)\n```\n\n运行该代码后，它会提示用户输入两个数字，然后将它们相加，并将结果输出到屏幕上。用户输入的数字会被转换为整数类型，并将其添加到变量 `sum` 中，最后计算 `sum` 的值，并使用 `print()` 函数输出结果。']]
historysO = []
historysA = []

for i in range(len(historys)):
    history = historys[i]
    for i in range(len(history)):
        tmp = history[i]
        tmp = str.replace(tmp,"\n","<br/>")
        history[i] = tmp
historysA.append(historys)
print(historysA)