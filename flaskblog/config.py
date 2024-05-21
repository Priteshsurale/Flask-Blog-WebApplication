import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY                  = os.environ.get('SECRET_KEY') # secret key protect against modifying cookies and cross site request forgery(csrf) attacks.
    MAIL_PORT                   = 465
    MAIL_SERVER                 = 'smtp.gmail.com'
    MAIL_USE_TLS                = False
    MAIL_USE_SSL                = True
    MAIL_USERNAME               = os.environ.get('GMAIL_ID')
    MAIL_PASSWORD               = os.environ.get('GMAIL_PASS')
    ACCOUNT_EMAIL_VERIFICATION  = 'none'
    SQLALCHEMY_DATABASE_URI     = os.environ.get('SQLALCHEMY_DATABASE_URI')