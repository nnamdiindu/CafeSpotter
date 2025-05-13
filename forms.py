from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Email


class EditForm(FlaskForm):
    name = StringField("Cafe name", validators=[DataRequired()])
    location = StringField("Location", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired()])
    img_url = StringField("Image URL", validators=[DataRequired()])
    seats = StringField("Number of seats, e.g. 30-40", validators=[DataRequired()])
    toilets = BooleanField("Does it have toilets?")
    wifi = BooleanField("Does it have WiFi?")
    sockets = BooleanField("Does it have sockets?")
    allow_calls = BooleanField("Are calls allowed?")
    coffee_price = StringField("Coffee Price", validators=[DataRequired()])
    submit = SubmitField("Submit")


class RegisterForm(FlaskForm):
    name = StringField("Full name", validators=[DataRequired()])
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")