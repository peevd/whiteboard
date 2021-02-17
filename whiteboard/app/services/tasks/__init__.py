from flask import Blueprint
from flask_restful import Api

tasks = Blueprint("tasks", __name__)
api = Api(tasks)

from . import views
