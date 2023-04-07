from app import app, mysql, jwt
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
    cur = mysql.connection.cursor()
    msg = ""
    if (
        request.method == "POST"
        and "username" in request.form
        and "password" in request.form
    ):
        username = request.form["username"]
        password = request.form["password"]
        cur.execute(
            "SELECT * FROM user WHERE username = %s AND password = %s",
            (username, password),
        )
        user = cur.fetchone()
        if user:
            msg = "Login successfully!"
            access_token = create_access_token(identity=username)
            resp = make_response(render_template("login.html", msg=msg))
            set_access_cookies(resp, access_token)
            return resp
        else:
            msg = "Incorrect login!"
    return render_template("login.html", msg=msg)


@app.route("/register", methods=["GET", "POST"])
def register():
    cur = mysql.connection.cursor()
    msg = ""
    if (
        request.method == "POST"
        and "name" in request.form
        and "username" in request.form
        and "password" in request.form
    ):
        name = request.form["name"]
        username = request.form["username"]
        password = request.form["password"]
        cur.execute(
            "SELECT * FROM user WHERE username = %s", (request.form["username"],)
        )
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
    return render_template("register.html", msg=msg)


@app.route("/logout")
def logout():
    resp = make_response(render_template("login.html"))
    unset_jwt_cookies(resp)
    resp.set_cookie("access_token", "", expires=0)
    return resp


@app.route("/profile", methods=["GET"])
@jwt_required()
def protected_profile():
    username = get_jwt_identity()
    print(username)
    return render_template("profile.html")


# error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("/error-pages/404.html"), 404


@jwt.unauthorized_loader
def unauthorized_response(callback):
    return render_template("/error-pages/401.html"), 401


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
