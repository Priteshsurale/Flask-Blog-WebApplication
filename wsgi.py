from flaskblog import create_app

app = create_app()

# code runner
if __name__ == '__main__':
    app.run(debug=False)
