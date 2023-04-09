from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from wtforms import Form, StringField, PasswordField, validators
from datetime import timedelta

app = Flask(__name__)
app.config["MYSQL_HOST"] = "db"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "web"
app.config["JWT_SECRET_KEY"] = "3821b6c598199d34ea47e7fdf4c90122"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]

mysql = MySQL(app)
jwt = JWTManager(app)
flask_bcrypt = Bcrypt(app)


class RegisterForm(Form):
    name = StringField(
        "Name",
        [
            validators.DataRequired(),
            validators.Length(min=1, max=30),
            validators.Regexp("^[a-zA-Z ]*$", message="Name must contain letters only"),
        ],
    )
    username = StringField(
        "Username",
        [
            validators.DataRequired(),
            validators.Length(min=6, max=30),
            validators.Regexp(
                "^\w+$",
                message="Username must contain only letters, numbers, or underscore",
            ),
        ],
    )
    password = PasswordField(
        "Password",
        [
            validators.DataRequired(),
            validators.Length(min=6, max=25),
        ],
    )


class LoginForm(Form):
    username = StringField(
        "Username",
        [
            validators.DataRequired(),
            validators.Length(min=6, max=30),
            validators.Regexp(
                "^\w+$",
                message="Username must contain only letters, numbers, or underscore",
            ),
        ],
    )
    password = PasswordField(
        "Password", [validators.DataRequired(), validators.Length(min=6, max=25)]
    )


from app import views
