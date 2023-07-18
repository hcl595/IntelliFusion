from flask import Flask, Blueprint

widgets_blue = Blueprint('widgets', __name__, url_prefix='/widgets', static_folder='./static/', template_folder='./templates/')
from . import views

