from . import api
from ... import db
from ...models.courses import Course
from ...models.student_answers import StudentAnswer
from ...models.tasks import Task
from ...models.participants import Participant
from ..utils import parser, parse_token, auth_check, is_course_owner, \
        self_participates, is_admin

import json
import datetime
from flask import request
from flask_restful import Resource

parser_get = parser.copy()
parser_get.add_argument("p", required=True,
                        location="args")

parser_put = parser.copy()
parser_put.add_argument("p", required=True,
                        type=int,
                        location="args")
parser_put.add_argument("grade", required=True,
                        type=int,
                        location="json",
                        help="Missing Argument!")


class StudentAnswersGet(Resource):
    # GET answers for all tasks /for current participant ?p=<int>/ for self ?p=me
    @auth_check
    def get(self, c_id):
        args = parser_get.parse_args()
        token = parse_token(args["Authorization"])
        answers_list = []

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if args["p"] == "me":
            if self_participates(token, c_id):
                all_course_tasks = Task.query.filter_by(course_id=c_id)
                for task in all_course_tasks:
                    c_answer = StudentAnswer.query.filter_by(student_id=token["sub"],
                                                             task_id=task.id,
                                                             course_id=c_id).first()
                    if c_answer is None:
                        continue

                    # Open question case
                    if task.format == 2:
                        answers_list.append(c_answer.toDict())

                    # Test case
                    if task.format == 1:
                        c_answer = c_answer.toDict()
                        c_answer["answers"] = json.loads(c_answer["answers"])
                        answers_list.append(c_answer)
                return answers_list, 200
            else:
                return {
                    "message": "You dont participate in this course!"
                }, 403

        else:
            try:
                int(args["p"])
            except ValueError:
                return {
                    "message": "Bad request argument!"
                }, 400

            if is_course_owner(token, c_course) or is_admin(token):
                c_participant = Participant.query.filter_by(id=args["p"],
                                                            course_id=c_id).first()
                if c_participant is None:
                    return {
                        "message": "Student not found in this course register!"
                    }, 404

                all_course_tasks = Task.query.filter_by(course_id=c_id)
                for task in all_course_tasks:
                    c_answer = StudentAnswer.query.filter_by(student_id=c_participant.user_id,
                                                             task_id=task.id,
                                                             course_id=c_id).first()
                    if c_answer is None:
                        continue

                    # Open question case
                    if task.format == 2:
                        answers_list.append(c_answer.toDict())

                    # Test case
                    if task.format == 1:
                        c_answer = c_answer.toDict()
                        c_answer["answers"] = json.loads(c_answer["answers"])
                        answers_list.append(c_answer)
                return answers_list, 200
            else:
                return {
                    "message": "Permission denied!"
                }, 403


api.add_resource(StudentAnswersGet, "/api/courses/<int:c_id>/answers")


class StudentAnswers(Resource):
    # ADD answer for current task in course
    @auth_check
    def post(self, c_id, t_id):
        args = parser.parse_args()
        token = parse_token(args["Authorization"])

        data = request.get_json()
        student_data = data["answers"]

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

        mine_register = Participant.query.filter_by(user_id=token["sub"],
                                                    course_id=c_id).first()
        if mine_register is None:
            return {
                "message": "User not found in course register!"
            }, 404

        answer_check = StudentAnswer.query.filter_by(student_id=token["sub"],
                                                     task_id=t_id,
                                                     course_id=c_id).first()
        if answer_check is not None:
            return {
                "message": "Answer already exist!"
            }, 409

        # Open question case
        if c_task.format == 2:
            if type(student_data) is str:
                today = datetime.datetime.now()
                answer = StudentAnswer(
                    course_id=c_id,
                    group_id=mine_register.group_id,
                    task_id=t_id,
                    answers=student_data,
                    student_id=token["sub"],
                    date=today.isoformat()
                    )
                db.session.add(answer)
                db.session.commit()
                return answer.toDict(), 201
            else:
                return {
                    "message": "Bad argument in JSON!"
                }, 400

        # Test case
        if c_task.format == 1:
            if type(student_data) is list:
                task_to_dict = c_task.toDict()
                c_test = json.loads(task_to_dict["test"])
                correct_ans = c_test["correctAnswers"]

                percent_per_question = 100 / len(correct_ans)
                questions_success_percents = []

                # Check for duplicated questions ID's in student request data!
                parsed_q_ids = [x["q_id"] for x in student_data]
                if (any(parsed_q_ids.count(x) > 1 for x in parsed_q_ids)):
                    return {
                        "message": "Founded duplicated question ID's!"
                    }, 400

                # Check is count of answers is equal to count of questions in this task!
                if len(parsed_q_ids) != len(c_test["questions"]):
                    return {
                        "message": "Difference beween count of test questions and count of answers!"
                    }, 400

                if c_test["computing_system"] == 1:
                    for st_answ in student_data:
                        question_succes = 0
                        percent_per_answ = percent_per_question / len(correct_ans[str(st_answ["q_id"])])

                        # Check for duplicated answers ID's for current question in student request data!
                        if (any(st_answ["a_id"].count(x) > 1 for x in st_answ["a_id"])):
                            return {
                                "message": "Founded duplicated answers ID's for current question!"
                            }, 400

                        # Check if count of answers ID's for current question in
                        # student request data is not bigger
                        # than count of correct answers for this question!
                        # This check only if "computing_system" is set to 1
                        if len(st_answ["a_id"]) > len(correct_ans[str(st_answ["q_id"])]):
                            return {
                                "message": "More answers than needed!"
                            }, 400

                        for ans in st_answ["a_id"]:
                            if ans in correct_ans[str(st_answ["q_id"])]:
                                question_succes += percent_per_answ

                        questions_success_percents.append(question_succes)
                    result = sum(questions_success_percents)

                if c_test["computing_system"] == 2:
                    for st_answ in student_data:
                        question_succes = 0
                        percent_per_answ = percent_per_question / len(correct_ans[str(st_answ["q_id"])])

                        if len(st_answ["a_id"]) > 100:
                            return {
                                "message": "Too many question answers in student request data!"
                            }, 400

                        # Check for duplicated answers ID's for current question in student request data!
                        if (any(st_answ["a_id"].count(x) > 1 for x in st_answ["a_id"])):
                            return {
                                "message": "Founded duplicated answers for current question!"
                            }, 400

                        for ans in st_answ["a_id"]:
                            if ans in correct_ans[str(st_answ["q_id"])]:
                                question_succes += percent_per_answ

                        if len(st_answ["a_id"]) > len(correct_ans[str(st_answ["q_id"])]):
                            over_answs = (len(st_answ["a_id"]) - len(correct_ans[str(st_answ["q_id"])]))
                            question_succes -= over_answs * percent_per_answ

                        questions_success_percents.append(question_succes)
                    result = sum(questions_success_percents)
                    if result < 0:
                        result = 0

                str_st_answer = json.dumps(student_data)

                today = datetime.datetime.now()
                answer = StudentAnswer(
                    course_id=c_id,
                    group_id=mine_register.group_id,
                    task_id=t_id,
                    answers=str_st_answer,
                    grade=result,
                    student_id=token["sub"],
                    date=today.isoformat()
                )
                db.session.add(answer)
                db.session.commit()
                return {
                    "message": "Test is ok"
                }, 201
            else:
                return {
                    "message": "Bad argument in JSON!"
                }, 400


