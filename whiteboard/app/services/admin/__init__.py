from flask import Blueprint
from flask_restful import Api

adm = Blueprint("adm", __name__)
api = Api(adm)

from . import views

