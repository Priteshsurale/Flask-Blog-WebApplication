import os 
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
from flask_login import LoginManager # mange user session
from flask_sqlalchemy import SQLAlchemy
load_dotenv()

app = Flask(__name__)

# secret key protect against modifying cookies and cross site request forgery(csrf) attacks.
app.config['SECRET_KEY'] = '0b134aeac20f8b7faa9b88a2087030f5' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app) # we add some functionality to database models and then it will handle all of the session in the background
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['ACCOUNT_EMAIL_VERIFICATION'] = 'none'

app.config['MAIL_USERNAME'] = os.environ.get('GMAIL_ID')
app.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PASS')
# print(os.environ.get('GMAIL_ID'),os.environ.get('GMAIL_PASS'))
mail = Mail(app)

from flaskblog import routes 