from app import db
from flask_sqlalchemy import inspect
from . utils import add_course_image_url


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.Text())
    is_active = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    price = db.Column(db.Float)
    date = db.Column(db.DateTime)

    child_task = db.relationship("Task", cascade="all,delete", backref="courses")

    child_groups = db.relationship("Group", cascade="all,delete", backref="courses")

    child_approval_requests = db.relationship("CourseApprovalRequest",
                                              cascade="all,delete", backref="courses")

    child_events = db.relationship("Event",
                                   cascade="all,delete", backref="courses")

    child_participants = db.relationship("Participant",
                                         cascade="all,delete", backref="courses")

    owner = db.relationship("User")

    def toDict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        data["owner"] = self.owner.first_name + " " + self.owner.last_name
        data["date"] = data["date"].strftime("%Y-%m-%d %H:%M")
        data["picture"] = add_course_image_url(data["id"])
        return data

