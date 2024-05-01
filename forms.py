from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, FileField, SubmitField, IntegerField
from wtforms.validators import InputRequired
from werkzeug.security import generate_password_hash


class HelpForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Remember me')
    salary = DecimalField('Salary', validators=[InputRequired()])
    gender = RadioField('Gender', choices=[
                        ('male', 'Male'), ('female', 'Female')])
    country = SelectField('Country', choices=[('IN', 'India'), ('US', 'United States'),
                                              ('UK', 'United Kingdom')])
    message = TextAreaField('Message', validators=[InputRequired()])
    photo = FileField('Photo')

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    submit = SubmitField('Log in')

class NameForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Yes Name')
