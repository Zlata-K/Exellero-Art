import csv
import bcrypt
from flask import Flask, render_template, redirect, url_for, session, flash, request
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import Email, InputRequired

from forms import ContactForm, ContactForm2, LoginForm, RegisterForm

app = Flask(__name__)
app.secret_key = 'anoriginalkey'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.config['USE_SESSION_FOR_NEXT'] = True


class User(UserMixin):
    def __init__(self, username, email, phone, password=None):
        self.id = username
        self.email = email
        self.phone = phone
        self.password = password


@login_manager.user_loader
def load_user(user_id):
    user = find_user(user_id)
    if user:
        user.password = None
    return user


def find_user(username):
    with open('data/users.csv') as f:
        for user in csv.reader(f):
            if username == user[0]:
                return User(*user)
    return None


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = find_user(form.username.data)
        if user and bcrypt.checkpw(form.password.data.encode(), user.password.encode()):
            login_user(user)
            flash('Logged in successfully.')
            next_page = session.get('next', '/')
            session['next'] = '/'
            return redirect(next_page)
        else:
            flash('Incorrect username/password!')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # flash(str(session))
    return redirect('/')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = find_user(form.username.data)
        if not user:
            salt = bcrypt.gensalt()
            password = bcrypt.hashpw(form.password.data.encode(), salt)
            with open('data/users.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([form.username.data, form.email.data, form.phone.data, password.decode()])
            flash('Registered successfully.')
            return redirect('/login')
        else:
            flash('This username already exists, choose another one')
    return render_template('register.html', form=form)


@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html')


@app.route('/non_protected')
def non_protected():
    return render_template('non_protected.html')


@app.route('/')
def fun():
    return render_template("exellero_home.html")


@app.route('/home')
def home():
    return render_template("exellero_home.html")


@app.route('/about')
def about():
    return render_template("exellero_about.html")


@app.route('/gallery')
def gallery():
    return render_template("exellero_gallery.html")


@app.route('/tutorials', methods=['GET', 'POST'])
def tuts():
    form = ContactForm2()
    if form.validate_on_submit():
        with open('data/tutorials.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([form.name.data, form.message.data])
        return redirect(url_for('response_tut', name=form.name.data))
    return render_template("exellero_tutorials.html", form=form)


@app.route('/response_tut/<name>')
def response_tut(name):
    return render_template('response_tut.html', name=name)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        with open('data/messages.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([form.name.data, form.email.data, form.message.data])
        return redirect(url_for('response', name=form.name.data))
    return render_template("exellero_contact.html", form=form)


@app.route('/response/<name>')
def response(name):
    return render_template('response.html', name=name)


@app.route('/gallery_2017')
def gal_17():
    return render_template("gallery_2017.html")


@app.route('/gallery_2018')
def gal_18():
    return render_template("gallery_2018.html")


@app.route('/gallery_2019')
def gal_19():
    return render_template("gallery_2019.html")


@app.route('/gallery_inc_2017')
def gal_inc_17():
    return render_template("gallery_inc_2017.html")


@app.route('/gallery_inc_2018')
def gal_inc_18():
    return render_template("gallery_inc_2018.html")


@app.route('/gallery_inc_2019')
def gal_inc_19():
    return render_template("gallery_inc_2019.html")


@app.route('/login_page')
def login_page():
    return render_template("login_page.html")


if __name__ == '__main__':
    app.run()
