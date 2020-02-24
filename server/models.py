from server import db, app, login, admin, current_user
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView


class Scheme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    details = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'details': self.details
        }

    def __repr__(self):
        return f"Scheme('{self.name}')"


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated