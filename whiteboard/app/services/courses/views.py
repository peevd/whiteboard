from . import api
from ... import db
from ...models.courses import Course
from ...models.participants import Participant
from ...models.users import User
# from ...models.approval_requests import CourseApprovalRequest
from ..utils import parser, parse_token, auth_check, is_course_owner, \
        is_teacher, allowed_file, is_moderator, is_admin, \
        closing_course_reason_mail_body, mail_sender, is_student

import datetime
from flask import current_app as app, request
from flask_restful import Resource
import os
import shutil
import requests

parser_post_put = parser.copy()
parser_post_put.add_argument("name", required=True,
                             location="json",
                             help="Name cannot be blank!")
parser_post_put.add_argument("description", required=True,
                             location="json",
                             help="Description cannot be blank!")
parser_post_put.add_argument("price", required=True,
                             location="json",
                             help="Description cannot be blank!")

parser_get = parser.copy()
parser_get.add_argument("f", required=False,
                        location="args",
                        help="Unknowed argument!")
parser_get.add_argument("status", required=False,
                        location="args")
parser_get.add_argument("count", required=False,
                        location="args")

parser_active_put = parser.copy()
parser_active_put.add_argument("active", required=True,
                               type=bool,
                               location="json",
                               help="Misssing argument!")

parser_status_put = parser.copy()
parser_status_put.add_argument("status", required=True,
                               location="json",
                               help="Missing argument!")
parser_status_put.add_argument("reason", required=False,
                               location="json")


class NonAuthCourses(Resource):
    # GET all "open" courses without authentication
    def get(self):
        open_courses = Course.query.filter_by(status="open")

        return [x.toDict() for x in open_courses], 200


api.add_resource(NonAuthCourses, "/api/courses/index")


class Courses(Resource):
    # GET all registerd courses
    @auth_check
    def get(self):
        args = parser_get.parse_args()
        token = parse_token(args["Authorization"])
        if args["f"] is not None:
            if args["f"] == "all":
                if is_student(token):

                    all_courses = Course.query.filter_by(status="open")

                    return [x.toDict() for x in all_courses], 200
                else:
                    all_courses = Course.query

                    return [x.toDict() for x in all_courses], 200

            elif args["f"] == "mine":
                main_courses = Course.query.filter_by(owner_id=token["sub"])

                return [x.toDict() for x in main_courses], 200

            elif args["f"] == "coursesIn":
                mine_info = Participant.query.filter_by(user_id=token["sub"])
                courses_info = []

                for info in mine_info:
                    course = Course.query.filter_by(id=info.course_id).first()
                    courses_info.append(course.toDict())

                return courses_info, 200

            elif args["f"] == "coursesInCount":
                mine_info = Participant.query.filter_by(user_id=token["sub"])
                return {
                    "count": mine_info.count()
                }, 200

        elif args["count"] is not None:
            if args["status"] is not None:
                if args["status"] not in ["closed", "waiting_approval", "rejected", "open"]:
                    return {
                        "message": "Bad argument value!"
                    }, 400

                courses = Course.query.filter_by(status=args["status"])
                return {
                    "count": courses.count()
                }, 200
            else:
                all_courses = Course.query
                return {
                    "count": all_courses.count()
                }, 200
        else:
            return {
                "message": "Bad query arguments!"
            }, 400

    # Add course in register
    @auth_check
    def post(self):
        args = parser_post_put.parse_args()
        token = parse_token(args["Authorization"])

        if is_teacher(token):
            today = datetime.datetime.now()
            course = Course(
                name=args["name"],
                description=args["description"],
                status="closed",
                owner_id=token["sub"],
                price=args["price"],
                date=today.isoformat()
            )
            db.session.add(course)
            db.session.commit()

            b_data_path = app.config['B_DATA_FILES_DIR']
            path = b_data_path + "course_%d/" % course.id
            course_dir = os.path.dirname(path)
            os.makedirs(course_dir)
            if not os.path.exists(course_dir):
                os.makedirs(course_dir)
            os.chmod(path, 0o700)
            return course.toDict(), 201
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(Courses, "/api/courses")


