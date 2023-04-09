from app import app, mysql, jwt, flask_bcrypt, RegisterForm, LoginForm
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


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


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
            msg = "Login successfully!"
            access_token = create_access_token(identity=username)
            resp = make_response(render_template("login.html", msg=msg, form=form))
            set_access_cookies(resp, access_token)
            return resp
        else:
            msg = "Incorrect login!"
    return render_template("login.html", msg=msg, form=form)


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
                "INSERT INTO user VALUES (NULL, %s, %s, %s)",
                (
                    name,
                    username,
                    password,
                ),
            )
            mysql.connection.commit()
            msg = "Register successfully!"
    return render_template("register.html", msg=msg, form=form)


@app.route("/logout")
def logout():
    form = LoginForm(request.form)
    resp = make_response(render_template("login.html", form=form))
    unset_jwt_cookies(resp)
    return resp


@app.route("/profile", methods=["GET"])
@jwt_required()
def protected_profile():
    username = get_jwt_identity()
    return render_template("profile.html", username=username)


# error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("/error-pages/404.html"), 404


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return render_template("/error-pages/401.html"), 401


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
