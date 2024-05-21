from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.utils import save_picture, send_reset_email
from flask_login import current_user, login_required, login_user, logout_user
from flask import flash, url_for, request, redirect, Blueprint, render_template
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm

users = Blueprint('users',__name__)


# REGISTER PAGE ROUTE
@users.route("/register", methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
    
  form = RegistrationForm()
  if form.validate_on_submit():
    hash_pass = bcrypt.generate_password_hash(form.password.data)
    user = User(username=form.username.data,email=form.email.data, password=hash_pass)
    db.session.add(user)
    db.session.commit()
    flash(f'Account created for {form.username.data}!','success')
    return redirect(url_for('users.login'))
    
  return render_template('register.html', title='Register', form=form)


# LOGIN PAGE ROUTE
@users.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
    
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      
      # if any query parameter
      next_page = request.args.get('next')
      return redirect(next_page) if next_page else redirect(url_for('main.home'))
    else:
      flash('Login Unsuccessful. Please check email and password','danger')
  
  return render_template('login.html', title='Login', form=form)


# LOGOUT ROUTE
@users.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('main.home'))


# ACCOUNT ROUTE
@users.route('/account',methods=['GET','POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture = save_picture(form.picture.data)
      current_user.image_file = picture   

    current_user.username = form.username.data
    current_user.email = form.email.data
    db.session.commit()
    flash('your account has been updated!','success')
    return redirect(url_for('users.account')) # post get redirect pattern
  
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.email.data = current_user.email
    
  image_file = url_for('static', filename='profile_pics/'+ current_user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form)


# USER SPECIFIC POSTS
@users.route("/user/<string:username>")
def user_posts(username):
  page = request.args.get('page',1,type=int)
  user = User.query.filter_by(username=username).first_or_404()
  
  posts = Post.query.filter_by(author=user)\
    .order_by(Post.date_posted.desc())\
      .paginate(page=page,per_page=5)
      
  return render_template('user_post.html',posts=posts, user=user, title='User Post')



@users.route('/reset_password',methods=['GET','POST'])
def reset_request():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    # send_reset_email(user)
    # flash('An email has been sent with instruction to reset your password.', 'info')
    # return redirect(url_for('login'))
    token = user.get_reset_token()
    return redirect(url_for('users.reset_token',token=token))
  return render_template('reset_request.html',title='Reset Password', form=form)


@users.route('/reset_password/<token>',methods=['GET','POST'])
def reset_token(token):
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  
  user = User.verify_reset_token(token)
  if user is None:
    flash('That is an invalid or expired token','warning')
    return redirect(url_for('users.reset_request'))
  
  form = ResetPasswordForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data)
    user.password = hashed_password
    db.session.commit()
    flash('Your password has been updated! you are now able to log in', 'info')
    return redirect(url_for('users.login'))
  return render_template('reset_token.html',title='Reset Password', form=form)
  