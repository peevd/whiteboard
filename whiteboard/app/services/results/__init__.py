from flask import Blueprint
from flask_restful import Api

results = Blueprint("results", __name__)
api = Api(results)

from . import views

