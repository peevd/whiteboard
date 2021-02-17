from . import api
from ... import db
from ...models.courses import Course
from ...models.groups import Group
from ...models.tasks import Task
from ...models.users import User
from ...models.approval_requests import CourseApprovalRequest
from ..utils import parser, parse_token, auth_check, is_course_owner, \
        is_moderator, is_admin, is_request_owner, is_teacher, \
        create_admin_approval_request_mail_body, mail_sender

import datetime
from flask_restful import Resource
from sqlalchemy import extract

parser_get = parser.copy()
parser_get.add_argument("f", required=False,
                        location="args")
parser_get.add_argument("status", required=False,
                        type=int,
                        location="args")
parser_get.add_argument("date", required=False,
                        location="args")
parser_get.add_argument("ownerID", required=False,
                        type=int,
                        location="args")
parser_get.add_argument("courseID", required=False,
                        type=int,
                        location="args")
parser_get.add_argument("count", required=False,
                        location="args")

parser_post = parser.copy()
parser_post.add_argument("c_id", required=True,
                         location="json",
                         type=int,
                         help="Misssing argument!")

parser_put = parser.copy()
parser_put.add_argument("note", required=False,
                        location="json")
parser_put.add_argument("status", required=False,
                        type=int,
                        location="json")


class ApprovalRequests(Resource):
    # GET approval requests by date / status / ownerID
    @auth_check
    def get(self):
        args = parser_get.parse_args()
        token = parse_token(args["Authorization"])

        if is_admin(token) or is_moderator(token):
            if args["count"] is not None:
                if args["status"] is not None:
                    if args["status"] not in [1, 2, 3]:
                        return {
                            "message": "Bad argument value!"
                        }, 400
                    requests = CourseApprovalRequest.query.filter_by(status=args["status"])
                    return {
                        "count": requests.count()
                    }, 200
                else:
                    requests = CourseApprovalRequest.query
                    return {
                        "count": requests.count()
                    }, 200

            requests = []
            if args["status"] is None and args["date"] is None and \
                    args["ownerID"] is None and args["courseID"] is None:

                new_requests = CourseApprovalRequest.query.order_by("date").filter_by(status=1)
                new_requests = [x.toDict() for x in new_requests]
                for request in new_requests:
                    c_course = Course.query.filter_by(id=request["course_id"]).first()
                    request["course_name"] = c_course.name
                return new_requests, 200

            if args["courseID"] is not None:
                c_course_requests = CourseApprovalRequest.query.order_by("date").filter_by(course_id=args["courseID"]).first()
                if c_course_requests is None:
                    return {
                        "message": "Not Found!"
                    }, 404
                request = c_course_requests.toDict()
                c_course = Course.query.filter_by(id=request["course_id"]).first()
                request["course_name"] = c_course.name
                return request, 200

            if args["date"] is not None:
                try:
                    datetime.datetime.strptime(args["date"], "%Y-%m-%d")
                except ValueError:
                    return ("Bad date format! Try yy-mm-dd!"), 400

                date = args["date"].split("-")
                date_requests = db.session.query(CourseApprovalRequest).filter(
                            extract("year", CourseApprovalRequest.date) == date[0],
                            extract("month", CourseApprovalRequest.date) == date[1],
                            extract("day", CourseApprovalRequest.date) == date[2])

                if args["ownerID"] is not None:
                    for request in date_requests:
                        if request.owner_id == args["ownerID"]:
                            requests.append(request)
                    date_requests = requests
                    requests = []

                if args["status"] is not None:
                    if args["status"] not in [1, 2, 3]:
                        return {
                            "message": "Bad argument value!"
                        }, 400

                    for request in date_requests:
                        if request.status == args["status"]:
                            requests.append(request)

                    date_requests = requests

                date_requests_dicts = [x.toDict() for x in date_requests]
                for request in date_requests_dicts:
                    c_course = Course.query.filter_by(id=request["course_id"]).first()
                    request["course_name"] = c_course.name

                return date_requests_dicts, 200

            if args["date"] is None:
                if args["status"] is not None and args["ownerID"] is not None:
                    if args["status"] not in [1, 2, 3]:
                        return {
                            "message": "Bad argument value!"
                        }, 400

                    requests = CourseApprovalRequest.query.filter_by(status=args["status"],
                                                                     owner_id=args["ownerID"])
                    requests_dicts = [x.toDict() for x in requests]
                    for request in requests_dicts:
                        c_course = Course.query.filter_by(id=request["course_id"]).first()
                        request["course_name"] = c_course.name
                    return requests_dicts, 200

                if args["status"] is not None:
                    if args["status"] not in [1, 2, 3]:
                        return {
                            "message": "Bad argument value!"
                        }, 400

                    requests = CourseApprovalRequest.query.filter_by(status=args["status"])

                    requests_dicts = [x.toDict() for x in requests]
                    for request in requests_dicts:
                        c_course = Course.query.filter_by(id=request["course_id"]).first()
                        request["course_name"] = c_course.name

                    return requests_dicts, 200

                if args["ownerID"] is not None:
                    requests = CourseApprovalRequest.query.filter_by(owner_id=args["ownerID"])
                    requests_dicts = [x.toDict() for x in requests]
                    for request in requests_dicts:
                        c_course = Course.query.filter_by(id=request["course_id"]).first()
                        request["course_name"] = c_course.name
                    return requests_dicts, 200

        elif is_teacher(token):
            if args["courseID"] is not None:
                c_course_requests = CourseApprovalRequest.query.order_by("date").filter_by(course_id=args["courseID"],
                                                                                           owner_id=token["sub"]).first()
                if c_course_requests is None:
                    return {
                        "message": "Not Found!"
                    }, 404
                request = c_course_requests.toDict()

                c_course = Course.query.filter_by(id=request["course_id"]).first()
                request["course_name"] = c_course.name
                return request, 200

            own_requests = CourseApprovalRequest.query.filter_by(owner_id=token["sub"])
            requests_dicts = [x.toDict() for x in own_requests]
            for request in requests_dicts:
                c_course = Course.query.filter_by(id=request["course_id"]).first()
                request["course_name"] = c_course.name
            return requests_dicts, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # POST notification for course approval for Moderator / Admin
    @auth_check
    def post(self):
        args = parser_post.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=args["c_id"]).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course):
            if c_course.status == "open":
                return {
                    "message": "Course already approved!"
                }, 409

            c_request = CourseApprovalRequest.query.filter_by(course_id=args["c_id"]).first()
            if c_request:
                return {
                    "message": "Requset already exist!"
                }, 409

            course_groups = Group.query.filter_by(course_id=args["c_id"])
            if course_groups.count() == 0:
                return {
                    "message": "Need group/s for course!"
                }, 409

            course_tasks = Task.query.filter_by(course_id=args["c_id"])
            if course_tasks.count() == 0:
                return {
                    "message": "Need task/s for course!"
                }, 409

            today = datetime.datetime.now()
            newApprovalRquest = CourseApprovalRequest(
                course_id=c_course.id,
                owner_id=token["sub"],
                status=1,
                date=today.isoformat()
            )

            db.session.add(newApprovalRquest)
            db.session.commit()

            c_course.status = "waiting_approval"
            db.session.commit()

            # TODO: Add email sender for user who write request
            newApprovalRquestDict = newApprovalRquest.toDict()
            newApprovalRquestDict["course_name"] = c_course.name

            return newApprovalRquestDict, 201
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(ApprovalRequests, "/api/requests")


