from flask import Blueprint
from flask_restful import Api

keys = Blueprint("keys", __name__)
api = Api(keys)

from . import views

