from flask_wtf import FlaskForm
from wtforms import fields, validators, ValidationError
from .models import AdminUser


class LoginForm(FlaskForm):
    email = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])
    remember_me = fields.BooleanField('Remember Me')
    submit = fields.SubmitField('Sign In')

    def validate(self):
        return True

    def get_user(self):
        return AdminUser.query.filter_by(email=self.email.data).first()
