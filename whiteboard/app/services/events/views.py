from . import api
from ... import db
from ...models.courses import Course
from ...models.groups import Group
from ...models.participants import Participant
from ...models.events import Event
from ...models.tasks import Task
from ..utils import parser, parse_token, auth_check, is_course_owner, \
        is_moderator, is_admin, is_event_owner, is_teacher, \
        self_part_course_group, get_tasks_info

import datetime
from datetime import timedelta
from flask_restful import Resource
from flask import request

parser_get = parser.copy()
parser_get.add_argument("f", required=True,
                        location="args",
                        help="Missing argument!")
parser_get.add_argument("c_id", required=False,
                        type=int,
                        location="args")
parser_get.add_argument("g_id", required=False,
                        type=int,
                        location="args")

parser_post = parser.copy()
parser_post.add_argument("c_id", required=True,
                         location="json",
                         type=int,
                         help="Missing argument!")
parser_post.add_argument("g_id", required=True,
                         location="json",
                         type=int,
                         help="Missing argument!")
parser_post.add_argument("subject", required=True,
                         location="json",
                         help="Missing argument!")
parser_post.add_argument("body", required=True,
                         location="json",
                         help="Missing argument!")
parser_post.add_argument("date", required=True,
                         location="json",
                         help="Missing argument!")
parser_post.add_argument("task_ids", required=True,
                         location="json",
                         help="Missing argument!")

parser_put = parser.copy()
parser_put.add_argument("subject", required=True,
                        location="json",
                        help="Missing argument!")
parser_put.add_argument("body", required=True,
                        location="json",
                        help="Missing argument!")
parser_put.add_argument("date", required=True,
                        location="json",
                        help="Missing argument!")
parser_put.add_argument("task_ids", required=True,
                        location="json",
                        help="Missing argument!")


