from app import app, mysql
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_cors import CORS
import re


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")


# error handling
@app.errorhandler(404)
def page_not_found(e):
    return render_template("/error-pages/404.html"), 404


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
