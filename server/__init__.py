from flask import Flask, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f0ede16f635dfdc68bb71dfeee0e59'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['API_KEY'] = ''
app.config['API_SECRET_KEY'] = ''

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login = LoginManager(app)

current_user = current_user

from server.buyer.routes import buyer_routes
from server.crops.routes import crops_routes
from server.farmers.routes import farmers_routes
from server.messages.routes import message_routes
from server.admin import routes

app.register_blueprint(buyer_routes)
app.register_blueprint(crops_routes)
app.register_blueprint(crops_routes)
app.register_blueprint(message_routes)

# login.login_view = 'log_in'
