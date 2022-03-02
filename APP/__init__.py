from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from flask_login import LoginManager

# creating and initialising flask app
app = Flask(__name__)

# adding configurations frm a config class
app.config.from_object(Config)

# hooking the database to the flask app
db = SQLAlchemy(app=app)

# initialisation of the Login manager and hooking it up to the flask app
login_manager = LoginManager(app)

# setting the defualt login page
login_manager.login_view = "admin_login_page"

# session timed out message
login_manager.needs_refresh_message=(u"Session Timed out, Please re-login")

# setting session message category
login_manager.needs_refresh_message_category="danger"

from APP import views, models
