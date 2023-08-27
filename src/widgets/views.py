from widgets import widgets_blue
import psutil
from flask import render_template, jsonify


@widgets_blue.post("/file")
def getfile():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename

    # 创建一个Tkinter根窗口
    root = Tk()
    root.withdraw()  # 隐藏根窗口

    # 弹出文件选择对话框
    file_path = askopenfilename()

    # 打印文件路径
    print("文件路径：", file_path)
    return jsonify(file_path)

@widgets_blue.route("/test")
def test_widgets():
    return render_template("test.html")

@widgets_blue.route("/Translate_Direct")
def TranslateTranslate():
    return render_template("Translate_Direct.html")

@widgets_blue.route('/CPU_Percent')
def CorePercent():
    return render_template("CPU_Percent.html")

@widgets_blue.route('/RAM_Percent')
def RAMPercent():
    return render_template("Memory_Percent.html") 

@widgets_blue.route('/GPU_Percent')
def GPURAMPercent():
    return render_template("GPU_Percent.html") 

@widgets_blue.post('/Get_CPU_Percent')
def Get_CPU_Precent():
    cpu_percent = psutil.cpu_percent()
    return jsonify({'data':cpu_percent})

@widgets_blue.post('/Get_RAM_Percent')
def Get_RAM_Precent():
    memory_percent = psutil.virtual_memory().percent
    return jsonify({'data':memory_percent})

@widgets_blue.post('/Get_GPU_Percent')
def Get_GPU_RAM_Precent():
    try:
        import pynvml
        pynvml.nvmlInit()
        handler = pynvml.nvmlDeviceGetHandleByIndex(0)
        meminfo = pynvml.nvmlDeviceGetMemoryInfo(handler)
        total = round(meminfo.total / 1024 / 1024, 2)
        used = round(meminfo.used / 1024 / 1024, 2)
        GPU_RAM_Per = round(used / total * 100, 1)
        return jsonify({'data':GPU_RAM_Per})
    except:
        memory_percent = 0
        return jsonify({'data':memory_percent})
