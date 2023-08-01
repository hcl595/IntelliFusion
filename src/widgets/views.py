from widgets import widgets_blue
import psutil
from flask import Flask, render_template, jsonify


@widgets_blue.route('/Core_Percent')
def CorePercent():
    return render_template("CPU_Percent.html")

@widgets_blue.route('/Ram_Percent')
def RAMPercent():
    return render_template("Memory_Percent.html") 

@widgets_blue.post('/Get_CPU_Percent')
def Get_CPU_Precent():
    cpu_percent = psutil.cpu_percent()
    return jsonify({'data':cpu_percent})

@widgets_blue.post('/Get_RAM_Percent')
def Get_RAM_Precent():
    memory_percent = psutil.virtual_memory().percent
    return jsonify({'data':memory_percent})