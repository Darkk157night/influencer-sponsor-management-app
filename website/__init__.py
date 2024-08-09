from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] ='0c2ecc9bfef6ef11f629e261'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///website.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
from website import routes
