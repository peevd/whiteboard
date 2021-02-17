from flask_restful import reqparse
import jwt
from jwt import DecodeError, ExpiredSignature
from flask import current_app as app
from functools import wraps
from ..models.users import User
from ..models.groups import Group
from ..models.participants import Participant
from ..models.tasks import Task

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import random
import hashlib

"""+++++++++++++++++++++++   AUTHENTICATION CHECK   ++++++++++++++++++++++++"""


parser = reqparse.RequestParser()
parser.add_argument("Authorization",
                    location="headers", required=True)


def parse_token(token):
    t = token.split()[1]
    return jwt.decode(t, app.config["TOKEN_SECRET"])


def auth_check(funk):
    @wraps(funk)
    def duth_dec(*args, **kwargs):
        args = parser.parse_args()
        try:
            token = parse_token(args["Authorization"])
        except DecodeError:
            return {"message": "Token invalid!"}, 401
        except ExpiredSignature:
            return {"message": "Token has expired"}, 401
        return funk(*args, **kwargs)
    return duth_dec


def admin_check(funk):
    @wraps(funk)
    def duth_dec(*args, **kwargs):
        args = parser.parse_args()
        try:
            token = parse_token(args["Authorization"])
            user = User.query.filter_by(id=token["sub"]).first()
            if user.role_id != 1:
                return "Not Admin", 403
        except DecodeError:
            return {"message": "Token invalid!"}, 401
        except ExpiredSignature:
            return {"message": "Token has expired"}, 401
        return funk(*args, **kwargs)
    return duth_dec


"""+++++++++++++++++++++++++++   ROLES CHECKS   +++++++++++++++++++++++++++++"""


def is_teacher(token):
    user = User.query.filter_by(id=token["sub"]).first()
    if user is None:
        return {
            "message": "User not Found!"
        }, 404
    else:
        if user.role_id == 3:
            return True
        else:
            return False


def is_moderator(token):
    user = User.query.filter_by(id=token["sub"]).first()
    if user is None:
        return {
            "message": "User not Found!"
        }, 404
    else:
        if user.role_id == 2:
            return True
        else:
            return False


def is_admin(token):
    user = User.query.filter_by(id=token["sub"]).first()
    if user is None:
        return {
            "message": "User not Found!"
        }, 404
    else:
        if user.role_id == 1:
            return True
        else:
            return False


def is_student(token):
    user = User.query.filter_by(id=token["sub"]).first()
    if user is None:
        return {
            "message": "User not Found!"
        }, 404
    else:
        if user.role_id == 4:
            return True
        else:
            return False


"""+++++++++++++++++++++++++   PERMISSION  CHECKS   +++++++++++++++++++++++++"""


def self_participates(token, c_id):
    mine_register = Participant.query.filter_by(user_id=token["sub"],
                                                course_id=c_id).first()
    if mine_register is not None:
        return True
    else:
        return False


def self_part_course_group(token, c_id, g_id):
    mine_register = Participant.query.filter_by(user_id=token["sub"],
                                                course_id=c_id,
                                                group_id=g_id).first()
    if mine_register is not None:
        return True
    else:
        return False


def user_participates(u_id, c_id):
    mine_register = Participant.query.filter_by(user_id=u_id,
                                                course_id=c_id).first()
    if mine_register is not None:
        return True
    else:
        return False


def is_course_owner(token, c_course):
    if c_course.owner_id == token["sub"]:
        return True
    else:
        return False


def is_event_owner(token, c_event):
    if token["sub"] == c_event.owner_id:
        return True
    else:
        return False


def is_request_owner(token, c_request):
    if token["sub"] == c_request.owner_id:
        return True
    else:
        return False


"""+++++++++++++++++++++++++++   EXISTS  CHECKS   +++++++++++++++++++++++++++"""


def group_exist(g_id, c_id):
    c_group = Group.query.filter_by(id=g_id, course_id=c_id).first()
    if c_group is not None:
        return True
    else:
        return False


