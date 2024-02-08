from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = EmailField('Email: ', validators=[DataRequired()])
    password = PasswordField('Password: ', validators=[DataRequired()])
    submit_btn = SubmitField('Login')



class ErgastForm(FlaskForm):
    name_or_id = StringField('Name_or_id: ', validators=[DataRequired()])
    submit_btn = SubmitField('Ergast')


