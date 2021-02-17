from . import api
from ... import db
from ...models.groups import Group
from ...models.courses import Course
from ...models.boards import Board
from ...models.participants import Participant
from ..utils import parser, parse_token, auth_check, is_course_owner, \
        self_participates, is_moderator, is_admin

from flask import current_app as app
from flask_restful import Resource
import os
import shutil

parser_post_put = parser.copy()
parser_post_put.add_argument("name", required=True,
                             location="json",
                             help="Name cannot be blank!")
parser_post_put.add_argument("max_members", type=int, required=True,
                             location="json",
                             help="Group size cannot be blank!")

parser_bord_put = parser.copy()
parser_bord_put.add_argument("is_active", type=bool,
                             required=False,
                             location="json")
parser_bord_put.add_argument("task_id", type=int,
                             required=False,
                             location="json")

parser_bord_data_put = parser.copy()
parser_bord_data_put.add_argument("board_data", type=str,
                                  required=True,
                                  location="json",
                                  help="Missing required parameter in JSON bodyY!")
parser_bord_snapshot_put = parser.copy()
parser_bord_snapshot_put.add_argument("board_snapshot", type=str,
                                      required=True,
                                      location="json",
                                      help="Missing required parameter in JSON bodyY!")


class Groups(Resource):
    # GET all groups for current course
    @auth_check
    def get(self, c_id):
        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        all_course_groups = [x.toDict() for x in Group.query.filter_by(course_id=c_id)]
        for group in all_course_groups:
            gr_count = Participant.query.filter_by(course_id=c_id,
                                                   group_id=group["id"]).count()
            group["members_in"] = gr_count

        return all_course_groups, 200

    # POST new group and board
    @auth_check
    def post(self, c_id):
        args = parser_post_put.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {"message":
                    "Course not Found!"}, 404

        if is_course_owner(token, c_course):
            if c_course.status in ["open", "waiting_approval"]:
                return {
                    "message": "Course is open or waiting approval!"
                }, 409

            new_group = Group(
                name=args["name"],
                max_members=args["max_members"],
                course_id=c_id,
            )
            db.session.add(new_group)
            db.session.commit()

            c_board = Board.query.filter_by(group_id=new_group.id).first()
            if c_board is not None:
                return {
                    "message": "Board already exist!"
                }, 409

            new_board = Board(
                group_id=new_group.id
            )
            db.session.add(new_board)
            db.session.commit()

            # Create files for current group with board data
            b_data_path = app.config['B_DATA_FILES_DIR']
            path = b_data_path + "course_%d/group_%d/" % (c_id, new_group.id)
            group_dir = os.path.dirname(path)
            if not os.path.exists(group_dir):
                os.makedirs(group_dir)
            os.chmod(path, 0o700)

            file = open(os.path.join(path, "b_data.txt"), "w+")
            file.close()
            f1_path = path + "b_data.txt"
            os.chmod(f1_path, 0o700)

            file = open(os.path.join(path, "b_snap.txt"), "w+")
            file.close()
            f2_path = path + "b_snap.txt"
            os.chmod(f2_path, 0o700)
            new_group = new_group.toDict()
            new_group["members_in"] = 0
            return new_group, 201
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(Groups, "/api/courses/<int:c_id>/groups")


