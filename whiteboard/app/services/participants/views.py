from . import api
from ... import db
from ...models.participants import Participant
from ...models.courses import Course
from ...models.groups import Group
from ...models.users import User
from ...models.student_answers import StudentAnswer
from ...models.keys import Key
from ..utils import parser, parse_token, auth_check, is_course_owner, is_admin

from flask_restful import Resource

parser_post = parser.copy()
parser_post.add_argument("key", required=True,
                         location="json",
                         help="missing argument!")


class Participants(Resource):
    # GET all Participants for course group
    @auth_check
    def get(self, c_id, g_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
        if c_group is None:
            return {
                "message": "Group not Found!"
            }, 404

        if is_course_owner(token, c_course) or is_admin(token):
            all_participants = [x.toDict() for x in Participant.query.filter_by(course_id=c_id, group_id=g_id)]
            participants_info = []
            for participant in all_participants:
                user = User.query.filter_by(id=participant["user_id"]).first()
                user = user.toDict()
                user_dict = {}
                user_dict["id"] = participant["id"]
                user_dict["first_name"] = user["first_name"]
                user_dict["last_name"] = user["last_name"]
                user_dict["email"] = user["email"]
                user_dict["picture"] = user["picture"]
                participants_info.append(user_dict)

            return participants_info, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # Add participant to course and group
    @auth_check
    def post(self, c_id, g_id):
        args = parser_post.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
        if c_group is None:
            return {
                "message": "Group not Found!"
            }, 404

        c_participant = Participant.query.filter_by(user_id=token["sub"],
                                                    group_id=g_id).first()
        if c_participant is not None:
            return {
                "message": "Student already participating in this group!"
            }, 409

        user_key = Key.query.filter_by(user_id=token["sub"],
                                       course_id=c_id,
                                       group_id=g_id).first()
        if user_key is None:
            return {
                "message": "This student don't have invitation for this course!"
            }, 404

        if args["key"] == user_key.key:
            new_participant = Participant(
                user_id=token["sub"],
                course_id=c_id,
                group_id=g_id
                )
            db.session.add(new_participant)
            db.session.commit()

            db.session.delete(user_key)
            db.session.commit()
            return new_participant.toDict(), 201
        else:
            return {
                "message": "Wrong Key!"
            }, 409


api.add_resource(Participants,
                 "/api/courses/<int:c_id>/groups/<int:g_id>/participants")


class ParticipantsViews(Resource):
    # DELETE participant from course
    @auth_check
    def delete(self, c_id, g_id, p_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
        if c_group is None:
            return {
                "message": "Group not Found!"
            }, 404

        c_participant = Participant.query.filter_by(id=p_id,
                                                    group_id=g_id).first()
        if c_participant is not None:
            if is_course_owner(token, c_course) or is_admin(token):
                usr_course_ans = StudentAnswer.query.filter_by(student_id=c_participant.user_id,
                                                               group_id=g_id)
                for ans in usr_course_ans:
                    db.session.delete(ans)
                    db.session.commit()

                db.session.delete(c_participant)
                db.session.commit()

                return {
                    "Participant id": p_id,
                    "Group id": g_id
                }, 200

            else:
                return {
                    "message": "Permission denied!"
                }, 403
        else:
            return {
                "message": "Participant not Found!"
            }, 404


api.add_resource(ParticipantsViews,
                 "/api/courses/<int:c_id>/groups/<int:g_id>/participants/<int:p_id>")


class ParticipantsSelfDelete(Resource):
    # Delete self from Participants register
    @auth_check
    def delete(self, c_id, g_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_group = Group.query.filter_by(id=g_id).first()
        if c_group is None:
            return {
                "message": "Group not Found!"
            }, 404

        me_participant = Participant.query.filter_by(user_id=token["sub"],
                                                     course_id=c_id,
                                                     group_id=g_id).first()
        if me_participant is not None:
            mine_course_ans = StudentAnswer.query.filter_by(student_id=token["sub"],
                                                            group_id=g_id,
                                                            course_id=c_id)
            for ans in mine_course_ans:
                db.session.delete(ans)
                db.session.commit()

            db.session.delete(me_participant)
            db.session.commit()
            return {
                "User id": token["sub"],
                "Group id": g_id
            }, 200

        else:
            return {
                "message": "Participant not Found!"
            }, 404


api.add_resource(ParticipantsSelfDelete,
                 "/api/courses/<int:c_id>/groups/<int:g_id>/participants/me")

