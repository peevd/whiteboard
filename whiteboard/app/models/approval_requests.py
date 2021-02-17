from app import db
from flask_sqlalchemy import inspect


class CourseApprovalRequest(db.Model):
    __tablename__ = "courseApprovalRequests"

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    moderator_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # asjdk
    status = db.Column(db.Integer)  # new - 1/ needs fixing - 2/ approved - 3
    note = db.Column(db.UnicodeText)
    date = db.Column(db.DateTime)

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["date"] = data["date"].strftime("%Y-%m-%d %H:%M")
        return data

