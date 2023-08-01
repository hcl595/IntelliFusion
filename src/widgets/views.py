from widgets import widgets_blue
import psutil
from flask import Flask, render_template


@widgets_blue.route('/Core_Percent')
def CorePercent():
    cpu_percent = psutil.cpu_percent()
    return render_template("CPU_Percent.html",
                           cpu_percent = cpu_percent)

@widgets_blue.route('/Ram_Percent')
def RAMPercent():
    memory_percent = psutil.virtual_memory().percent
    return render_template("RAM_Percent.html",
                           memory_percent = memory_percent) 