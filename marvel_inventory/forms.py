from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserSignupForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    display_name = StringField('Display Name', validators=[DataRequired()])
    first_name = StringField('First Name')
    last_name = StringField('Last Name')
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

class UserSigninForm(FlaskForm):
    login = StringField('Login', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit_button = SubmitField()

# We will also want a class for the api requests so the user can search for a character or comic
class SearchCharactersForm(FlaskForm):
    charname = StringField('charname', validators=[DataRequired()])
    submit_button = SubmitField()