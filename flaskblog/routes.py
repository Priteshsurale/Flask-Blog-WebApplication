from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flaskblog.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required 

posts = [
    {
      'author': 'Pritesh Surale',
      'title': 'Blog Post 1',
      'content': 'First post content',
      'date_posted': 'April 30,2024' 
    },
    {
      'author': 'Sahil Kanchankar', 
      'title': 'Blog Post 2',
      'content': 'Second post content',
      'date_posted': 'April 29,2024' 
    },
    {
      'author': 'Arjun Thakur',
      'title': 'Blog Post 3',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Vedant Somalkar',
      'title': 'Blog Post 4',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Prasad Bhalero',
      'title': 'Blog Post 5',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Govinda Patidar',
      'title': 'Blog Post 6',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Akansha Kumari',
      'title': 'Blog Post 7',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    },
    {
      'author': 'Vipin Mahala',
      'title': 'Blog Post 8',
      'content': 'Third post content',
      'date_posted': 'April 28,2024' 
    }
]


# home route 
@app.route("/")
@app.route("/home")
def home():
  if current_user.is_authenticated:
    return render_template('home.html',posts=posts, title='Home')
  else:
    flash('Please log in to access this page.','info')
    return redirect(url_for('login'))
  
# about page route
@app.route("/about")
def about():
    return render_template('about.html',title='About')


# register page route
@app.route("/register", methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
    
  form = RegistrationForm()
  if form.validate_on_submit():
    hash_pass = bcrypt.generate_password_hash(form.password.data)
    user = User(username=form.username.data,email=form.email.data, password=hash_pass)
    db.session.add(user)
    db.session.commit()
    
    flash(f'Account created for {form.username.data}!','success')
    return redirect(url_for('login'))
    
  return render_template('register.html', title='Register', form=form)


# login page route
@app.route("/login", methods=['GET','POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
    
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      
      return redirect(next_page) if next_page else redirect(url_for('home'))
    else:
      flash('Login Unsuccessful. Please check email and password','danger')
  return render_template('login.html', title='Login', form=form)


# logout route
@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('home'))

# account route
@app.route('/account')
@login_required
def account():
  return render_template('account.html', title='Account')