from flask import Blueprint
from flask_restful import Api

chatEvents = Blueprint("chatEvents", __name__)
api = Api(chatEvents)

from . import events

