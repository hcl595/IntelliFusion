from widgets import widgets_blue
import psutil
from flask import Flask, render_template

@widgets_blue.route('/')
def widgets_blue_root():
    return render_template('CorePercent.html')

@widgets_blue.route('/CorePercent')
def CorePercent():
    cpu_percent = psutil.cpu_percent()
    return cpu_percent

@widgets_blue.route('/RamPercent')
def RAMPercent():
    memory_percent = psutil.virtual_memory().percent
    return memory_percent