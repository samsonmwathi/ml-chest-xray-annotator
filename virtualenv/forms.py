from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,SubmitField,EmailField,PasswordField,FileField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms import validators

class SignupForm(FlaskForm):
    first_name = StringField('first name',[DataRequired()])
    last_name = StringField('last name',[DataRequired()]) 
    email = EmailField('Email',[DataRequired()])
    password = PasswordField('password',[Length(min=5,message=('password too short')),EqualTo('confirm_password', 'Password mismatch'),DataRequired()])
    confirm_password = PasswordField('confirm_password',[Length(min=5,message=('password too short')),DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')

class LoginForm(FlaskForm):
    email = EmailField('Email',[DataRequired()])
    password = PasswordField('password',[Length(min=5,message=('password too short')),DataRequired()])
    recaptcha = RecaptchaField()
    submit = SubmitField('submit')
