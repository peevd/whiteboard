from flask import Blueprint
from flask_restful import Api

approvalRequest = Blueprint("approvalRequest", __name__)
api = Api(approvalRequest)

from . import views

