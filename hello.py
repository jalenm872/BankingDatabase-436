from flask import Flask, render_template

#Create a flask instance
app = Flask(__name__, template_folder='templates')

# Create a route decorator
@app.route('/')

# def index():
#     return "<h1>Hello World!</h1>"
#     #return render_template('index.html')


def index():
    return render_template("index.html")

# localhost:5000/user/John
@app.route('/user/<name>')

def user(name):
    return render_template("user.html", user_name=name)

#Create Custom Error Pages

#Invalid URL
@app.errorhandler(404)

def page_not_found(e):
    return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(500)

def page_not_found(e):
    return render_template("500.html"), 500