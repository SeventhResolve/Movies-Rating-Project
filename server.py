"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users"""

    # users = db.session.query(User)
    users = User.query.all()

    # print users[0].email

    return render_template("user_list.html", users=users)


@app.route("/login")
def login_form():
    """Show login form"""

    return render_template("login.html")

############## need to test method
@app.route("/login_returning_user")
def check_login():
    """ Check credentials, return to login page if creds do not match"""
    
    username = request.args.get("username")
    password = request.args.get("password")

    return render_template("login.html")

@app.route("/add_new_user", methods=["POST"])
def add_user():
    """Add new user (email and password) to database"""

    username = request.form.get("username")
    password = request.form.get("password")
    print username
    print password

    new_user = User(email=username,
                    password=password)

    print new_user
    db.session.add(new_user)
    db.session.commit()
    
    return render_template("login.html")



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
