from . import api
import os
from ..utils import allowed_file

from flask_restful import reqparse
from flask import current_app as app
from flask_restful import Resource
import subprocess

import instance.config

parser = reqparse.RequestParser()

parser_post = parser.copy()
parser_post.add_argument("file_path", required=True,
                         location="json",
                         help="Missing argument!")


class PresentHandler(Resource):
    def post(self):
        args = parser_post.parse_args()

        file_path = args["file_path"]
        file_name = file_path.split("/")[-1]
        file_path = '%s%s' % (app.config['PRESENT_DIR'], file_path)

        ALLOWED_EXTENSIONS = app.config["ALLOWED_EXTENSIONS"]

        is_file = os.path.isfile(file_path)
        if is_file and allowed_file(file_name, ALLOWED_EXTENSIONS):
            try:
                subprocess.call(
                    ['soffice', '--headless', '--convert-to',
                     'svg:draw_svg_Export', '--outdir',
                     os.path.dirname(file_path), file_path]
                )
                os.remove(file_path)

                return {
                    "message": "Ok"
                }, 200

            except SystemError:
                return {
                    "message": "Something go wrong! Please try again! 1"
                }, 409
        else:
            return {
                "message": "Something go wrong! Please try again! 2"
            }, 409


api.add_resource(PresentHandler, "/api/pHandler")

