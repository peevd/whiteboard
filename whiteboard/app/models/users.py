from app import db
from flask_sqlalchemy import inspect


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    picture = db.Column(db.UnicodeText)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    facebook = db.Column(db.String(120))
    google = db.Column(db.String(120))

    child_participants = db.relationship("Participant",
                                         cascade="save-update", backref="users")
    child_events = db.relationship("Event",
                                   cascade="save-update", backref="users")

    child_answers = db.relationship("StudentAnswer",
                                    cascade="save-update", backref="users")

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        return data

    def toDictPublic(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        del data["email"]
        del data["facebook"]
        del data["google"]
        return data

