import os
import unittest
from urllib.parse import urlparse

from app import *

class appTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def register(self, name, email, password, details):
        """the sole purpose of this function is to register a user and
            take us to the page where the user will be redirected to after registering
        """
        return self.app.post('/register/', data=dict(
            name = name,
            email = email,
            password = password,
            verpassword = password,
            details = details
            ), follow_redirects=True)

    def login(self, name, password):
        """This function should be called after calling register function,
            its purpose is to login a user and redirect us to the appropriate page
        """
        return self.app.post('/validate/', data=dict(
            name = name,
            password = password
            ), follow_redirects=True)

    def add_category(self):
        """This function should be called after calling login function,
            this one adds a category for the user
        """
        response = self.app.post('/addcategory/', data=dict(
            category_name = 'Healthy Recipes'
            ), follow_redirects=True)
        return response

    def add_recipe(self):
        """This function should be called after calling add_category function,
            It first takes you to the appropriate recipe's page,
            in our case; recipes that lie under Healthy Recipes category
            and adds in a recipe with the following values:
                recipe's title = Testing recipe title
                first ingredient = Testing ingredients
                directions = Testing directions
            And returns a response which should include a recipe with the above values
        """
        self.app.get('/recipes', query_string={'category_name': 'Healthy Recipes'})

        response = self.app.post('/addrecipe/', data=dict(
            recipetitle = 'Testing recipe title',
            ingredient1 = 'Testing ingredients',
            directions = 'Testing directions'
            ), follow_redirects=True)

        return response

    def delete_recipe(self):
        """This function should be called after calling add_recipe function,
            it deletes a recipe, in our case it deletes a recipe added through add_recipe function,
            and should return recipes page without any recipes
        """
        response = self.app.get('/deleterecipe/Testing%20recipe%20title', follow_redirects=True)
        return response


    # Ensure the Homepage loads correctly
    def test_index(self):
        response = self.app.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensure there is text on home page saying 'Login' (Because its a registration page, and has a link to a login page)
    def test_index_text(self):
        response = self.app.get('/', content_type='html/text')
        self.assertTrue(b'Login' in response.data)

    # Ensure that the user registration behaves correctly
    def test_registration(self):
        response = self.register('admin', 'admin@gmail.com', 'default', 'A user for testing purposes')
        self.assertIn(b'Sign in!!!', response.data)

    # Ensure the app behaves correctly given the correct credentials
    def test_login_crct_credentials(self):
        self.register('admin', 'admin@gmail.com', 'default', 'A user for testing purposes')
        response = self.login('admin', 'default')
        self.assertIn (b'Welcome admin', response.data)

    #Ensure that users can add in new categories
    def test_add_recipe(self):
        self.register('admin', 'admin@gmail.com', 'default', 'A user for testing purposes')
        self.login('admin', 'default')
        response = self.add_recipe()
        self.assertIn(b'Healthy Recipes', response.data)

    #Ensure that users can add in new recipes
    def test_add_recipe(self):

        self.register('admin', 'admin@gmail.com', 'default', 'A user for testing purposes')
        self.login('admin', 'default')
        self.add_category()

        response = self.add_recipe()

        self.assertIn(b'Testing', response.data)

    # Ensure thats users can delete a recipe
    def test_delete_recipe(self):
        self.register('admin', 'admin@gmail.com', 'default', 'A user for testing purposes')
        self.login('admin', 'default')
        self.add_category()

        #: Store the url which a user gets after adding a recipe,
        #: So that we can check if the user gets redirected to the same url after he deletes a recipe
        response_after_adding_recipe = self.add_recipe()
        url_after_adding_recipe = urlparse(response_after_adding_recipe.location).path

        #: delete a recipe
        response = self.delete_recipe()

        #: check if after deleting a recipe, the user gets redirected to the correct url
        self.assertEqual(urlparse(response.location).path, url_after_adding_recipe)

        #: Check to see if the recipe still exists
        self.assertNotIn(b'Testing', response.data)

if __name__ == '__main__':
    unittest.main()