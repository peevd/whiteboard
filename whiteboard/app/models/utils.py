from flask import current_app as app
import os


"""++++++++++++++++++++++++++++   FILE GET URL   ++++++++++++++++++++++++++++"""


def add_course_image_url(id):
    UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
    filename = "picture_" + str(id)

    exists = os.path.isfile(UPLOAD_FOLDER + filename)
    pic_url = app.config["HOST"] + "static/courses/"
    if exists:
        pic_url += filename
        return pic_url
    else:
        pic_url = ""
        return pic_url

