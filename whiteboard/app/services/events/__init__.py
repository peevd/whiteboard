from flask import Blueprint
from flask_restful import Api

events = Blueprint("events", __name__)
api = Api(events)

from . import views

