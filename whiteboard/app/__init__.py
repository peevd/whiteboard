from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from config import app_config
from flask_socketio import SocketIO

import flask_admin as admin
from flask_admin.contrib.fileadmin import FileAdmin

# from flask_admin.menu import MenuLink

socketio = SocketIO(path="/whiteboard.io")
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    migrate = Migrate(app, db)
    CORS(app)

    adm = admin.Admin(app, url="/miagi")
    # adm = admin.Admin(app)

    from app.models import roles
    from app.models import users
    from app.models import courses
    from app.models import approval_requests
    from app.models import participants
    from app.models import boards
    from app.models import tasks
    from app.models import student_answers
    from app.models import groups
    from app.models import keys
    from app.models import results
    from app.models import payments
    from app.models import events

    from .services.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .services.courses import courses as courses_blueprint
    app.register_blueprint(courses_blueprint)

    from .services.approval_requests import approvalRequest as approvalRequest_blueprint
    app.register_blueprint(approvalRequest_blueprint)

    from .services.user import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from .services.tasks import tasks as tasks_blueprint
    app.register_blueprint(tasks_blueprint)

    from .services.groups import groups as groups_blueprint
    app.register_blueprint(groups_blueprint)

    from .services.events import events as events_blueprint
    app.register_blueprint(events_blueprint)

    from .services.participants import participants as participants_blueprint
    app.register_blueprint(participants_blueprint)

    from .socket_events import chatEvents as chatEvents_blueprint
    app.register_blueprint(chatEvents_blueprint)

    from .services.student_answers import studentAsnswers as studentAsnswers_blueprint
    app.register_blueprint(studentAsnswers_blueprint)

    from .services.results import results as results_blueprint
    app.register_blueprint(results_blueprint)

    from .services.keys import keys as keys_blueprint
    app.register_blueprint(keys_blueprint)

    from .services.payments import payments as payments_blueprint
    app.register_blueprint(payments_blueprint)

    from .services.admin import adm as admin_blueprint
    app.register_blueprint(admin_blueprint)

    # from .services.admin_test import adam as adam_blueprint
    # app.register_blueprint(adam_blueprint)

    # Declare socket
    socketio.init_app(app)

    from .models.roles import Role

    # Declare default objects in db
    @app.before_first_request
    def init_roles():
        if Role.query.count() == 0:
            db.session.add(Role(id=1, name='admin'))
            db.session.add(Role(id=2, name='moderator'))
            db.session.add(Role(id=3, name='teacher'))
            db.session.add(Role(id=4, name='student'))
            db.session.commit()

    # ADD Admin UI
    from .services.admin.views import RoleAdmin, UserAdmin, CourseAdmin, \
        TaskAdmin, GroupsAdmin, BoardAdmin, ParticipantAdmin, \
        StudentAnswerAdmin, ResultAdmin, KeysAdmin, PaymentsAdmin, EventsAdmin, \
        CourseApprovalRequestsAdmin

    adm.add_view(RoleAdmin(roles.Role, db.session))
    adm.add_view(UserAdmin(users.User, db.session))
    adm.add_view(CourseAdmin(courses.Course, db.session))
    adm.add_view(TaskAdmin(tasks.Task, db.session))
    adm.add_view(GroupsAdmin(groups.Group, db.session))
    adm.add_view(EventsAdmin(events.Event, db.session))
    adm.add_view(BoardAdmin(boards.Board, db.session))
    adm.add_view(ParticipantAdmin(participants.Participant, db.session))
    adm.add_view(StudentAnswerAdmin(student_answers.StudentAnswer, db.session))
    adm.add_view(ResultAdmin(results.Result, db.session))
    adm.add_view(KeysAdmin(keys.Key, db.session))
    adm.add_view(PaymentsAdmin(payments.Payment, db.session))
    adm.add_view(CourseApprovalRequestsAdmin(approval_requests.CourseApprovalRequest, db.session))

    path = app.config["B_DATA_FILES_DIR"]
    adm.add_view(FileAdmin(path, name='Static Files'))

    # from .services.admin_test import RoleAdmin, UserAdmin, CourseAdmin, TaskAdmin
    #
    # adm.add_view(RoleAdmin(roles.Role, db.session))
    # adm.add_view(UserAdmin(users.User, db.session))
    # adm.add_view(CourseAdmin(courses.Course, db.session))
    # adm.add_view(TaskAdmin(tasks.Task, db.session))
    #
    # adm.add_link(MenuLink(name='Logout', endpoint='adam.logout'))
    return app

