from flask import Blueprint
from flask_restful import Api

payments = Blueprint("payments", __name__)
api = Api(payments)

from . import views

