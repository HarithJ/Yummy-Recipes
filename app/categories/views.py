from flask import render_template, redirect, url_for, request, session, g, abort, flash

from . import categories
from config import Config


@categories.route('/profile.html/')
def profile(ingredients = None):
    """This function takes a user to his homepage after he has logged in,
    where he will see his/her categories and will be add in new categories.
    """

    if Config.current_user == None:
        return redirect(url_for('auth.login_page'))

    return redirect(url_for('categories.categories_page'))

@categories.route('/categories.html/', methods=['GET'])
def categories_page():
    return render_template("categories.html", categories=Config.current_user.categories, user_name=Config.current_user.name)

@categories.route('/addcategory/', methods=['POST'])
def add_category():

    #: check to see if the category name is not blank:
    if request.form['category_name'] == "":
        flash("Category name cannot be blank!")
        return redirect(url_for('categories.categories_page'))

    Config.current_user.add_category(request.form['category_name'])
    return redirect(url_for('categories.categories_page'))

@categories.route('/editcategory/<string:prev_name>', methods=['POST'])
def edit_category_name(prev_name):
    Config.current_user.edit_category(prev_name, request.form['category_name'])
    return redirect(url_for('categories.categories_page'))


@categories.route('/deletecategory')
def delete_category():
    category = Config.current_user.delete_category(request.args['category_name'])
    return redirect(url_for('categories.categories_page'))
