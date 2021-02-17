from app import db
from flask_sqlalchemy import inspect


class StudentAnswer(db.Model):
    __tablename__ = "studentAnswers"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    task_id = db.Column(db.Integer, db.ForeignKey("tasks.id"))
    answers = db.Column(db.UnicodeText)
    grade = db.Column(db.Float)
    student_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date = db.Column(db.DateTime)

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["date"] = data["date"].strftime("%Y-%m-%d %H:%M")
        return data

