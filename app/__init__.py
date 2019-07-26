from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

# initialize config variables for application
app.config.from_object(Config)

# Bootstrap requires app instance; always comes after app is declared
bootstrap = Bootstrap(app)

# app variables for database usage
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# variables for login
login = LoginManager(app)

# when a page requires someone to login, the application will route them to the correct route
login.login_view = 'login'

from app import routes
