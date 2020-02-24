from server import db, login
from flask_login import UserMixin


@login.user_loader
def load_admin(admin_id):
    return AdminModel.query.get(int(admin_id))


class AdminModel(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    gov_id = db.Column(db.String(120))
    designation = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Admin('{self.name}', '{self.email}', {self.designation})"