class CourseViews(Resource):
    # GET current course
    @auth_check
    def get(self, id):
        c_course = Course.query.filter_by(id=id).first()
        if c_course is not None:
            return c_course.toDict(), 200
        else:
            return {
                "message": "Course not Found!"
            }, 404

    # UPDATE current course
    @auth_check
    def put(self, id):
        args = parser_post_put.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
                }, 404

        if is_course_owner(token, c_course):

            today = datetime.datetime.now()
            if c_course.status in ["closed", "rejected"]:
                c_course.name = args["name"]
                c_course.description = args["description"]
                c_course.price = args["price"]
                c_course.date = today.isoformat()
                db.session.commit()
                return c_course.toDict(), 200
            else:
                return {
                    "message": "Course is active or archived!"
                }, 409

        elif is_moderator(token) or is_admin(token):
            today = datetime.datetime.now()

            c_course.name = args["name"]
            c_course.description = args["description"]
            c_course.price = args["price"]
            c_course.date = today.isoformat()
            db.session.commit()
            return c_course.toDict(), 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # DELETE current course
    @auth_check
    def delete(self, id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]
        PRESENT_UPLOAD_FOLDER = app.config["PRESENT_UPLOAD_FOLDER"]
        b_data_path = app.config['B_DATA_FILES_DIR']

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course):
            if c_course.status == "open":
                return {
                    "message": "Course is open. Cannot be deleted without admin approval!"
                }, 409

            db.session.delete(c_course)
            db.session.commit()

            # DELETE exists data for boards for this course
            path = b_data_path + "course_%d/" % id
            course_dir = os.path.dirname(path)
            if os.path.exists(course_dir):
                shutil.rmtree(course_dir)

            # DELETE exist presentations for this course
            course_present_path = PRESENT_UPLOAD_FOLDER + "course_%d/" % id
            c_pres_dir = os.path.dirname(course_present_path)
            if os.path.exists(c_pres_dir):
                shutil.rmtree(c_pres_dir)

            # DELETE exist picture for this course
            filename = "picture_" + str(id)
            exists = os.path.isfile(UPLOAD_FOLDER + filename)
            if exists:
                old_file = UPLOAD_FOLDER + filename
                os.remove(old_file)
            return {
                "id": id
                }, 200

        elif is_admin(token):
            db.session.delete(c_course)
            db.session.commit()

            # DELETE exists data for boards for this course
            path = b_data_path + "course_%d/" % id
            course_dir = os.path.dirname(path)
            if os.path.exists(course_dir):
                shutil.rmtree(course_dir)

            # DELETE exist presentations for this course
            course_present_path = PRESENT_UPLOAD_FOLDER + "course_%d/" % id
            c_pres_dir = os.path.dirname(course_present_path)
            if os.path.exists(c_pres_dir):
                shutil.rmtree(c_pres_dir)

            # DELETE exist picture for this course
            filename = "picture_" + str(id)
            exists = os.path.isfile(UPLOAD_FOLDER + filename)
            if exists:
                old_file = UPLOAD_FOLDER + filename
                os.remove(old_file)
            return {
                "id": id
                }, 200

        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(CourseViews, "/api/courses/<int:id>")


class CourseActive(Resource):
    # PUT request to update course to active/unactive
    @auth_check
    def put(self, id):
        args = parser_active_put.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course) or is_admin(token):
            today = datetime.datetime.now()
            is_active = args["active"]
            c_course.is_active = is_active
            c_course.date = today.isoformat()
            db.session.commit()
            return c_course.toDict(), 200
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(CourseActive, "/api/courses/<int:id>/activate")


class CourseStatus(Resource):
    # PUT course to close ~ admin only
    @auth_check
    def put(self, id):
        args = parser_status_put.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404
        course_owner = User.query.filter_by(id=c_course.owner_id).first()

        if args["status"] not in ["closed", "waiting_approval", "rejected", "open"]:
            return {
                "message": "Bad argument value!"
            }, 400

        if is_admin(token):
            if c_course.status == "open":
                if args["status"] != "open":
                    if args["reason"] is None:
                        return {
                            "message": "Missing argument!"
                        }, 400

                    today = datetime.datetime.now()
                    c_course.status = args["status"]
                    c_course.date = today.isoformat()
                    db.session.commit()

                    mail_content = closing_course_reason_mail_body(course_owner.last_name,
                                                                   c_course.name,
                                                                   args["reason"])

                    mail_sender(course_owner.email, mail_content)

                    return c_course.toDict(), 200
                else:
                    return {
                        "message": "Course is already open!"
                    }, 409
            else:
                today = datetime.datetime.now()
                c_course.status = args["status"]
                c_course.date = today.isoformat()
                db.session.commit()
                return c_course.toDict(), 200
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(CourseStatus, "/api/courses/<int:id>/status")


