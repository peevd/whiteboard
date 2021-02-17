from . import api
from ... import db
from ...models.courses import Course
from ...models.groups import Group
from ...models.participants import Participant
from ...models.results import Result
from ..utils import parser, parse_token, auth_check, is_course_owner, \
            self_participates, user_participates, group_exist, is_admin

import datetime
from flask_restful import Resource


parser_get = parser.copy()
parser_get.add_argument("g", required=False,
                        type=int,
                        location="args")
parser_get.add_argument("u", required=False,
                        type=int,
                        location="args")

parser_post = parser.copy()
parser_post.add_argument("u", required=True,
                         type=int,
                         location="args")
parser_post.add_argument("grade", required=True,
                         location="json",
                         help="Missing argument!")

parser_put = parser.copy()
parser_put.add_argument("grade", required=True,
                        location="json",
                        help="Missing argument!")


class ResultBase(Resource):
    # GET course results  /for hole group ?g=<int>/ for single student ?u=<int>/ and for all groups without ags
    @auth_check
    def get(self, c_id):
        args = parser_get.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course) or is_admin(token):
            # Results for current group
            if args["g"] is not None:
                if not group_exist(args["g"], c_id):
                    return {
                        "message": "Group not Found!"
                    }, 404

                student_results = Result.query.filter_by(course_id=c_id,
                                                         group_id=args["g"])
                all_results = []
                for result in student_results:
                    all_results.append(result.toDict())

                grpoup_results = {}
                grpoup_results["group_id"] = args["g"]
                grpoup_results["results"] = all_results
                return grpoup_results, 200

            # Results for current student
            if args["u"] is not None:
                if not user_participates(args["u"], c_id):
                    return {
                        "message": "Student not Found in course register!"
                    }, 404

                student_result = Result.query.filter_by(course_id=c_id,
                                                        student_id=args["u"]).first()
                if student_result is None:
                    return {
                        "message": "Result not Found!"
                    }, 404

                return student_result.toDict(), 200

            # Results for all course groups
            if args["g"] is None and args["u"] is None:
                all_groups = Group.query.filter_by(course_id=c_id)
                groups_results = []
                for group in all_groups:
                    c_group = {}

                    student_results = student_result = Result.query.filter_by(course_id=c_id,
                                                                              group_id=group.id)
                    results = []
                    for result in student_results:
                        results.append(result.toDict())

                    c_group["group_id"] = group.id
                    c_group["results"] = results
                    groups_results.append(c_group)
                return groups_results, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    @auth_check
    def post(self, c_id):
        args = parser_post.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course):
            if args["u"] is not None:
                register_check = Participant.query.filter_by(course_id=c_id,
                                                             user_id=args["u"]).first()
                if register_check is None:
                    return {
                        "message": "Student not Found in course register!"
                    }, 404

                result_check = Result.query.filter_by(course_id=c_id,
                                                      group_id=register_check.group_id,
                                                      student_id=args["u"]).first()
                if result_check is not None:
                    return {
                        "message": "Grade for this student already exist!"
                    }, 409

                today = datetime.datetime.now()
                new_result = Result(
                    course_id=c_id,
                    group_id=register_check.group_id,
                    student_id=args["u"],
                    grade=args["grade"],
                    date=today.isoformat()
                    )
                db.session.add(new_result)
                db.session.commit()
                return new_result.toDict(), 201
            else:
                return {
                    "message": "Missing argument!"
                }, 404
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(ResultBase, "/api/courses/<int:c_id>/results")


class ResultsViews(Resource):
    # Change result for current student
    @auth_check
    def put(self, c_id, r_id):
        args = parser_put.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_result = Result.query.filter_by(id=r_id, course_id=c_id).first()
        if c_result is None:
            return {
                "message": "Resoult not Found!"
            }, 404

        today = datetime.datetime.now()
        if is_course_owner(token, c_course):
            c_result.grade = args["grade"]
            c_result.date = today.isoformat()
            db.session.commit()
            return c_result.toDict(), 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    @auth_check
    def delete(self, c_id, r_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_result = Result.query.filter_by(id=r_id, course_id=c_id).first()
        if c_result is None:
            return {
                "message": "Resoult not Found!"
            }, 404

        if is_course_owner(token, c_course):
            db.session.delete(c_result)
            db.session.commit()
            return {
                "id": r_id
            }, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(ResultsViews, "/api/courses/<int:c_id>/results/<int:r_id>")


class ResultMe(Resource):
    # Get self result for current cource
    @auth_check
    def get(self, c_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if not self_participates(token, c_id):
            return {
                "message": "User not found in course register!"
            }, 404

        my_result = Result.query.filter_by(course_id=c_id,
                                           student_id=token["sub"]).first()
        if my_result is not None:
            return my_result.toDict(), 200
        else:
            return {
                "message": "Result not Found!"
            }, 404


api.add_resource(ResultMe, "/api/courses/<int:c_id>/results/me")