class GroupViews(Resource):
    # GET current group
    @auth_check
    def get(self, c_id, g_id):
        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {"message":
                    "Course not Found!"}, 404

        c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
        if c_group is None:
            return {
                "message": "Group not Found!"
            }, 404

        c_group = c_group.toDict()
        gr_count = Participant.query.filter_by(course_id=c_id,
                                               group_id=g_id).count()
        c_group["members_in"] = gr_count

        return c_group, 200

    # PUT current group
    @auth_check
    def put(self, c_id, g_id):
        args = parser_post_put.parse_args()
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

            c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
            if c_group is not None:
                c_group.name = args["name"]
                c_group.max_members = args["max_members"]
                db.session.commit()
                return c_group.toDict(), 200
            else:
                return {
                    "message": "Group not Found!"
                }, 404

        elif is_moderator(token) or is_admin(token):
            c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
            if c_group is not None:
                c_group.name = args["name"]
                c_group.max_members = args["max_members"]
                db.session.commit()
                return c_group.toDict(), 200
            else:
                return {
                    "message": "Group not Found!"
                }, 404
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # DELETE current group
    @auth_check
    def delete(self, c_id, g_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {"message":
                    "Course not Found!"}, 404

        # TODO: ADD check for participants in this group befor delete, disallow
        # delete option if has
        if is_course_owner(token, c_course):
            if c_course.status in ["open", "waiting_approval"]:
                return {
                    "message": "Course is open or waiting approval!"
                }, 409

            c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
            if c_group is not None:
                db.session.delete(c_group)
                db.session.commit()

                b_data_path = app.config['B_DATA_FILES_DIR']
                path = b_data_path + "course_%d/group_%d/" % (c_id, g_id)
                group_dir = os.path.dirname(path)
                if os.path.exists(group_dir):
                    shutil.rmtree(group_dir)
                return {
                    "id": g_id
                }, 200
            else:
                return {
                    "message": "Group not Found!"
                }, 404

        elif is_admin(token):
            c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
            if c_group is not None:
                db.session.delete(c_group)
                db.session.commit()

                b_data_path = app.config['B_DATA_FILES_DIR']
                path = b_data_path + "course_%d/group_%d/" % (c_id, g_id)
                group_dir = os.path.dirname(path)
                if os.path.exists(group_dir):
                    shutil.rmtree(group_dir)
                return {
                    "id": g_id
                }, 200
            else:
                return {
                    "message": "Group not Found!"
                }, 404

        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(GroupViews, "/api/courses/<int:c_id>/groups/<int:g_id>")


class GroupIn(Resource):
    # get group in witch self participates
    @auth_check
    def get(self, c_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        mine_register = Participant.query.filter_by(user_id=token["sub"],
                                                    course_id=c_id).first()
        if mine_register is None:
            return {
                "message": "User not found in register!"
            }, 404

        mine_register = mine_register.toDict()
        group_in = Group.query.filter_by(id=mine_register["group_id"],
                                         course_id=c_id).first()

        group_in = group_in.toDict()
        gr_count = Participant.query.filter_by(course_id=c_id,
                                               group_id=group_in["id"]).count()
        group_in["members_in"] = gr_count
        return group_in, 200


api.add_resource(GroupIn, "/api/courses/<int:c_id>/groups/in")


class BoardViews(Resource):
    # GET board for current group
    @auth_check
    def get(self, c_id, g_id):
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

        c_board = Board.query.filter_by(group_id=g_id).first()
        if c_board is not None:
            return c_board.toDict(), 200
        else:
            return {
                "message": "Board is not Found!"
            }, 404

    # Set board to Active/Unactive
    @auth_check
    def put(self, c_id, g_id):
        args = parser_bord_put.parse_args()
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

        if is_course_owner(token, c_course):
            c_board = Board.query.filter_by(group_id=g_id).first()
            if c_board is not None:
                if args["is_active"] is not None:
                    c_board.is_active = args["is_active"]
                    db.session.commit()

                if args["task_id"] is not None:
                    c_board.task_id = args["task_id"]
                    db.session.commit()
                return c_board.toDict(), 200
            else:
                return {
                    "message": "Board not Found!"
                }, 404
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(BoardViews, "/api/courses/<int:c_id>/groups/<int:g_id>/board")


class BoardDataViews(Resource):
    # GET data for board
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

        if is_course_owner(token, c_course) or self_participates(token, c_id):
            c_board = Board.query.filter_by(group_id=g_id).first()
            if c_board is not None:
                b_data_path = app.config['B_DATA_FILES_DIR']
                path = b_data_path + "course_%d/group_%d/" % (c_id, g_id)

                file = open(os.path.join(path, "b_data.txt"), "r")
                b_data = file.read().replace("\n", "")
                file.close()
                return b_data, 200
            else:
                return {
                    "message": "Board is not Found!"
                }, 404
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # UPDATE current board data
    @auth_check
    def put(self, c_id, g_id):
        args = parser_bord_data_put.parse_args()
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

        if is_course_owner(token, c_course):
            c_board = Board.query.filter_by(group_id=g_id).first()
            if c_board is not None:
                b_data_path = app.config['B_DATA_FILES_DIR']
                path = b_data_path + "course_%d/group_%d/" % (c_id, g_id)

                file = open(os.path.join(path, "b_data.txt"), "w+")
                file.write(args["board_data"])
                file.close()
                return {
                    "message": "Updated!"
                }, 200
            else:
                return {
                    "message": "Board is not Found!"
                }, 404
        else:
            return{
                "message": "Permission denied!"
            }, 403


api.add_resource(BoardDataViews,
                 "/api/courses/<int:c_id>/groups/<int:g_id>/board/data")


class BoardSnapshotDataViews(Resource):
    # GET data for board
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

        if is_course_owner(token, c_course) or self_participates(token, c_id):
            c_board = Board.query.filter_by(group_id=g_id).first()
            if c_board is not None:
                c_board = c_board.toDict()

                b_data_path = app.config['B_DATA_FILES_DIR']
                path = b_data_path + "course_%d/group_%d/" % (c_id, g_id)

                file = open(os.path.join(path, "b_snap.txt"), "r")
                b_snap = file.read().replace("\n", "")
                file.close()
                return b_snap, 200
            else:
                return {
                    "message": "Board is not Found!"
                }, 404
        else:
            return {
                "message": "Permission denied!"
            }, 403

    # UPDATE current board snapshot data
    @auth_check
    def put(self, c_id, g_id):
        args = parser_bord_snapshot_put.parse_args()
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

        if is_course_owner(token, c_course):
            c_board = Board.query.filter_by(group_id=g_id).first()
            if c_board is not None:
                b_data_path = app.config['B_DATA_FILES_DIR']
                path = b_data_path + "course_%d/group_%d/" % (c_id, g_id)

                file = open(os.path.join(path, "b_snap.txt"), "w+")
                file.write(args["board_snapshot"])
                file.close()
                return {
                    "message": "Updated!"
                }, 200
            else:
                return {
                    "message": "Board is not Found!"
                }, 404
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(BoardSnapshotDataViews,
                 "/api/courses/<int:c_id>/groups/<int:g_id>/board/snapshot")

