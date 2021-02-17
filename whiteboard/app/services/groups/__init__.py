from flask import Blueprint
from flask_restful import Api

groups = Blueprint("groups", __name__)
api = Api(groups)

from . import views
