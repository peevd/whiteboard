from app import db
from flask_sqlalchemy import inspect


class Event(db.Model):
    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    date = db.Column(db.DateTime)
    subject = db.Column(db.String(100))
    body = db.Column(db.UnicodeText)
    task_ids = db.Column(db.UnicodeText)

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["date"] = data["date"].strftime("%Y-%m-%d %H:%M")
        return data

