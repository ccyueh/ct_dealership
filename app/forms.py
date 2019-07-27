from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField, TextAreaField, BooleanField, DateTimeField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Optional
from flask import flash
from app.models import User
import datetime

class LoginForm(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-type Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            flash('Sorry but those credentials are already in use.')
            raise ValidationError('Username already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            flash('Sorry but those credentials are already in use.')
            raise ValidationError('E-mail already taken.')

class CustomerForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    submit = SubmitField('Display Cars')

class MaintenanceForm(FlaskForm):
    car_id = IntegerField('Car ID', validators=[DataRequired()])
    maintenance_desc = TextAreaField('Description', validators=[DataRequired()])
    staff_id = IntegerField('Staff ID', validators=[DataRequired()])
    date_started = DateTimeField('Date Started', validators=[DataRequired()], default=datetime.datetime.now())
    date_finished = DateTimeField('Date Finished', validators=[Optional()], default=None)
    submit = SubmitField('Submit Record')
