# from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib import sqla
from flask import current_app as app
from flask import redirect
from werkzeug.exceptions import HTTPException, Response
from flask_basicauth import BasicAuth


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            "You could not be authenticated. Please refresh the page.", 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class ModelView(sqla.ModelView):
    def is_accessible(self):
        basic_auth = BasicAuth(app)
        if not basic_auth.authenticate():
            raise AuthException('Not authenticated.')
        else:
            return True

    def inaccessible_callback(self, name, **kwargs):
        basic_auth = BasicAuth(app)
        return redirect(basic_auth.challenge())


class RoleAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "name"
    ]
    column_filters = [
        "id",
        "name"
    ]


class UserAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    column_hide_backrefs = False
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "first_name",
        "last_name",
        "email",
        "picture",
        "role_id",
        "google",
        "facebook",
    ]
    column_filters = [
        "id",
        "first_name",
        "last_name",
        "email",
        "picture",
        "role_id",
        "google",
        "facebook",
    ]


class CourseAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "name",
        "description",
        "is_active",
        "status",
        "owner_id",
        "price",
        "date",

    ]
    column_filters = [
        "id",
        "name",
        "description",
        "is_active",
        "status",
        "owner_id",
        "price",
        "date",
    ]


class TaskAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "name",
        "description",
        "course_id",
        "task_number",
        "format",
        "test",
        "max_points"
    ]
    column_filters = [
        "id",
        "name",
        "description",
        "course_id",
        "task_number",
        "format",
        "test",
        "max_points"
    ]


class GroupsAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "name",
        "max_members",
        "course_id"
    ]
    column_filters = [
        "id",
        "name",
        "max_members",
        "course_id"
    ]


class BoardAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "group_id",
        "is_active",
        "task_id"
    ]
    column_filters = [
        "id",
        "group_id",
        "is_active",
        "task_id"
    ]


class ParticipantAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "user_id",
        "course_id",
        "group_id"
    ]
    column_filters = [
        "id",
        "user_id",
        "course_id",
        "group_id"
    ]


class StudentAnswerAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "course_id",
        "group_id",
        "task_id",
        "answers",
        "grade",
        "student_id",
        "date"
    ]
    column_filters = [
        "id",
        "course_id",
        "group_id",
        "task_id",
        "answers",
        "grade",
        "student_id",
        "date"
    ]


class ResultAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "course_id",
        "group_id",
        "student_id",
        "grade",
        "date"
    ]
    column_filters = [
        "id",
        "course_id",
        "group_id",
        "student_id",
        "grade",
        "date"
    ]


class KeysAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "user_id",
        "course_id",
        "group_id",
        "key"
    ]
    column_filters = [
        "id",
        "user_id",
        "course_id",
        "group_id",
        "key"
    ]


class PaymentsAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "payment_id",
        "user_id",
        "course_id",
        "group_id",
        "date"
    ]
    column_filters = [
        "id",
        "payment_id",
        "user_id",
        "course_id",
        "group_id",
        "date"
    ]


class EventsAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "owner_id",
        "course_id",
        "group_id",
        "date",
        "subject",
        "body",
        "task_ids"
    ]
    column_filters = [
        "id",
        "owner_id",
        "course_id",
        "group_id",
        "date",
        "subject",
        "body",
        "task_ids"
    ]


class CourseApprovalRequestsAdmin(ModelView):
    action_disallowed_list = ["delete", ]
    column_display_pk = True
    create_modal = True
    edit_modal = True
    column_list = [
        "id",
        "course_id",
        "owner_id",
        "moderator_id",
        "status",
        "note",
        "date"
    ]
    column_filters = [
        "id",
        "course_id",
        "owner_id",
        "moderator_id",
        "status",
        "note",
        "date"
    ]