"""++++++++++++++++++++++++++++   EMAIL SENDER   ++++++++++++++++++++++++++++"""


# Invitation Email for student
def create_invitation_mail_body(student_name, course_name, group_name, URL):
    subject = "Invitation for course in Whiteboard.me!"
    body = """
Hello Mr./Ms. %s

    Whiteboard.me send this email to invite you in Course: %s Group: %s!

    For registration for this course click the link below:
    %s

Best Regards,
Whiteboard team\
""" % (student_name, course_name, group_name, URL)

    mail_content = {}
    mail_content["subject"] = subject
    mail_content["body"] = body
    return mail_content


def create_admin_approval_request_mail_body(owner_last_name, course_name,
                                            course_id, status, note):
    subject = "Course approval request answer!"
    URL = "%s#/my-courses/%s" % (app.config["HOST"], course_id)
    if status == 2:
        body = """\
Hello Mr./Ms. %s

    Whiteboard send this mail to let you know that our team found content
    in your course '%s', that does not comply with site requirements!

    Please check our suggestions how to change content(s) and resend request:
        " %s "

    Go to course:
    %s

Best Regards,
Whiteboard team\
""" % (owner_last_name, course_name, note, URL)

    elif status == 3:

        body = """\
Hello Mr./Ms. %s

    Whiteboard send this mail to let you know that our team approve
    your course '%s', and now you can start work with it!

    Go to course:
    %s

Best Regards,
Whiteboard team\
""" % (owner_last_name, course_name, URL)

    mail_content = {}
    mail_content["subject"] = subject
    mail_content["body"] = body
    return mail_content


# Email with reson for closing active course (only for admin)
def closing_course_reason_mail_body(owner_last_name, course_name, reason):
    subject = "Reason for closing course in Whiteboard.me!"
    body = """
Hello Mr./Ms. %s

    Whiteboard.me send this email to inform you that Course: %s is closed!

    The reason for closing this course can read below:
    %s

    Please connect with Whiteboard team for more information!

Best Regards,
Whiteboard team\
""" % (owner_last_name, course_name, reason)

    mail_content = {}
    mail_content["subject"] = subject
    mail_content["body"] = body
    return mail_content


def mail_sender(to_addr, mail_content):
    msg = MIMEMultipart()
    msg["From"] = app.config["FROM_ADDR"]
    msg["To"] = to_addr
    msg["Subject"] = mail_content["subject"]

    body = mail_content["body"]

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(app.config["SMTP_SERVER"], app.config["SMTP_SERVER_PORT"])
    server.starttls()
    server.login(app.config["FROM_ADDR"], app.config["EMAIL_PASS"])
    text = msg.as_string()
    server.sendmail(app.config["FROM_ADDR"], to_addr, text)
    server.quit()


def key_gen(c_id, g_id, u_id, date):
    string = str(c_id) + str(g_id) + str(u_id) + str(date)
    key = hashlib.sha224(bytes(string, encoding="utf8")).hexdigest()
    return key


def url_gen(c_id, g_id, key):
    invitation_url = "%s#/joined-courses/%s?gId=%s&key=%s" % (app.config["HOST"], c_id, g_id, key)
    return invitation_url


"""+++++++++++++++++++++++++++   FILE CHECK/GET   +++++++++++++++++++++++++++"""


# Check is file extension is in allowed register
def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


"""++++++++++++++++++++++++++   EVENTS TASK INFO   ++++++++++++++++++++++++++"""


def get_tasks_info(task_ids):
    task_ids = task_ids.split(",")
    task_ids = [int(x) for x in task_ids]
    task_data = []
    for task_id in task_ids:
        c_task = Task.query.filter_by(id=task_id).first()
        test_dict_data = {}
        test_dict_data["id"] = c_task.id
        test_dict_data["name"] = c_task.name
        test_dict_data["description"] = c_task.description
        task_data.append(test_dict_data)
    return task_data

