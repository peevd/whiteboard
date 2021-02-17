from app import db
from flask_sqlalchemy import inspect


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    max_members = db.Column(db.Integer)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"))

    child_board = db.relationship("Board",
                                  cascade="all,delete", backref="groups")
    child_events = db.relationship("Event",
                                   cascade="all,delete", backref="groups")
    child_participants = db.relationship("Participant",
                                         cascade="all,delete", backref="groups")
    child_answers = db.relationship("StudentAnswer",
                                    cascade="all,delete", backref="groups")
    child_keys = db.relationship("Key",
                                 cascade="all,delete", backref="groups")

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        return data

