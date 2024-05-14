import jwt
from datetime import datetime,timedelta
from flask_login import UserMixin
from flaskblog import db, login_manager, app

# this keeps the current user object loaded in the current session based on the store id
@login_manager.user_loader
def user_loader(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
  password = db.Column(db.String(60), nullable=False)
  posts = db.relationship('Post', backref='author', lazy=True)
  
  def get_reset_token(self, expires_min=30):
    payload = {'user_id': self.id, 'exp':datetime.now() + timedelta(minutes=expires_min)}
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
  
  @staticmethod
  def verify_reset_token(token):
    try:
      payload = jwt.decode(token,app.config['SECRET_KEY'], algorithms=['HS256'])
      user_id = payload.get('user_id')
      print('user_id:',user_id)
    except:
      return None
    return User.query.get(user_id)
  
  def __repr__(self):
    return f"User('{self.username}','{self.email}','{self.image_file}')"
  
  
class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100), unique=True, nullable=False)
  date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
  content = db.Column(db.Text, nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  
  def __repr__(self):
    return f"Post('{self.title}','{self.date_posted}')"

# stateful protocol stores everything in backend
# stateless protocol stores everything in client side