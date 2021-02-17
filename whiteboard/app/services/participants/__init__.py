from flask import Blueprint
from flask_restful import Api

participants = Blueprint("participants", __name__)
api = Api(participants)

from . import views
