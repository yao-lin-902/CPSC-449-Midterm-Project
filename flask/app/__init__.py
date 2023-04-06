from flask import Flask
from flask_mysqldb import MySQL
from datetime import timedelta

app = Flask(__name__)
app.config["MYSQL_HOST"] = "db"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "web"
app.secret_key = "3821b6c598199d34ea47e7fdf4c90122"
app.permanent_session_lifetime = timedelta(minutes=10)

mysql = MySQL(app)

from app import views
