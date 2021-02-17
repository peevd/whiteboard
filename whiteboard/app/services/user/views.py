from . import api
from ... import db
from ...models.users import User
from ...models.roles import Role
from ..utils import parser, parse_token, auth_check, is_teacher, is_admin, \
                    is_moderator

from flask_restful import Resource

parser_get = parser.copy()
parser_get.add_argument("r", required=False,
                        location="args")
parser_get.add_argument("fname", required=False,
                        location="args")
parser_get.add_argument("lname", required=False,
                        location="args")
parser_get.add_argument("fullname", required=False,
                        location="args")
parser_get.add_argument("count", required=False,
                        location="args")
parser_get.add_argument("role_id", required=False,
                        type=int,
                        location="args")

parser_put = parser.copy()
parser_put.add_argument("role_id", type=int, required=True,
                        location="json", help="Role id cannot be blank!")


class Users(Resource):
    # GET self information
    @auth_check
    def get(self):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        me = User.query.filter_by(id=token["sub"]).first()
        if me is None:
            return {
                "message": "User not found!"
            }, 404
        else:
            me_dict = {}
            me_dict["id"] = me.id
            me_dict["first_name"] = me.first_name
            me_dict["last_name"] = me.last_name
            me_dict["email"] = me.email
            me_dict["picture"] = me.picture
            me_dict["role_id"] = me.role_id
            return me_dict, 200

    # Set/Change self role
    @auth_check
    def put(slef):
        args = parser_put.parse_args()
        token = parse_token(args["Authorization"])

        if args["role_id"] in [1, 2]:
            return {
                "message": "Permission denied!"
            }, 403

        me = User.query.filter_by(id=token["sub"]).first()
        if me is None:
            return {
                "message": "User not found!"
            }, 404

        role = Role.query.filter_by(id=args["role_id"]).first()
        if role is None:
            return {
                "message": "Role not Found!"
            }, 404
        else:
            me.role_id = args["role_id"]
            db.session.commit()

            me_dict = {}
            me_dict["first_name"] = me.first_name
            me_dict["last_name"] = me.last_name
            me_dict["email"] = me.email
            me_dict["role_id"] = me.role_id
            return me_dict, 200


api.add_resource(Users, "/api/users/me")


class UsersInfo(Resource):
    # GET user basic info
    @auth_check
    def get(self, u_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        if is_admin(token):
            user = User.query.filter_by(id=u_id).first()
            if user is None:
                return {
                    "message": "User not found!"
                }, 404
            else:
                user_public = user.toDict()
                return user_public, 200
        else:
            user = User.query.filter_by(id=u_id).first()
            if user is None:
                return {
                    "message": "User not found!"
                }, 404

            if user.role_id in [1, 2]:
                return {
                    "message": "Access for this user denied!"
                }, 403

            user_public = user.toDictPublic()
            return user_public, 200


api.add_resource(UsersInfo, "/api/users/<int:u_id>")


class AllUsersFilter(Resource):
    # GET all available users
    @auth_check
    def get(self):
        args = parser_get.parse_args()
        token = parse_token(args["Authorization"])

        if is_teacher(token):
            if args["r"] is not None:
                if args["r"] not in ["student", "teacher"]:
                    return {
                        "message": "Unknown argument!"
                    }, 400

                if args["r"] == "student":
                    users_toDict = []
                    users = User.query.filter_by(role_id=4)

                    for user in users:
                        user_public = user.toDictPublic()
                        users_toDict.append(user_public)
                    return users_toDict, 200

                if args["r"] == "teacher":
                    users_toDict = []
                    users = User.query.filter_by(role_id=3)

                    for user in users:
                        user_public = user.toDictPublic()
                        users_toDict.append(user_public)
                    return users_toDict, 200

            if args["r"] is None:
                users_toDict = []
                users = User.query

                for user in users:
                    user_public = user.toDictPublic()
                    if user_public["role_id"] in [1, 2]:
                        continue
                    users_toDict.append(user_public)
                return users_toDict, 200

        if is_admin(token) or is_moderator(token):
            if args["count"] is not None:
                if args["role_id"] is not None:
                    if args["role_id"] not in [4, 3]:
                        return {
                            "message": "Unknown argument value!"
                        }, 400

                    users = User.query.filter_by(role_id=args["role_id"])
                    return {
                        "count": users.count()
                    }, 200
                else:
                    users = User.query
                    return {
                        "count": users.count()
                    }, 200
            if args["r"] is not None:
                if args["r"] not in ["student", "teacher"]:
                    return {
                        "message": "Unknown argument!"
                    }, 400

                if args["r"] == "student":
                    users_toDict = []
                    users = User.query.filter_by(role_id=4)

                    for user in users:
                        user_public = user.toDict()
                        users_toDict.append(user_public)
                    return users_toDict, 200

                if args["r"] == "teacher":
                    users_toDict = []
                    users = User.query.filter_by(role_id=3)

                    for user in users:
                        user_public = user.toDict()
                        users_toDict.append(user_public)
                    return users_toDict, 200

            if args["r"] is None:
                users_toDict = []
                users = User.query

                for user in users:
                    user_public = user.toDict()
                    users_toDict.append(user_public)
                return users_toDict, 200
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(AllUsersFilter, "/api/users")

