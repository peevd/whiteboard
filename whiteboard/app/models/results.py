from app import db
from flask_sqlalchemy import inspect


class Result(db.Model):
    __tablename__ = "results"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)
    grade = db.Column(db.String(100))
    date = db.Column(db.DateTime)

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["date"] = data["date"].strftime("%Y-%m-%d %H:%M")
        return data

