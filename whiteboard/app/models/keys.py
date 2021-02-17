from app import db
from flask_sqlalchemy import inspect


class Key(db.Model):
    __tablename__ = "keys"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    key = db.Column(db.String(56), unique=True)

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        return data

