from flask_admin.contrib.sqla import ModelView
from server import db

class Buyer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"Buyer('{self.username}', '{self.email}')"

class BuyerView(ModelView):
    can_create = False