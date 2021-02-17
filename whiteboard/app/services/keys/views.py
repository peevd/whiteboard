from . import api
from ... import db
from ...models.courses import Course
from ...models.groups import Group
from ...models.participants import Participant
from ...models.users import User
from ...models.keys import Key
from ..utils import parser, parse_token, auth_check, is_course_owner, \
                    create_invitation_mail_body, mail_sender, key_gen, url_gen

import datetime
from flask_restful import Resource


parser_post = parser.copy()
parser_post.add_argument("u_id", required=True,
                         type=int,
                         location="json",
                         help="Recipient addres cannot be blank!")


class Invitations(Resource):
    # POST request to can teacher send invite emails to students
    @auth_check
    def post(self, c_id, g_id):
        args = parser_post.parse_args()
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

        if is_course_owner(token, c_course):
            # Check is course group full (participants + unused_keys)
            all_participants = Participant.query.filter_by(group_id=g_id)
            unused_keys = Key.query.filter_by(course_id=c_id, group_id=g_id)
            if all_participants.count() + unused_keys.count() >= c_group.max_members:
                return {
                    "message": "This group is full already!"
                }, 409

            c_user = User.query.filter_by(id=args["u_id"]).first()
            if c_user is None:
                return {
                    "message": "User not Found!"
                }, 404

            for participant in all_participants:
                if participant.user_id == args["u_id"]:
                    return {
                        "message": "Student already exist in this course register!"
                    }, 409

            user_key = Key.query.filter_by(user_id=args["u_id"],
                                           course_id=c_id,
                                           group_id=g_id).first()
            if user_key is not None:
                return {
                    "message": "Key for this participant already exist!"
                }, 404

            date = datetime.datetime.now()
            n_key = key_gen(c_id, g_id, args["u_id"], date)

            new_key = Key(
                user_id=args["u_id"],
                course_id=c_id,
                group_id=g_id,
                key=n_key
            )
            db.session.add(new_key)
            db.session.commit()
            URL = url_gen(c_id, g_id, n_key)

            mail_content = create_invitation_mail_body(c_user.last_name, c_course.name, c_group.name, URL)
            try:
                mail_sender(c_user.email, mail_content)
            except Exception as e:
                raise e

            return {
                "message": "Key created and sended!"
            }, 200

        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(Invitations, "/api/courses/<int:c_id>/groups/<int:g_id>/invitations")


class InvitationsResend(Resource):
    # Resend invitation email without generate new key
    @auth_check
    def post(self, c_id, g_id):
        args = parser_post.parse_args()
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

        c_user = User.query.filter_by(id=args["u_id"]).first()
        if c_user is None:
            return {
                "message": "User not Found!"
            }, 404

        if is_course_owner(token, c_course):
            c_key = Key.query.filter_by(user_id=args["u_id"],
                                        course_id=c_id,
                                        group_id=g_id).first()
            if c_key is None:
                return {
                    "message": "Key for this participant is not Found!"
                }, 404

            URL = url_gen(c_id, g_id, c_key.key)

            mail_content = create_invitation_mail_body(c_user.last_name, c_course.name, c_group.name, URL)
            try:
                mail_sender(c_user.email, mail_content)
            except Exception as e:
                raise e

            return {
                "message": "URL successfully resend!"
            }, 201
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(InvitationsResend,
                 "/api/courses/<int:c_id>/groups/<int:g_id>/reinvitations")

