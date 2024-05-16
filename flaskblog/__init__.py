from flask import Flask
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from flaskblog.config import Config
from flask_login import LoginManager # mange user session
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
login_manager = LoginManager() # we add some functionality to database models and then it will handle all of the session in the background
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# CREATING APP WITH CONFIGURATION
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
     
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    from flaskblog.main.routes import main
    from flaskblog.posts.routes import posts
    from flaskblog.users.routes import users
    from flaskblog.errors.handlers import errors
    
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app