api.add_resource(StudentAnswers, "/api/courses/<int:c_id>/tasks/<int:t_id>/answers")


class StudentAnswerGrade(Resource):
    # Put request for teacher to add grade for answer/s
    @auth_check
    def put(self, c_id, t_id):
        args = parser_put.parse_args()
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

        if is_course_owner(token, c_course):
            c_participant = Participant.query.filter_by(id=args["p"],
                                                        course_id=c_id).first()

            c_answer = StudentAnswer.query.filter_by(student_id=c_participant.user_id,
                                                     task_id=t_id,
                                                     course_id=c_id).first()
            if c_answer is None:
                return {
                    "message": "Answer not Found!"
                }, 404
            today = datetime.datetime.now()
            c_answer.grade = args["grade"]
            c_answer.date = today.isoformat()
            db.session.commit()

            return c_answer.toDict(), 200
        else:
            return {
                "message": "Permission denied!"
            }, 403


api.add_resource(StudentAnswerGrade, "/api/courses/<int:c_id>/tasks/<int:t_id>/grades")


class StudentAnswersGrade(Resource):
    # Get grade for course
    @auth_check
    def get(self, c_id):
        args = parser_get.parse_args()
        token = parse_token(args["Authorization"])

        c_course = Course.query.filter_by(id=c_id).first()
        if c_course is None:
            return {
                "message": "Course not Found!"
            }, 404

        if args["p"] == "me":
            if self_participates(token, c_id):
                all_course_task = Task.query.filter_by(course_id=c_id)
                max_score = all_course_task.count() * 100

                all_answers = StudentAnswer.query.filter_by(student_id=token["sub"],
                                                            course_id=c_id)
                student_score = 0
                missing_grade = False
                for answer in all_answers:
                    if answer.grade is None:
                        missing_grade = True
                        continue
                    student_score += answer.grade

                grade = (student_score / max_score) * 100

                missing_answers = False
                if all_course_task.count() > all_answers.count():
                    missing_answers = True

                return {
                    "grade": grade,
                    "missing_answers": missing_answers,
                    "missing_grade": missing_grade
                }, 200
            else:
                return{
                    "message": "You not found in course register!"
                }, 404
        else:
            try:
                int(args["p"])
            except ValueError:
                return {
                    "message": "Bad request argument!"
                }, 400

            if is_course_owner(token, c_course) or is_admin(token):
                c_participant = Participant.query.filter_by(id=args["p"],
                                                            course_id=c_id).first()
                if c_participant is None:
                    return {
                        "message": "Student not found in this course register!"
                    }, 404

                all_course_task = Task.query.filter_by(course_id=c_id)
                max_score = all_course_task.count() * 100

                all_answers = StudentAnswer.query.filter_by(student_id=c_participant.user_id,
                                                            course_id=c_id)
                student_score = 0
                missing_grade = False
                for answer in all_answers:
                    if answer.grade is None:
                        missing_grade = True
                        continue
                    student_score += answer.grade

                grade = (student_score / max_score) * 100

                missing_answers = False
                if all_course_task.count() > all_answers.count():
                    missing_answers = True

                return {
                    "grade": grade,
                    "missing_answers": missing_answers,
                    "missing_grade": missing_grade
                }, 200
            else:
                return {
                    "message": "Permission denied!"
                }, 403


api.add_resource(StudentAnswersGrade, "/api/courses/<int:c_id>/grades")


class StudentAnswersExist(Resource):
    # Check if answer exist
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

        if self_participates(token, c_id):
            student_answers = StudentAnswer.query.filter_by(course_id=c_id,
                                                            task_id=t_id,
                                                            student_id=token["sub"]).first()
            if student_answers is not None:
                answer_check = True
            else:
                answer_check = False

            return {
                "exists": answer_check
            }, 200
        else:
            return {
                "message": "User not Found in course register!"
            }, 404


api.add_resource(StudentAnswersExist, "/api/courses/<int:c_id>/tasks/<int:t_id>/answers/exist")

