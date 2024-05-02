from flask import Flask, render_template, url_for
app = Flask(__name__)


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

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html',posts=posts,)


@app.route("/about")
def about():
    return render_template('about.html',title='About')
    


# if __name__ == '__main__'::ha:
#     app.run(debug=True)