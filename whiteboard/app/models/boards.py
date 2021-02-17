from app import db
from flask_sqlalchemy import inspect


class Board(db.Model):
    __tablename__ = "boards"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))
    is_active = db.Column(db.Boolean, default=False)
    task_id = db.Column(db.Integer)

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        return data

