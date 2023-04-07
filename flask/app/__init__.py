from flask import Flask
from flask_mysqldb import MySQL
from flask_jwt_extended import JWTManager
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

from app import views
