from app import db
from flask_sqlalchemy import inspect


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    description = db.Column(db.Text())
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    task_number = db.Column(db.Integer)
    format = db.Column(db.Integer)
    test = db.Column(db.UnicodeText)
    max_points = db.Column(db.Integer)

    child_student_answers = db.relationship("StudentAnswer",
                                            cascade="all,delete", backref="tasks")

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        return data

