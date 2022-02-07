from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,   SelectField, SelectMultipleField, \
    BooleanField, TextAreaField
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


class ProjectForm(FlaskForm):
    name = StringField(label='', validators=[DataRequired()])
    description = StringField(label='', validators=[DataRequired()])
    submit = SubmitField(label='ذخیره')


class RequirementForm(FlaskForm):
    title = TextAreaField(label='', validators=[DataRequired()])
    level = SelectField(label='سطح نیازمندی', choices=[(1, 'R'), (2, 'S')])
    priority = SelectField(label='اولویت', choices=[(1, 'کلیدی'), (2, 'ضروری'), (3, 'اختیاری')])
    req_type = SelectField(label='نوع نیازمندی', choices=[(1, 'کارکردی'), (2, 'غیرکارکردی')])
    changes = SelectField(label='تغییرات', choices=[(1, 'سیمانی'), (2, 'بسامدی')])
    review = SelectField(label='وضعیت بازبینی', choices=[(1, 'رد'), (2, 'قبول'), (3, 'انتظار')])
    evaluation = SelectField(label='وضعیت ارزیابی', choices=[(1, 'رد'), (2, 'قبول'), (3, 'انتظار'), (4, 'ملاقات شده')])
    evaluation_method = SelectField(label='روش ارزیابی',
                                    choices=[(1, 'آنالیز'), (2, 'شبیه سازی'), (3, 'بازرسی'), (4, 'تست سیستم'),
                                             (5, 'تست کامپوننت')])
    quality_factor = SelectField(label='فاکتور کیفی', choices=[(1, 'AVAILABILITY'), (2, 'FLEXBILITY'), (3, 'INTEGRITY'),
                                                               (4, 'MAINTAINABILITY'), (5, 'PORTABILITY'),
                                                               (6, 'RELIABILITY'), (7, 'SAFETY'), (8, 'SECURITY'),
                                                               (9, 'SUPPORTABILITY'), (10, 'SUSTAINABILITY'),
                                                               (11, 'USABILITY')])
    description = TextAreaField(label='پیوست')
    parent = SelectField(label='والد',coerce=int )
    # project = SelectField(label='پروژه')
    submit = SubmitField(label='ذخیره')


class RequirementFormFilter(FlaskForm):
    check = BooleanField('فیلتر بر اساس  حداقل یک معیار انتخاب شده')
    priority = SelectMultipleField(label='اولویت', choices=[('1', 'کلیدی'), ('2', 'ضروری'), ('3', 'اختیاری')])
    req_type = SelectMultipleField(label='نوع نیازمندی', choices=[('1', 'کارکردی'), ('2', 'غیرکارکردی')])
    changes = SelectMultipleField(label='تغییرات', choices=[('1', 'سیمانی'), ('2', 'بسامدی')])
    review = SelectMultipleField(label='وضعیت بازبینی', choices=[('1', 'رد'), ('2', 'قبول'), ('3', 'انتظار')])
    evaluation = SelectMultipleField(label='وضعیت ارزیابی',
                                     choices=[('1', 'رد'), ('2', 'قبول'), ('3', 'انتظار'), ('4', 'ملاقات شده')])
    evaluation_method = SelectMultipleField(label='روش ارزیابی',
                                            choices=[('1', 'آنالیز'), ('2', 'شبیه سازی'), ('3', 'بازرسی'),
                                                     ('4', 'تست سیستم'),
                                                     ('5', 'تست کامپوننت')])
    quality_factor = SelectMultipleField(label='فاکتور کیفی',
                                         choices=[('1', 'AVAILABILITY'), ('2', 'FLEXBILITY'), ('3', 'INTEGRITY'),
                                                  ('4', 'MAINTAINABILITY'), ('5', 'PORTABILITY'),
                                                  ('6', 'RELIABILITY'), ('7', 'SAFETY'), ('8', 'SECURITY'),
                                                  ('9', 'SUPPORTABILITY'), ('10', 'SUSTAINABILITY'),
                                                  ('11', 'USABILITY')])
    # parent = SelectField(label='والد')
    submit2 = SubmitField(label='جستجو')
