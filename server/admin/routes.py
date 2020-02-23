from server import app, db, current_user, bcrypt
from server.models import AdminModel, MyModelView, Farmer, Crop, Buyer, Message, Scheme
from flask_login import login_user, logout_user, login_required, current_user
from server.admin.forms import RegistrationForm, LoginForm, AlertForm, BuyerRegistrationForm, SchemeForm
from flask import render_template, redirect, request, url_for
from flask_admin import BaseView, expose
import nexmo
from flask_admin.menu import MenuLink
from server.static.utils import save_picture
from flask_admin import Admin
admin = Admin(app)


admin.add_view(MyModelView(AdminModel, db.session))
admin.add_view(MyModelView(Farmer, db.session))
admin.add_view(MyModelView(Buyer, db.session))
admin.add_view(MyModelView(Scheme, db.session))
admin.add_link(MenuLink("Site", endpoint="signin.index"))


class RegisterationView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            admin = AdminModel(
                name = form.name.data,
                email = form.email.data,
                designation = form.designation.data,
                password = hashed_password,
                gov_id = save_picture(form.gov_id.data)
            )
            db.session.add(admin)
            db.session.commit()
        return self.render('admin/register.html', form=form)
    def is_accessible(self):
        return current_user.is_authenticated
admin.add_view(RegisterationView(name='Register', endpoint='register'))

class LoginView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            admin = AdminModel.query.filter_by(name=form.name.data).first()
            if admin and bcrypt.check_password_hash(admin.password, form.password.data):
                login_user(admin, remember=form.remember.data)
                return redirect(url_for('home'))
        return self.render('admin/login.html', form=form)
    def is_accessible(self):
        return not current_user.is_authenticated
admin.add_view(LoginView(name='Login', endpoint='signin'))

class AlertView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        form = AlertForm()
        if form.validate_on_submit():
            client = nexmo.Client(key=app.config['API_KEY'], secret=app.config['API_SECRET_KEY'])
            client.send_message({
                'from': 'Nexmo',
                'to': '918920278726',
                'text': 'Alert',
            })
        return self.render('admin/alert.html', form=form)
    def is_accessible(self):
        return current_user.is_authenticated
admin.add_view(AlertView(name='Alert', endpoint='alert'))

class LogoutView(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def index(self):
        logout_user()
        return redirect(url_for('admin.index'))
    def is_accessible(self):
        return current_user.is_authenticated
admin.add_view(LogoutView(name='Log Out', endpoint='log_out'))

@app.route('/delete_scheme/<int:scheme_id>', methods=['GET', 'POST'])
@login_required
def delete_scheme(scheme_id):
    scheme = Scheme.query.get(scheme_id)
    db.session.delete(scheme)
    db.session.commit()
    return redirect(url_for('schemes_test'))

@app.route('/')
def home():
    return redirect(url_for('admin.index'))