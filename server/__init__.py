from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_bcrypt import Bcrypt

app  = Flask(__name__)
app.config['SECRET_KEY'] = 'f0ede16f635dfdc68bb71dfeee0e59'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)
admin = Admin(app)
current_user = current_user

# login.login_view = 'log_in'

from server import routes