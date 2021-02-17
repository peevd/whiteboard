from app import db
from flask_sqlalchemy import inspect


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    payment_id = db.Column(db.String(100))
    user_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["date"] = data["date"].strftime("%Y-%m-%d %H:%M")
        return data