class Evenets(Resource):
    # GET all course group events
    @auth_check
    def get(self):
        args = parser_get.parse_args()
        token = parse_token(args["Authorization"])

        yesterday = datetime.date.today() - timedelta(1)

        if args["f"] == "all":
            if is_admin(token) or is_moderator(token):
                events = Event.query.filter(Event.date >= yesterday).order_by("date")
                events = [x.toDict() for x in events]
                for event in events:
                    event["tasks_data"] = get_tasks_info(event["task_ids"])
                return events, 200

            if is_teacher(token):
                events = Event.query.filter(Event.date >= yesterday).filter_by(owner_id=token["sub"]).order_by("date")
                events = [x.toDict() for x in events]
                for event in events:
                    c_course = Course.query.filter_by(id=event["course_id"]).first()
                    c_group = Group.query.filter_by(id=event["group_id"]).first()
                    event["course_name"] = c_course.name
                    event["group_name"] = c_group.name
                    event["tasks_data"] = get_tasks_info(event["task_ids"])
                return events, 200

            else:
                events_for_user = []
                mine_info = Participant.query.filter_by(user_id=token["sub"])

                for info in mine_info:
                    events = Event.query.filter(Event.date >= yesterday).filter_by(course_id=info.course_id,
                                                                                   group_id=info.group_id)
                    for event in events:
                        event = event.toDict()
                        c_course = Course.query.filter_by(id=event["course_id"]).first()
                        c_group = Group.query.filter_by(id=event["group_id"]).first()
                        event["course_name"] = c_course.name
                        event["group_name"] = c_group.name
                        event["tasks_data"] = get_tasks_info(event["task_ids"])
                        events_for_user.append(event)

                events_for_user.sort(key=lambda r: r["date"])
                return events_for_user, 200

        if args["f"] == "byCourse":
            if args["c_id"] is None:
                return {
                    "message": "Bad request argument!"
                }, 400

            c_course = Course.query.filter_by(id=args["c_id"]).first()
            if c_course is None:
                return {
                    "message": "Course not Foudn!"
                }, 404

            if is_course_owner(token, c_course) \
                    or is_moderator(token) or is_admin(token):

                events = Event.query.filter(Event.date >= yesterday).filter_by(course_id=args["c_id"]).order_by("date")
                events = [x.toDict() for x in events]
                for event in events:
                    c_course = Course.query.filter_by(id=event["course_id"]).first()
                    c_group = Group.query.filter_by(id=event["group_id"]).first()
                    event["course_name"] = c_course.name
                    event["group_name"] = c_group.name
                    event["tasks_data"] = get_tasks_info(event["task_ids"])
                return events, 200

            mine_register = Participant.query.filter_by(user_id=token["sub"],
                                                        course_id=args["c_id"]).first()

            if mine_register is not None:
                events = Event.query.filter(Event.date >= yesterday).filter_by(course_id=args["c_id"],
                                                                               group_id=mine_register.group_id).order_by("date")
                events = [x.toDict() for x in events]
                for event in events:
                    c_course = Course.query.filter_by(id=event["course_id"]).first()
                    c_group = Group.query.filter_by(id=event["group_id"]).first()
                    event["course_name"] = c_course.name
                    event["group_name"] = c_group.name
                    event["tasks_data"] = get_tasks_info(event["task_ids"])
                return events, 200

            else:
                return {
                    "message": "Permission denied!"
                }, 403

        if args["f"] == "byCourseGroup":
            if args["c_id"] is None or args["g_id"] is None:
                return {
                    "message": "Bad request argument!"
                }, 400

            c_course = Course.query.filter_by(id=args["c_id"]).first()
            if c_course is None:
                return {
                    "message": "Course not Foudn!"
                }, 404

            c_group = Group.query.filter_by(id=args["g_id"]).first()
            if c_group is None:
                return {
                    "message": "Group not Found!"
                }, 404

            if is_course_owner(token, c_course) \
                    or is_moderator(token) or is_admin(token):

                events = Event.query.filter(Event.date >= yesterday).filter_by(course_id=args["c_id"],
                                                                               group_id=args["g_id"]).order_by("date")
                events = [x.toDict() for x in events]
                for event in events:
                    c_course = Course.query.filter_by(id=event["course_id"]).first()
                    c_group = Group.query.filter_by(id=event["group_id"]).first()
                    event["course_name"] = c_course.name
                    event["group_name"] = c_group.name
                    event["tasks_data"] = get_tasks_info(event["task_ids"])
                return events, 200

            mine_register = Participant.query.filter_by(user_id=token["sub"],
                                                        course_id=args["c_id"],
                                                        group_id=args["g_id"]).first()

            if mine_register is not None:
                events = Event.query.filter(Event.date >= yesterday).filter_by(course_id=args["c_id"],
                                                                               group_id=args["g_id"]).order_by("date")
                events = [x.toDict() for x in events]
                for event in events:
                    c_course = Course.query.filter_by(id=event["course_id"]).first()
                    c_group = Group.query.filter_by(id=event["group_id"]).first()
                    event["course_name"] = c_course.name
                    event["group_name"] = c_group.name
                    event["tasks_data"] = get_tasks_info(event["task_ids"])
                return events, 200
            else:
                return {
                    "message": "Permission denied!"
                }, 403
        else:
            return {
                "message": "Bad request argument!"
            }, 400

    # POST event to a group
    @auth_check
    def post(self):
        args = parser_post.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=args["c_id"]).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_group = Group.query.filter_by(id=args["g_id"], course_id=args["c_id"]). first()
        if c_group is None:
            return {
                "message": "Group not Found!"
            }, 404

        if is_course_owner(token, c_course):
            data = request.get_json()
            task_ids = data["task_ids"]
            tasks_data = []
            task_ids_str = ""
            for task_id in task_ids:
                c_task = Task.query.filter_by(id=task_id,
                                              course_id=args["c_id"]).first()
                if c_task is None:
                    return {
                        "message": "Task not Found!"
                    }, 404

                test_dict_data = {}
                test_dict_data["id"] = c_task.id
                test_dict_data["name"] = c_task.name
                test_dict_data["description"] = c_task.description
                tasks_data.append(test_dict_data)

                task_ids_str += str(task_id)
                task_ids_str += ","

            task_ids_str = task_ids_str[:-1]

            date_datetime_object = datetime.datetime.strptime(args["date"], "%Y-%m-%d %H:%M")
            event = Event(
                owner_id=token["sub"],
                course_id=c_course.id,
                group_id=c_group.id,
                date=date_datetime_object.isoformat(),
                subject=args["subject"],
                body=args["body"],
                task_ids=task_ids_str
            )

            db.session.add(event)
            db.session.commit()

            event = event.toDict()
            event["course_name"] = c_course.name
            event["group_name"] = c_group.name
            event["tasks_data"] = tasks_data

            return event, 201
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(Evenets, "/api/events")


