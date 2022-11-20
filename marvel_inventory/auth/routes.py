from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_inventory.models import User, db
from marvel_inventory.forms import UserSignupForm, UserSigninForm
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder = 'auth_templates')

@auth.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = UserSignupForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            first_name = form.first_name.data
            last_name = form.last_name.data
            display_name = form.display_name.data
            password = form.password.data

            user = User(email, first_name=first_name, last_name=last_name, display_name=display_name, password=password)

            db.session.add(user)
            db.session.commit()
            flash(f"Account successfully created. Please sign in.", "user-created")
            return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid Form Data: Please check your form')
    return render_template('signup.html', form=form)

@auth.route('/sigin', methods = ['GET', 'POST'])
def signin():
    form = UserSigninForm()
    try:
        if request.method == 'POST' and form.validate_on_submit():
            login = form.login.data
            password = form.password.data
            logged_email = User.query.filter(User.email == login).first()
            logged_display = User.query.filter(User.display_name == login).first()
            if logged_email and check_password_hash(logged_email.password, password) or logged_display and check_password_hash(logged_display.password, password):
                print('Welcome')
                if logged_email:
                    login_user(logged_email)
                else:
                    login_user(logged_display)
                flash(f"You have successfully logged in!", 'auth-success')
                return redirect(url_for('site.profile'))
            else:
                flash('Your login and password combination is incorrect. Please try again.', 'auth-failed')
                redirect(url_for('auth.signin'))
    except:
        raise Exception("Invalid form data: Please Try Again")
    return render_template('signin.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))