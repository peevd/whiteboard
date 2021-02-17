from app import db
from flask_sqlalchemy import inspect


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)

    child_users = db.relationship("User",
                                  cascade="save-update", backref="roles")

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        return data

