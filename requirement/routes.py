from requirement import app
from flask import render_template, redirect, url_for, request, flash, get_flashed_messages
from requirement import db
from requirement.forms import RegisterForm, LoginForm
from requirement.models import User
from flask_login import login_user, logout_user,login_required


@app.route("/", methods=['POST', 'GET'])
@login_required
def index():
    return render_template("index.html")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        login_user(user_to_create)
        flash('نام کاربری شما ثبت و با موفقیت وارد سیستم شدید!')
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('index'))

    if form.errors != {}:
        for err in form.errors.values():
            flash(f'Error : {err}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash("با موفقیت وارد شدید!", category="success")
            return redirect(url_for('index'))
        else:
            flash('نام کاربری و رمز عبور نادرست می باشد', category="danger")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('با موفقیت خارج شدید', category='info')
    return redirect(url_for('login_page'))