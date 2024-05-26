from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import DecimalField, RadioField, SelectField, TextAreaField, DateTimeLocalField, DateField, FileField, SubmitField, DateTimeField, IntegerField
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
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired()])
    submit = SubmitField('Log in')

class SignUpForm(FlaskForm):
    lname = StringField('Last Name', validators=[InputRequired()])
    name = StringField('First Name', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired()])
    submit = SubmitField('Sign Up')


class NameForm(FlaskForm):
    name = StringField('Name')
    submit = SubmitField('Yes Name')

class CreateTeamForm(FlaskForm):
    TeamName = StringField('Name your team', validators=[InputRequired()])
    TeamSpeech = TextAreaField('Team speech')
    submit = SubmitField('Make A Team')

class AddTeamMember(FlaskForm):
    emailname = StringField('Email of wanted player', validators=[InputRequired()])
    submit = SubmitField('ADD PLAYER')

class EventForm(FlaskForm):
    eventdate = DateTimeLocalField("Time", validators=[InputRequired()])
    eventname = StringField("Name", validators=[InputRequired()])
    eventdesc = StringField("Description", validators=[InputRequired()])
    submit = SubmitField("Create Event")


