from widgets import widgets_blue
import psutil
from pyecharts import options as opts
from pyecharts.charts import Pie
from flask import Flask, render_template

@widgets_blue.route('/')
def widgets_blue_root():
    return render_template('CorePercent.html')

@widgets_blue.route("./static/js/echarts.min.js")
def js():
    with open("./static/js/echarts.min.js", "rb") as f:
        data = f.read().decode()
    return data

@widgets_blue.route('/CorePercent')
def CorePercent():
    cpu_percent = psutil.cpu_percent()
    c = Pie().add("", [["占用", cpu_percent], ["空闲", 100 - cpu_percent]])
    return c.render_embed().replace(
        "https://assets.pyecharts.org/assets/v5/echarts.min.js",
        "./static/js/echarts.min.js",
    )

@widgets_blue.route('/RamPercent')
def RAMPercent():
    memory_percent = psutil.virtual_memory().percent
    c = Pie().add("", [["占用", memory_percent], ["空闲", 100 - memory_percent]])
    return c.render_embed().replace(
        "https://assets.pyecharts.org/assets/v5/echarts.min.js",
        "./static/js/echarts.min.js",
    )