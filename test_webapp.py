import unittest

from flask import url_for
from flask_testing import TestCase

from app import create_app
from app.models import User
from config import Config

class TestBase(TestCase):

    def create_app(self):

        config_name = 'testing'
        app = create_app(config_name)

        return app

    def setUp(self):
        """
        Will be called before every test
        """
        #: create a test user
        Config.users['Harith'] = User('Harith', 'harithjaved@gmail.com', 'abc123', "I am a Tester")


    def tearDown(self):
        """
        Will be called after every test
        """
        Config.users = {}

class authentication(TestBase):
    """
    Tests for registration and login when provided appropriate credentials,
    and also when provided incorrect credentials
    """
    def test_validation_incorrect_credentials(self):
        """
        Test that when login form is provided with incorrect credentials,
        it redirects to login page with a flash msg
        """
        response = self.client.post(url_for('auth.validate'), data=dict(
            name = 'incorrect',
            password = 'incorrect'
            ), follow_redirects=True)

        self.assertIn(b'Incorrect Credentials Entered', response.data)

    def test_validation_correct_credentials(self):
        """
        Test that when login form is provided with correct credentials,
        it redirects to profile page
        """
        response = self.client.post(url_for('auth.validate'), data=dict(
            name = 'Harith',
            password = 'abc123'
            ))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, url_for('categories.profile'))

    def test_registration(self):
        """
        Test that a user can register successfully
        """
        response = self.client.post(url_for('auth.register'), data=dict(
            name = 'regTest',
            email = 'reg@test.com',
            password = 'testing',
            verpassword = 'testing',
            details = 'testing'
            ), follow_redirects=True)

        self.assertIn('regTest', Config.users)

class TestViews(TestBase):

    def test_index_view(self):
        """
        Test that registration page is accessible without login
        """
        response = self.client.get(url_for('auth.index'))
        self.assertEqual(response.status_code, 200)

    def test_login_view(self):
        """
        Test that login page is accessible without login
        """
        response = self.client.get(url_for('auth.login_page'))
        self.assertEqual(response.status_code, 200)


    def test_profile(self):
        """
        Test that user profile is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('categories.profile')
        redirect_url = url_for('auth.login_page')

        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_categories_page(self):
        """
        Test that categories page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('categories.categories_page')
        redirect_url = url_for('auth.login_page')

        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

    def test_recipes_page(self):
        """
        Test that recipes page is inaccessible without login
        and redirects to login page
        """
        target_url = url_for('recipes.recipes_page')
        redirect_url = url_for('auth.login_page')

        response = self.client.get(target_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, redirect_url)

if __name__ == '__main__':
    unitest.main()