class CourseImage(Resource):
    # UPLOAD image for current course
    @auth_check
    def post(self, id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        ALLOWED_EXTENSIONS = app.config["ALLOWED_EXTENSIONS"]
        UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course):
            if 'file' not in request.files:
                return {
                    "message": "No file part"
                }, 400

            file = request.files['file']
            if file.filename == "":
                return {
                    "message": "File not selected!"
                }, 400

            if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
                filename = "picture_" + str(id)

                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)

                exists = os.path.isfile(UPLOAD_FOLDER + filename)
                if exists:
                    return {
                        "message": "Picture already exist!"
                    }, 409

                file.save(os.path.join(UPLOAD_FOLDER, filename))
                return {
                    "message": "Created!"
                }, 201
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # UPLOAD image for current course
    @auth_check
    def put(self, id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        ALLOWED_EXTENSIONS = app.config["ALLOWED_EXTENSIONS"]
        UPLOAD_FOLDER = app.config["UPLOAD_FOLDER"]

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course) or is_moderator(token) or is_admin(token):
            if 'file' not in request.files:
                return {
                    "message": "No file part!"
                }, 400

            file = request.files['file']
            if file.filename == "":
                return {
                    "message": "File not selected!"
                }, 400

            if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
                filename = "picture_" + str(id)

                if not os.path.exists(UPLOAD_FOLDER):
                    return {
                        "message": "Directory don't exist!"
                    }, 404

                exists = os.path.isfile(UPLOAD_FOLDER + filename)
                if exists:
                    old_file = UPLOAD_FOLDER + filename
                    os.remove(old_file)

                    file.save(os.path.join(UPLOAD_FOLDER, filename))
                    return {
                        "message": "Updated!"
                    }, 201
                else:
                    return {
                        "message": "File to change not find!"
                    }, 404
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(CourseImage, "/api/courses/<int:id>/images")


class CoursePresentation(Resource):
    @auth_check
    def get(self, id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        PRESENT_UPLOAD_FOLDER = app.config['PRESENT_UPLOAD_FOLDER']

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course) or is_moderator(token) or is_admin(token):
            path = PRESENT_UPLOAD_FOLDER + "course_%d/" % (id)
            files = os.listdir(path)
            return files, 200

    # @auth_check
    def post(self, id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        PRESENT_ALLOWED_EXTENSIONS = app.config["PRESENT_ALLOWED_EXTENSIONS"]
        PRESENT_UPLOAD_FOLDER = app.config["PRESENT_UPLOAD_FOLDER"]
        PRESEND_HANDLER_HOST = app.config["PRESEND_HANDLER_HOST"]

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course) or is_moderator(token) or is_admin(token):
            if 'file' not in request.files:
                return {
                    "message": "No file part!"
                }, 400

            file = request.files['file']
            if file.filename == "":
                return {
                    "message": "File not selected!"
                }, 400

            path = PRESENT_UPLOAD_FOLDER + "course_%d/" % (id)
            course_dir = os.path.dirname(path)

            if not os.path.exists(course_dir):
                os.makedirs(course_dir)
            os.chmod(path, 0o755)

            if file and allowed_file(file.filename, PRESENT_ALLOWED_EXTENSIONS):
                file.save(os.path.join(course_dir, file.filename))
            else:
                return {
                    "message": "File is not presentation format!"
                }, 403

            payload = {"file_path": "course_%d/%s" % (id, file.filename)}
            try:
                r = requests.post(PRESEND_HANDLER_HOST, json=payload)
                return r.text, 200
            except requests.exceptions.RequestException as e:  # This is the correct syntax
                return {
                    "message": e
                }, 500

            if r.raise_for_status() is None:
                return "Ok", r.status_code
            else:
                return {
                    "message": "Something go wrong!"
                }, r.raise_for_status()
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(CoursePresentation, "/api/courses/<int:id>/presentations")


class CoursePresentationViews(Resource):
    @auth_check
    def delete(self, id, fileName):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        PRESENT_UPLOAD_FOLDER = app.config["PRESENT_UPLOAD_FOLDER"]

        c_course = Course.query.filter_by(id=id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course) or is_moderator(token) or is_admin(token):
            file_path = PRESENT_UPLOAD_FOLDER + "course_%d/%s" % (id, fileName) + ".svg"

            if os.path.isfile(file_path):
                os.remove(file_path)
                return {
                    "message": "ok"
                }, 200
            else:
                return {
                    "message": "File Not Found!"
                }, 404
        else:
            return {
                "message": "Permisson denied!"
            }, 403


api.add_resource(CoursePresentationViews, "/api/courses/<int:id>/presentations/<string:fileName>")

