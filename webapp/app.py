import os
from flask import Flask, render_template, redirect, url_for, request, session, g, abort, flash

#config
SECRET_KEY = 'development mode'

app = Flask(__name__, static_folder='../designs/UI', template_folder='../designs/UI')
app.config.from_object(__name__)

class Category:
    """ A class of categories, which takes category's name as the first argument.
    This class also keeps track of recipes that will be for this particular class.
    The instance of this class will have the ability to do the following:
        1. Add a recipe through add_recipe method which takes the title of the recipe, ingredients, and directions as its argument.
        2. Edit a recipe by using edit_recipe method which takes the previous title, the new title, ingredients, and directions as arguments.
        3. Delete a recipe by using delete_recipe method that takes the recipe's title that needs to be deleted as its argument
        4. Edit current category by changing its name to a new name.
    """

    def __init__(self, category_name):
        self.category_name = category_name
        self.recipes = {}

    def add_recipe(self, title, ingredients, directions):
        self.recipes[title] = Recipe(title, ingredients, directions)

    def edit_recipe(self, prev_title, title, ingredients, directions):
        self.recipes.pop(prev_title)
        self.recipes[title] = Recipe(title, ingredients, directions)

    def delete_recipe(self, recipe_title):
        self.recipes.pop(recipe_title)

    def edit_category(self, category_name):
        self.category_name = category_name


class Recipe:
    """This is a class that will represent a recipe.
    It takes a title for the recipe, it's ingredients and directions as arguments.
    """
    def __init__(self, title, ingredients, directions):
        self.title = title
        self.ingredients = ingredients
        self.directions = directions

class User:
    """This class will represent a user.
    It takes the user's name, his email, his password, and details as arguments.
    It also keeps track of categories of the user, so each user will have his/her own list of categories
    The class has the following methods:
        1. is_valid(password): which takes a password as an argument and returns True is the password provided matches the users password
        2. add_category(category_name): It adds a category, and takes category's name as the argument
        3. delete_category(category_name): It deletes a category whose name is provided as an arg
        4. edit_category(prev_name, new_name): This renames 'prev_category' with a new name provided as the 2nd arg
            (this also calls the edit_category method presented in Category class)
        5. return_category(category_name): It returns an instance of the Class Category, given that category's name
    """
    def __init__(self, name, email, password, details):
        self.name = name
        self.email = email
        self.password = password
        self.details = details
        self.categories = {}

    def is_valid(self, password):
        return self.password == password

    def add_category(self, category_name):
        self.categories[category_name] = Category(category_name)

    def delete_category(self, category_name):
        self.categories.pop(category_name)

    def edit_category(self, prev_name, new_name):

        self.categories[prev_name].edit_category(new_name)
        self.categories[new_name] = self.categories.pop(prev_name)

    def return_category(self, category_name):
        return self.categories[category_name]

"""These are global variables that keep track of:
    1. registered users
    2. the user which is currently logged in
    3. The category which a user is at currently
"""
users = {}
current_user = None
current_category = None


@app.route('/')
@app.route('/index.html/')
def index():
    """This function takes a user to index.html page (homepage) which diplays a registration form and a link to login page."""
    return render_template("index.html")

@app.route('/login.html/')
def login_page():
    """function renders a template for logging in"""
    return render_template("login.html")

@app.route('/profile.html/')
def profile(ingredients = None):
    """This function takes a user to his homepage after he has logged in,
    where he will see his/her categories and will be add in new categories.
    """
    global current_user
    if current_user == None:
        return redirect(url_for('login_page'))

    return redirect(url_for('categories'))

@app.route('/register/', methods=['POST'])
def register():
    """This function is there to register a user"""
    global users
    error = None

    # check if the password and ver password are not the same
    if request.form['password'] != request.form['verpassword']:
        error = 'Password does not match the password in verify password field'
        return render_template('index.html', error=error)

    users[request.form['name']] = User(request.form['name'], request.form['email'], request.form['password'], request.form['details'])
    return redirect(url_for('login_page'))

@app.route('/validate/', methods=['POST'])
def validate():
    """This function validates the login credentials entered by a user in login form"""
    global users
    global current_user
    error = None
    #: if the user has registered before
    if request.form['name'] in users:
        #: then also check if his password matches the password provided
        if users[request.form['name']].is_valid(request.form['password']):
            current_user = users[request.form['name']]
            return redirect(url_for('profile'))

    flash("Incorrect Credentials Entered")
    return redirect(url_for('login_page'))

@app.route('/categories.html/', methods=['GET'])
def categories():
    return render_template("categories.html", categories=current_user.categories, user_name=current_user.name)

@app.route('/addcategory/', methods=['POST'])
def add_category():
    current_user.add_category(request.form['category_name'])
    return redirect(url_for('categories'))

@app.route('/editcategory/<string:prev_name>', methods=['POST'])
def edit_category_name(prev_name):
    current_user.edit_category(prev_name, request.form['category_name'])
    return redirect(url_for('categories'))


@app.route('/deletecategory')
def delete_category():
    category = current_user.delete_category(request.args['category_name'])
    return redirect(url_for('categories'))


@app.route('/recipes', methods=['GET'])
def recipes():
    global current_category
    if not current_category:
        current_category = current_user.return_category(request.args['category_name'])
    return render_template("profile.html", recipes=current_category.recipes, user_name=current_user.name)


@app.route('/addrecipe/', methods=['POST'])
def add_recipe():
    global current_category

    ingredient = None
    ingredients = []
    ingredient_num = 1
    while 'ingredient{}'.format(ingredient_num) in request.form:
        ingredient = request.form['ingredient{}'.format(ingredient_num)]
        ingredients.append(ingredient)
        ingredient_num += 1

    current_category.add_recipe(request.form['recipetitle'], ingredients, request.form['directions'])
    return redirect(url_for('recipes', category_name=current_category.category_name))

@app.route('/editrecipe/<string:prev_title>', methods=['POST'])
def edit_recipe(prev_title):
    global current_category

    ingredient = None
    ingredients = []
    ingredient_num = 1
    while 'ingredient{}'.format(ingredient_num) in request.form:
        ingredient = request.form['ingredient{}'.format(ingredient_num)]
        ingredients.append(ingredient)
        ingredient_num += 1

    current_category.edit_recipe(prev_title, request.form['recipetitle'], ingredients, request.form['directions'])
    return redirect(url_for('recipes', category_name=current_category.category_name))

@app.route('/deleterecipe/<string:recipe_title>')
def delete_recipe(recipe_title):
    current_category.delete_recipe(recipe_title)
    return redirect(url_for('recipes', category_name=current_category.category_name))

@app.route('/logout/')
def logout():
    global current_user
    current_user = None
    return redirect(url_for('login_page'))

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run('', port=port)
