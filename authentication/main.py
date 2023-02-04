import os

from flask import Flask, redirect, render_template, request, session, url_for
from helpers import get_users, hash_password

__winc_id__ = "8fd255f5fe5e40dcb1995184eaa26116"
__human_name__ = "authentication"

app = Flask(__name__)

app.secret_key = os.urandom(16)


@app.route("/home")
def redirect_index():
    return redirect(url_for("index"))


@app.route("/")
def index():
    if 'username' in session:
        message = f'Logged in as {session["username"]}'
    else:
        message = 'You are not logged in'
    return render_template("index.html", title="Index", message = message, session = session)


@app.route("/about")
def about():
    return render_template("about.html", title="About")


@app.route("/lon")
def lon():
    return render_template("lon.html", title="League of Nations")


@app.route("/login", methods=["GET", "POST"])
def login():
    args = request.args
    args = args.to_dict()
    er_query = args.get("error")
    if er_query:
        error_m = 'Invalid username/password'
    else:
        error_m = ' '
    
    if request.method == "POST":
        user = request.form['username']
        given_pw = request.form['password']
        if user in get_users():
            if hash_password(given_pw) == get_users()[user]:
                session['username'] = user
                session['logged_in'] = True
                return redirect(url_for('dashboard'))    
            else:
                return redirect(url_for('login', error=True))
        else:
            return redirect(url_for('login', error=True))
    elif request.method == "GET":
        if 'logged_in' in session:
            return render_template("al_login.html", title= "Allready logged in")
        else:
            return render_template("login.html", title= "Login", error = error_m)

    


@app.route("/dashboard")
def dashboard():
    user = session['username']
    age = 0
    try:
        age = get_users()[user].age
    except:
        pass
    data={'username': user, 'age':  age}
    return render_template("dashboard.html", data = data)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    return redirect(url_for('index'))
