from flask import flash
from flask_wtf import FlaskForm
from .models import AdminTable
from wtforms import EmailField, PasswordField, StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError


class AdminLoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])


class NewAdminForm(FlaskForm):

    # method checks if username entered is a valid entry in the database
    def validate_username(self, username_to_check):
        username = AdminTable.query.filter_by(username=username_to_check.data).first()
        if username:
            raise ValidationError("Username already exists")

    # method checks if email entered is a valid entry in the database
    def validate_email(self, email_to_check):
        email = AdminTable.query.filter_by(email=email_to_check.data).first()
        if email:
            raise ValidationError("email already exists")

    name = StringField(label="First Name", validators=[DataRequired()])
    surname = StringField(label="SurName", validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    username = StringField(label="username", validators=[DataRequired(), Length(max=32)])
    password = PasswordField(label="Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(label="Confirm Password", validators=[EqualTo("password")])


class UserPostsForm(FlaskForm):
    post_category = SelectField(label="Post Category",
                                choices=[("Complaints", "Complaints"), ("Suggestions", "Suggestions")])
    text = TextAreaField(label="Post's Content", validators=[DataRequired()])
    email = StringField(label="Email")


# User defined method to check if there are errors in forms filled by users
def check_errors(form):
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'there was an error with creating new adding: {err_msg}', category="danger")
