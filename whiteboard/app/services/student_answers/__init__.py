from flask import Blueprint
from flask_restful import Api

studentAsnswers = Blueprint("studentAsnswers", __name__)
api = Api(studentAsnswers)

from . import views

