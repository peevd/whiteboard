from . import api
from ... import db
from ...models.tasks import Task
from ...models.courses import Course
from ..utils import parser, parse_token, auth_check, is_course_owner, \
        self_participates, is_moderator, is_admin

from flask_restful import Resource
from flask import request
from sqlalchemy import func
import json

parser_post = parser.copy()
parser_post.add_argument("name", required=True,
                         location="json",
                         help="Name cannot be blank!")
parser_post.add_argument("description", required=True,
                         location="json",
                         help="Description cannot be blank!")
parser_post.add_argument("format", type=int,
                         location="json",
                         required=True,
                         help="Missing argument!")
parser_post.add_argument("test", type=list,
                         location="json",
                         required=False)

parser_put = parser.copy()
parser_put.add_argument("name", required=True,
                        location="json",
                        help="Name cannot be blank!")
parser_put.add_argument("description", required=True,
                        location="json",
                        help="Description cannot be blank!")
parser_put.add_argument("test", type=list,
                        location="json",
                        required=False)


class Tasks(Resource):
    # GET all registerd tasks for current course
    @auth_check
    def get(self, c_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        course_tasks = Task.query.filter_by(course_id=c_id)
        tasks_dict = [x.toDict() for x in course_tasks]

        if is_course_owner(token, c_course) or is_moderator(token) or is_admin(token):
            for task in tasks_dict:
                if task["format"] == 1:
                    task["test"] = json.loads(task["test"])

            return tasks_dict, 200

        if self_participates(token, c_id):
            for task in tasks_dict:
                if task["format"] == 1:
                    task["test"] = json.loads(task["test"])
                    del task["test"]["correctAnswers"]

            return tasks_dict, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # ADD task to current course
    @auth_check
    def post(self, c_id):
        args = parser_post.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        last_task = db.session.query(func.max(Task.task_number)).first()
        if last_task[0] is None:
            next_task = 1
        else:
            next_task = last_task[0] + 1

        if is_course_owner(token, c_course):
            if c_course.status in ["open", "waiting_approval"]:
                return {
                    "message": "Course is open or waiting approval!"
                }, 409

            # Create OE Task
            if args["format"] == 2:

                new_task = Task(
                    name=args["name"],
                    description=args["description"],
                    course_id=c_id,
                    task_number=next_task,
                    format=args["format"]
                )
                db.session.add(new_task)
                db.session.commit()
                return new_task.toDict(), 201

            if args["format"] == 1:
                if args["test"] is None or "questions" not in args["test"] or "correctAnswers" not in args["test"]:
                    return {
                        "message": "Missing argument!"
                    }, 400

                if "computing_system" not in args["test"]:
                    return {
                        "message": "Missing argument!"
                    }, 400

                data = request.get_json()
                correct_answers = data["test"]["correctAnswers"]
                points = 0

                for answers in correct_answers:
                    points += len(correct_answers[answers])

                str_test_data = json.dumps(data["test"])

                new_task = Task(
                    name=args["name"],
                    description=args["description"],
                    course_id=c_id,
                    task_number=next_task,
                    format=args["format"],
                    test=str_test_data,
                    max_points=points
                )
                db.session.add(new_task)
                db.session.commit()

                new_task = new_task.toDict()
                new_task["test"] = data["test"]
                return new_task, 201
            else:
                return {
                    "message": "Wrong format!"
                }, 400
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(Tasks, "/api/courses/<int:c_id>/tasks")


class TaskViews(Resource):
    # GET current task
    @auth_check
    def get(self, c_id, t_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_task = Task.query.filter_by(id=t_id, course_id=c_id).first()
        if c_task is None:
            return {
                "message": "Task not Found!"
            }, 404
        c_task = c_task.toDict()

        if is_course_owner(token, c_course) or is_moderator(token) or is_admin(token):
            if c_task["format"] == 1:
                c_task["test"] = json.loads(c_task["test"])

            return c_task, 200

        if self_participates(token, c_id):
            if c_task["format"] == 1:
                test = json.loads(c_task["test"])
                # Remove correct answers ID's from dict and add count of them
                for each in test["correctAnswers"]:
                    test["correctAnswers"][each] = len(test["correctAnswers"][each])
                c_task["test"] = test
            return c_task, 200

        else:
            return {
                "message": "Permission denied!"
            }, 403

    # UPDATE course task
    def put(self, c_id, t_id):
        args = parser_put.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404
        if is_course_owner(token, c_course):
            if c_course.status in ["open", "waiting_approval"]:
                return {
                    "message": "Course is open or waiting approval!"
                }, 409

        if is_course_owner(token, c_course) or is_moderator(token) or is_admin(token):
            c_task = Task.query.filter_by(id=t_id, course_id=c_id).first()
            if c_task is not None:
                # OE task case
                if c_task.format == 2:
                    c_task.name = args["name"]
                    c_task.description = args["description"]
                    db.session.commit()
                    return c_task.toDict(), 200

                # Test task case
                if c_task.format == 1:
                    if args["test"] is None or "questions" not in args["test"] or "correctAnswers" not in args["test"]:
                        return {
                            "message": "Missing argument!"
                        }, 400
                    data = request.get_json()

                    correct_answers = data["test"]["correctAnswers"]
                    points = 0

                    for answers in correct_answers:
                        points += len(correct_answers[answers])

                    str_test_data = json.dumps(data["test"])

                    c_task.name = args["name"],
                    c_task.description = args["description"],
                    c_task.test = str_test_data,
                    c_task.max_points = points
                    db.session.commit()

                    c_task = c_task.toDict()
                    c_task["test"] = data["test"]
                    return c_task, 200
            else:
                return {
                    "message": "Task not Found!"
                }, 404
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # DELETE current task for current course
    @auth_check
    def delete(self, c_id, t_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if is_course_owner(token, c_course):
            if c_course.status in ["open", "waiting_approval"]:
                return {
                    "message": "Course is open or waiting approval!"
                }, 409

            c_task = Task.query.filter_by(id=t_id, course_id=c_id).first()

            if c_task is None:
                return {
                    "message": "Task not Found!"
                }, 404

            db.session.delete(c_task)
            db.session.commit()
            return {
                "id": t_id
            }, 200

        elif is_admin(token):
            c_task = Task.query.filter_by(id=t_id, course_id=c_id).first()

            if c_task is None:
                return {
                    "message": "Task not Found!"
                }, 404

            db.session.delete(c_task)
            db.session.commit()
            return {
                "id": t_id
            }, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(TaskViews, "/api/courses/<int:c_id>/tasks/<int:t_id>")

