from flask import Blueprint
from flask_restful import Api

p_handler = Blueprint("p_handler", __name__)
api = Api(p_handler)

from . import views

