from flask import render_template, redirect, url_for, request, session, g, abort, flash

from app import category_required, validate_input
from . import recipes
from config import Config

@recipes.route('/recipes', methods=['GET'])
@category_required
def recipes_page():
    return render_template("profile.html", recipes=Config.current_category.recipes, user_name=Config.current_user.name)


@recipes.route('/addrecipe/', methods=['POST'])
@category_required
def add_recipe():
    ingredient = None
    ingredients = []
    ingredient_num = 1
    while 'ingredient{}'.format(ingredient_num) in request.form:
        ingredient = request.form['ingredient{}'.format(ingredient_num)]
        if validate_input(ingredient):
            break
        ingredients.append(ingredient)
        ingredient_num += 1

    #: check if the recipe title is blank
    if request.form['recipetitle'] == "":
        flash("Recipe title cannot be blank!")
        return redirect(url_for('recipes.recipes_page', category_name=Config.current_category.category_name))

    Config.current_category.add_recipe(request.form['recipetitle'], ingredients, request.form['directions'])
    return redirect(url_for('recipes.recipes_page', category_name=Config.current_category.category_name))

@recipes.route('/editrecipe/<string:prev_title>', methods=['POST'])
@category_required
def edit_recipe(prev_title):


    ingredient = None
    ingredients = []
    ingredient_num = 1
    while 'ingredient{}'.format(ingredient_num) in request.form:
        ingredient = request.form['ingredient{}'.format(ingredient_num)]
        ingredients.append(ingredient)
        ingredient_num += 1

    Config.current_category.edit_recipe(prev_title, request.form['recipetitle'], ingredients, request.form['directions'])
    return redirect(url_for('recipes.recipes_page', category_name=Config.current_category.category_name))

@recipes.route('/deleterecipe/<string:recipe_title>')
@category_required
def delete_recipe(recipe_title):
    Config.current_category.delete_recipe(recipe_title)
    return redirect(url_for('recipes.recipes_page', category_name=Config.current_category.category_name))