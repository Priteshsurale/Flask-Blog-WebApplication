from flaskblog.models import Post
from flask import request, Blueprint, render_template


main = Blueprint('main',__name__)


# HOME ROUTE 
@main.route("/")
@main.route("/home")
def home():
  page = request.args.get('page',1,type=int)
  posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page,per_page=5)
  return render_template('home.html',posts=posts, title='Home')


# ABOUT PAGE ROUTE
@main.route("/about")
def about():
    return render_template('about.html',title='About')