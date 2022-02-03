from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from requirement.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exist !')

    def validate_email(self, email_to_check):
        user = User.query.filter_by(email=email_to_check.data).first()
        if user:
            raise ValidationError('Email already exist !')

    username = StringField(label='', validators=[Length(min=2, max=30), DataRequired()])
    password1 = PasswordField(label='', validators=[Length(min=4), DataRequired()])
    password2 = PasswordField(label='', validators=[EqualTo('password1'), DataRequired()])
    email = StringField(label='', validators=[Email(), DataRequired()])
    submit = SubmitField(label='ثبت ')


class LoginForm(FlaskForm):
    username = StringField(label='', validators=[DataRequired()])
    password = PasswordField(label='', validators=[DataRequired()])
    submit = SubmitField(label='ورود')
