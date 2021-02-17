from flask import Blueprint
from flask_restful import Api

users = Blueprint("users", __name__)
api = Api(users)

from . import views
