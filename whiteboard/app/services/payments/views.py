from . import api
from ... import db
from ...models.users import User
from ...models.groups import Group
from ...models.courses import Course
from ...models.payments import Payment
from ...models.keys import Key
from ...models.participants import Participant
from ..utils import parser, parse_token, auth_check, is_course_owner, \
                is_admin, is_teacher

from flask import current_app as app
from flask_restful import Resource
import stripe
import datetime

parser_get = parser.copy()
parser_get.add_argument("f", required=True,
                        location="args",
                        help="Missing argument!")
parser_get.add_argument("c_id", required=False,
                        location="args")
parser_get.add_argument("g_id", required=False,
                        location="args")
parser_get.add_argument("u_id", required=False,
                        location="args")

parser_post = parser.copy()
parser_post.add_argument("c_id", required=True,
                         type=int,
                         location="json",
                         help="Missing argument!")
parser_post.add_argument("g_id", required=True,
                         type=int,
                         location="json",
                         help="Missing argument!")
parser_post.add_argument("email", required=True,
                         location="json",
                         help="Missing argument!")
parser_post.add_argument("stripeToken", required=False,
                         location="json")


class Payments(Resource):
    # GET payments information
    @auth_check
    def get(self):
        args = parser_get.parse_args()
        token = parse_token(args["Authorization"])

        if is_teacher(token):
            if args["f"] == "all":
                payments = []
                main_courses = Course.query.filter_by(owner_id=token["sub"])
                for course in main_courses:
                    course_data = {}
                    course_data["course_id"] = course.id
                    course_data["name"] = course.name
                    course_data["price"] = course.price
                    course_data["groups"] = []

                    course_groups = Group.query.filter_by(course_id=course.id)
                    for group in course_groups:
                        gr_part_count = Participant.query.filter_by(course_id=course.id,
                                                                    group_id=group.id).count()
                        group_data = {}
                        group_data["group_id"] = group.id
                        group_data["name"] = group.name
                        group_data["participants"] = gr_part_count
                        group_data["group_price"] = gr_part_count * course.price

                        course_data["groups"].append(group_data)
                    payments.append(course_data)
                return payments, 200

            elif args["f"] == "byCourse":
                if args["c_id"] is None:
                    return {
                        "message": "Missing argument!"
                    }, 409

                c_course = Course.query.filter_by(id=args["c_id"]).first()

                if is_course_owner(token, c_course):
                    course_data = {}
                    course_data["course_id"] = c_course.id
                    course_data["name"] = c_course.name
                    course_data["price"] = c_course.price
                    course_data["groups"] = []

                    course_groups = Group.query.filter_by(course_id=args["c_id"])
                    for group in course_groups:
                        gr_part_count = Participant.query.filter_by(course_id=args["c_id"],
                                                                    group_id=group.id).count()
                        group_data = {}
                        group_data["group_id"] = group.id
                        group_data["name"] = group.name
                        group_data["participants"] = gr_part_count
                        group_data["group_price"] = gr_part_count * c_course.price

                        course_data["groups"].append(group_data)
                    return course_data, 200

                else:
                    return {
                        "message": "Permission denied!"
                    }, 409
            elif args["f"] == "byCourseGroup":
                if args["c_id"] is None or args["g_id"] is None:
                    return {
                        "message": "Missing argument!"
                    }, 409

                c_course = Course.query.filter_by(id=args["c_id"]).first()

                if is_course_owner(token, c_course):
                    course_data = {}
                    course_data["course_id"] = c_course.id
                    course_data["name"] = c_course.name
                    course_data["price"] = c_course.price

                    c_group = Group.query.filter_by(id=args["g_id"],
                                                    course_id=args["c_id"]).first()
                    if c_group is None:
                        return {
                            "message": "Group not Found!"
                        }, 404

                    gr_part_count = Participant.query.filter_by(course_id=args["c_id"],
                                                                group_id=args["g_id"]).count()
                    group_data = {}
                    group_data["group_id"] = c_group.id
                    group_data["name"] = c_group.name
                    group_data["participants"] = gr_part_count
                    group_data["group_price"] = gr_part_count * c_course.price

                    course_data["group"] = group_data
                    return course_data, 200
                else:
                    return {
                        "message": "Permission denied!"
                    }, 403
            else:
                return {
                    "message": "Bad argument value!"
                }, 409

        elif is_admin(token):
            if args["f"] == "byCourse":
                if args["c_id"] is None:
                    return {
                        "message": "Missing argument!"
                    }, 409

                c_course = Course.query.filter_by(id=args["c_id"]).first()

                if c_course is None:
                    return {
                        "message": "Course not Found!"
                    }, 404

                course_data = {}
                course_data["course_id"] = c_course.id
                course_data["name"] = c_course.name
                course_data["price"] = c_course.price
                course_data["groups"] = []

                course_groups = Group.query.filter_by(course_id=args["c_id"])
                for group in course_groups:
                    gr_participants = Participant.query.filter_by(course_id=args["c_id"],
                                                                  group_id=group.id)

                    participants_data = []
                    for participant in gr_participants:
                        participant_data = {}
                        part_payment = Payment.query.filter_by(user_id=participant.user_id,
                                                               course_id=c_course.id).first()
                        participant_data["part_id"] = participant.id
                        participant_data["user_id"] = participant.user_id
                        c_user = User.query.filter_by(id=participant.user_id).first()

                        participant_data["user_name"] = c_user.first_name + " " + c_user.last_name
                        participant_data["payment_id"] = part_payment.id
                        participant_data["payment_code"] = part_payment.payment_id
                        participant_data["payment_date"] = part_payment.date.strftime("%Y-%m-%d %H:%M")

                        participants_data.append(participant_data)

                    group_data = {}
                    group_data["group_id"] = group.id
                    group_data["name"] = group.name
                    group_data["participants"] = gr_participants.count()
                    group_data["group_price"] = gr_participants.count() * c_course.price
                    group_data["participants_data"] = participants_data

                    course_data["groups"].append(group_data)

                return course_data, 200

            if args["f"] == "byCourseGroup":
                if args["c_id"] is None or args["g_id"] is None:
                    return {
                        "message": "Missing argument!"
                    }, 409

                c_course = Course.query.filter_by(id=args["c_id"]).first()

                if c_course is None:
                    return {
                        "message": "Course not Found!"
                    }, 404

                course_data = {}
                course_data["course_id"] = c_course.id
                course_data["name"] = c_course.name
                course_data["price"] = c_course.price

                c_group = Group.query.filter_by(id=args["g_id"],
                                                course_id=args["c_id"]).first()
                if c_group is None:
                    return {
                        "message": "Group not Found!"
                    }, 404

                gr_participants = Participant.query.filter_by(course_id=args["c_id"],
                                                              group_id=args["g_id"])
                participants_data = []
                for participant in gr_participants:
                    participant_data = {}
                    part_payment = Payment.query.filter_by(user_id=participant.user_id,
                                                           course_id=c_course.id).first()
                    participant_data["part_id"] = participant.id
                    participant_data["user_id"] = participant.user_id
                    c_user = User.query.filter_by(id=participant.user_id).first()

                    participant_data["user_name"] = c_user.first_name + " " + c_user.last_name
                    participant_data["payment_id"] = part_payment.id
                    participant_data["payment_code"] = part_payment.payment_id
                    participant_data["payment_date"] = part_payment.date.strftime("%Y-%m-%d %H:%M")

                    participants_data.append(participant_data)

                group_data = {}
                group_data["group_id"] = c_group.id
                group_data["name"] = c_group.name
                group_data["participants"] = gr_participants.count()
                group_data["group_price"] = gr_participants.count() * c_course.price
                group_data["participans_data"] = participants_data

                course_data["group"] = group_data
                return course_data, 200

            if args["f"] == "byUserID":
                if args["u_id"] is None:
                    return {
                        "message": "Missing argument!"
                    }, 404

                c_user = User.query.filter_by(id=args["u_id"]). first()
                if c_user is None:
                    return {
                        "message": "User not Found!"
                    }, 404

                user_courses = Course.query.filter_by(owner_id=args["u_id"])

                payments = []
                for course in user_courses:
                    course_data = {}
                    course_data["course_id"] = course.id
                    course_data["name"] = course.name
                    course_data["price"] = course.price
                    course_data["groups"] = []

                    course_groups = Group.query.filter_by(course_id=course.id)
                    for group in course_groups:
                        gr_participants = Participant.query.filter_by(course_id=course.id,
                                                                      group_id=group.id)

                        participants_data = []
                        for participant in gr_participants:
                            participant_data = {}
                            part_payment = Payment.query.filter_by(user_id=participant.user_id,
                                                                   course_id=course.id).first()
                            participant_data["part_id"] = participant.id
                            participant_data["user_id"] = participant.user_id
                            c_user = User.query.filter_by(id=participant.user_id).first()

                            participant_data["user_name"] = c_user.first_name + " " + c_user.last_name
                            participant_data["payment_id"] = part_payment.id
                            participant_data["payment_code"] = part_payment.payment_id
                            participant_data["payment_date"] = part_payment.date.strftime("%Y-%m-%d %H:%M")

                            participants_data.append(participant_data)

                        group_data = {}
                        group_data["group_id"] = group.id
                        group_data["name"] = group.name
                        group_data["participants"] = gr_participants.count()
                        group_data["group_price"] = gr_participants.count() * course.price
                        group_data["participans_data"] = participants_data

                        course_data["groups"].append(group_data)
                    payments.append(course_data)
                return payments, 200
            else:
                return {
                    "message": "Permission denied!"
                }, 403

    # POST payment for course
    @auth_check
    def post(self):
        args = parser_post.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=args["c_id"]).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        c_group = Group.query.filter_by(id=args["g_id"]).first()
        if c_group is None:
            return {
                "message": "Group not Found!"
            }, 404

        keys = Key.query.filter_by(course_id=args["c_id"], group_id=args["g_id"])
        all_participants = Participant.query.filter_by(group_id=args["g_id"])
        if keys.count() + all_participants.count() >= c_group.max_members:
            return {
                "message": "This group is full already!"
            }, 409

        c_participant = Participant.query.filter_by(user_id=token["sub"],
                                                    course_id=args["c_id"]).first()
        if c_participant is not None:
            return {
                "message": "Student already participating in this course!"
            }, 409

        user = User.query.filter_by(id=token["sub"]).first()

        if c_course.status == "open":
            if args["stripeToken"] is None:
                return {
                    "message": "Missing argument!"
                }, 404

            if c_course.price > 0:
                stripe_keys = {
                    "secret_key": app.config["STRIPE_SECRET_KEY"],
                    "publishable_key": app.config['STRIPE_PUBLISHABLE_KEY']
                }

                stripe.api_key = stripe_keys['secret_key']

                amount = int(c_course.price * 100)

                customer = stripe.Customer.create(
                    email=user.email,
                    source=args["stripeToken"]
                )

                charge = stripe.Charge.create(
                    customer=customer.id,
                    amount=amount,
                    currency="usd",
                    description="Course payment",
                    receipt_email=args["email"]
                )

                if charge.status == "succeeded":
                    new_participant = Participant(
                        user_id=token["sub"],
                        course_id=args["c_id"],
                        group_id=args["g_id"]
                        )
                    db.session.add(new_participant)
                    db.session.commit()

                    today = datetime.datetime.now()
                    new_payment = Payment(
                        payment_id=charge["id"],
                        user_id=user.id,
                        course_id=args["c_id"],
                        group_id=args["g_id"],
                        date=today.isoformat()
                    )
                    db.session.add(new_payment)
                    db.session.commit()
                else:
                    return {
                        "message": "Payment unsuccessful!"
                    }, 205

                return new_participant.toDict(), 201

            if c_course.price == 0:
                new_participant = Participant(
                    user_id=token["sub"],
                    course_id=args["c_id"],
                    group_id=args["g_id"]
                    )
                db.session.add(new_participant)
                db.session.commit()

                return new_participant.toDict(), 201
        else:
            return {
                "message": "This course is not active!"
            }, 409


api.add_resource(Payments, "/api/payments")

