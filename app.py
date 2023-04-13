from flask import Flask
from flask_bcrypt import Bcrypt
from wtforms import Form, StringField, PasswordField, validators
from datetime import timedelta


from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    make_response,
)
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    set_access_cookies,
    get_jwt_identity,
    unset_jwt_cookies,
)
import re

import os

from werkzeug.utils import secure_filename

# Create Flask app and configure settings
app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "web"

app.config["JWT_SECRET_KEY"] = "3821b6c598199d34ea47e7fdf4c90122"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_CSRF_METHODS"] = []
#app.config["JWT_CSRF_IN_COOKIES"] = True
#app.config["JWT_ACCESS_CSRF_FIELD_NAME"] = "csrf_access_token"

# Initialize MYSQL, JWT, and Bcrypt
mysql = MySQL(app)
jwt = JWTManager(app)
flask_bcrypt = Bcrypt(app)

# Define registration form class
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

# Define login form class
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


# Define routes and their respective functions

# Home route
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# Login route
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        cur = mysql.connection.cursor()
        username = form.username.data
        password = form.password.data
        cur.execute(
            "SELECT * FROM user WHERE username = %s",
            (username,),
        )
        user = cur.fetchone()
        if user and flask_bcrypt.check_password_hash(user[3], password):
            msg = "Login successful!"
            access_token = create_access_token(identity=username)
            resp = make_response(render_template("login.html", msg=msg, form=form))
            set_access_cookies(resp, access_token)
            return resp
        else:
            msg = "Incorrect login!"
    return render_template("login.html", msg=msg, form=form)

# Register route
@app.route("/register", methods=["GET", "POST"])
def register():
    msg = ""
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        cur = mysql.connection.cursor()
        name = form.name.data
        username = form.username.data
        password = flask_bcrypt.generate_password_hash(form.password.data)
        cur.execute("SELECT * FROM user WHERE username = %s", (username,))
        user = cur.fetchone()
        if user:
            msg = "User already exist!"
        else:
            cur.execute(
                "INSERT INTO user VALUES (NULL, %s, %s, %s, 'default_profile_pic.jpg')",
                (
                    name,
                    username,
                    password,
                ),
            )
            mysql.connection.commit()
            msg = "Register successfully!"
    return render_template("register.html", msg=msg, form=form)

# Logout route
@app.route("/logout")
def logout():
    form = LoginForm(request.form)
    resp = make_response(render_template("login.html", form=form))
    unset_jwt_cookies(resp)
    return resp

# Protected profile route
@app.route("/profile", methods=["GET"])
@jwt_required()
def protected_profile():
    username = get_jwt_identity()
    cur = mysql.connection.cursor()
    cur.execute("SELECT profile_pic FROM user WHERE username = %s", (username,))
    profile_pic = cur.fetchone()
    return render_template("profile.html", username=username, profile_pic = profile_pic[0])

# Upload profile picture route
@app.route("/upload_profile_pic", methods=["POST"])
@jwt_required()
def upload_profile_pic():
    if "profile_pic" in request.files:
        username = get_jwt_identity()
        profile_pic = request.files["profile_pic"]

        # Define allowed file extensions and the maximum file size (in bytes)
        allowed_extensions = {"jpg", "jpeg", "png", "gif"}
        max_file_size = 5 * 1024 * 1024  # 5 MB

        # Validate the uploaded file
        if allowed_file(profile_pic, allowed_extensions, max_file_size):
            filename = secure_filename(profile_pic.filename)

            profile_pics_path = os.path.join(app.root_path, "static/profile_pics")
            profile_pic.save(os.path.join(profile_pics_path, f"{username}.{filename.split('.')[-1]}"))

            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE user SET profile_pic = %s WHERE username = %s",
                (f"{username}.{filename.split('.')[-1]}", username),
            )
            mysql.connection.commit()
            return redirect(url_for("protected_profile"))
        else:
            return "Invalid file.", 400
    else:
        return "No file uploaded.", 400


# error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("/error-pages/404.html"), 404


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return render_template("/error-pages/401.html"), 401

# helper function for checking file extension and size
    
def allowed_file(file, allowed_extensions, max_size):
    # Check if the file has a valid extension
    filename = file.filename
    file_ext = filename.rsplit(".", 1)[1].lower()
    if file_ext not in allowed_extensions:
        return False

    # Check if the file size is within the allowed limit
    file_size = file.content_length
    if file_size > max_size:
        return False

    return True


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