class EventViews(Resource):
    # GET current event by id
    @auth_check
    def get(self, e_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_event = Event.query.filter_by(id=e_id).first()
        if c_event is None:
            return {
                "message": "Event not Found!"
            }, 404

        if is_event_owner(token, c_event) \
                or is_moderator(token) \
                or is_admin(token) \
                or self_part_course_group(token, c_event.course_id, c_event.group_id):
            c_event = c_event.toDict()
            c_course = Course.query.filter_by(id=c_event["course_id"]).first()
            c_group = Group.query.filter_by(id=c_event["group_id"]).first()
            c_event["course_name"] = c_course.name
            c_event["group_name"] = c_group.name
            c_event["tasks_data"] = get_tasks_info(c_event["task_ids"])

            return c_event, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # PUT current event bey id
    @auth_check
    def put(self, e_id):
        args = parser_put.parse_args()
        token = parse_token(args["Authorization"])

        c_event = Event.query.filter_by(id=e_id).first()

        c_course = Course.query.filter_by(id=c_event.course_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_group = Group.query.filter_by(id=c_event.group_id, course_id=c_event.course_id). first()
        if c_group is None:
            return {
                "message": "Group not Found!"
            }, 404

        if is_event_owner(token, c_event) \
                or is_moderator(token) \
                or is_admin(token):

            if c_event is None:
                return {
                    "message": "Event not Found!"
                }, 404

            data = request.get_json()
            task_ids = data["task_ids"]
            tasks_data = []
            task_ids_str = ""
            for task_id in task_ids:
                c_task = Task.query.filter_by(id=task_id,
                                              course_id=c_course.id).first()
                if c_task is None:
                    return {
                        "message": "Task not Found!"
                    }, 404

                test_dict_data = {}
                test_dict_data["id"] = c_task.id
                test_dict_data["name"] = c_task.name
                test_dict_data["description"] = c_task.description
                tasks_data.append(test_dict_data)

                task_ids_str += str(task_id)
                task_ids_str += ","

            task_ids_str = task_ids_str[:-1]

            date_datetime_object = datetime.datetime.strptime(args["date"], "%Y-%m-%d %H:%M")
            c_event.subject = args["subject"]
            c_event.body = args["body"]
            c_event.date = date_datetime_object.isoformat()
            c_event.task_ids = task_ids_str

            db.session.commit()

            c_event = c_event.toDict()
            c_event["course_name"] = c_course.name
            c_event["group_name"] = c_group.name
            c_event["tasks_data"] = tasks_data

            return c_event, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # DELETE event by id
    @auth_check
    def delete(self, e_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_event = Event.query.filter_by(id=e_id).first()
        if c_event is None:
            return {
                "message": "Event not Found!"
            }, 404

        if is_event_owner(token, c_event) or is_admin(token):
            db.session.delete(c_event)
            db.session.commit()
            return {
                "id": e_id
            }, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(EventViews, "/api/events/<int:e_id>")

