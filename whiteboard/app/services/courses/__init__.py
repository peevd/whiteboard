from flask import Blueprint
from flask_restful import Api

courses = Blueprint("courses", __name__)
api = Api(courses)

from . import views
