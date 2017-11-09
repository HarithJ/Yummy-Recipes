from flask import render_template, redirect, url_for, request, session, g, abort, flash

from . import auth
from ..models import User
from config import Config

@auth.route('/')
@auth.route('/index.html/')
def index():
    """This function takes a user to index.html page (homepage) which diplays a registration form and a link to login page."""
    return render_template("index.html")

@auth.route('/login.html/')
def login_page():
    """function renders a template for logging in"""
    return render_template("login.html")

@auth.route('/register/', methods=['POST'])
def register():
    """This function is there to register a user"""
    error = None

    # check if the password and ver password are not the same
    if request.form['password'] != request.form['verpassword']:
        error = 'Password does not match the password in verify password field'
        return render_template('index.html', error=error)

    Config.users[request.form['name']] = User(request.form['name'], request.form['email'], request.form['password'], request.form['details'])
    return redirect(url_for('auth.login_page'))

@auth.route('/validate/', methods=['POST'])
def validate():
    """This function validates the login credentials entered by a user in login form"""

    #: if the user has registered before
    if request.form['name'] in Config.users:
        #: then also check if his password matches the password provided
        if Config.users[request.form['name']].is_valid(request.form['password']):
            Config.current_user = Config.users[request.form['name']]
            return redirect(url_for('categories.profile'))

    #: if incorrect credentials entered then display a flash message to the user
    flash("Incorrect Credentials Entered")
    return redirect(url_for('auth.login_page'))

@auth.route('/logout/')
def logout():
    Config.current_user = None
    return redirect(url_for('auth.login_page'))