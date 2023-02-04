from flask import Flask, render_template, redirect, url_for

__winc_id__ = "9263bbfddbeb4a0397de231a1e33240a"
__human_name__ = "templates"

app = Flask(__name__)


@app.route("/")
def index():
    text= {'h1' : 'Home, Sweet Home' , 'p' : 'This is rendered through a template'}
    return render_template('index.html', title = 'Index', data = text )

@app.route("/home")
def home():
    return redirect(url_for("index"))

@app.route("/about")
def about():
    text= {'h1' : 'Home, Sweet Home' , 'p' : 'This is rendered through a template'}
    return render_template('about.html', title = 'About', data = text )

@app.route("/user")
def user():
    text= {'h1' : 'User Page' , 'p' : 'This is rendered through a template'}
    return render_template('base.html', title = 'User', data = text )


if __name__ == '__main__':
    app.run(debug = True, port = 5000) #debug = True, port = 5000
