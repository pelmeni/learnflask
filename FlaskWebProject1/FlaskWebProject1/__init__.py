"""
The flask application package.
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
db_posts = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

import FlaskWebProject1.views, models

from .models import *



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))