class ApprovalRequest(Resource):
    # GET approval request by ID
    @auth_check
    def get(self, r_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])
        c_request = CourseApprovalRequest.query.filter_by(id=r_id).first()
        if c_request is None:
            return {
                "message": "Not found"
            }, 404

        if is_admin(token) or is_moderator(token) \
                or is_request_owner(token, c_request):

            c_request_dict = c_request.toDict()
            c_course = Course.query.filter_by(id=c_request_dict["course_id"]).first()
            c_request_dict["course_name"] = c_course.name

            return c_request_dict, 200

        else:
            return {
                "message": "Permission denied!"
            }, 403

    # Put approve request by ID
    @auth_check
    def put(self, r_id):
        args = parser_put.parse_args()
        token = parse_token(args["Authorization"])

        c_request = CourseApprovalRequest.query.filter_by(id=r_id).first()
        if c_request is None:
            return {
                "message": "Not Found!"
            }, 404

        c_course = Course.query.filter_by(id=c_request.course_id).first()

        today = datetime.datetime.now()
        if is_request_owner(token, c_request):
            if c_request.status == 1:
                return {
                    "message": "Course waiting for approvel!"
                }, 409

            if c_request.status == 3:
                return {
                    "message": "Course already approved!"
                }, 409

            c_request.status = 1
            c_request.date = today.isoformat()
            db.session.commit()

            c_course.status = "waiting_approval"
            db.session.commit()

            c_request_dict = c_request.toDict()
            c_request_dict["course_name"] = c_course.name

            return c_request_dict, 200

        elif is_admin(token) or is_moderator(token):
            if args["status"] is None or args["status"] not in [2, 3]:
                return {
                    "message": "Bad request argument!"
                }, 400

            if args["note"] is None:
                return {
                    "message": "Missing argument!"
                }, 400

            owner = User.query.filter_by(id=c_request.owner_id).first()

            c_request.moderator_id = token["sub"]
            c_request.status = args["status"]
            c_request.note = args["note"]
            c_request.date = today.isoformat()
            db.session.commit()

            if args["status"] == 2:
                c_course.status = "rejected"
                db.session.commit()

            if args["status"] == 3:
                c_course.status = "open"
                db.session.commit()

            mail_content = create_admin_approval_request_mail_body(owner.last_name,
                                                                   c_course.name,
                                                                   c_course.id,
                                                                   args["status"],
                                                                   args["note"])
            mail_sender(owner.email, mail_content)

            c_request_dict = c_request.toDict()
            c_request_dict["course_name"] = c_course.name

            return c_request_dict, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # DELETE approval request by ID ~ only admin / moderator
    @auth_check
    def delete(self, r_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        if is_admin(token) or is_moderator(token):
            c_request = CourseApprovalRequest.query.filter_by(id=r_id).first()
            if c_request is None:
                return {
                    "message": "Not found"
                }, 404

            db.session.delete(c_request)
            db.session.commit()
            return {
                "r_id": r_id
            }, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(ApprovalRequest, "/api/requests/<int:r_id>")

