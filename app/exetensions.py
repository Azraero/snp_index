from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
