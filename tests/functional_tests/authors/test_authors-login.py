from .base import AuthorsBaseTest
import pytest
from django.contrib.auth.models import User
from selenium.webdriver.common.by import By
from django.urls import reverse

@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):
        string_pass = 'pass'
        user = User.objects.create_user(username='my_user', password=string_pass)

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')
        username_field = self.get_by_placeholder(form, 'Type your username')
        password_field = self.get_by_placeholder(form, 'Type your password')

        username_field.send_keys(user.username)
        password_field.send_keys(string_pass)

        form.submit()

        self.assertIn(
            f'Your are logged in with {user.username}.', 
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url + reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def teste_form_login_is_valid(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys(' ')
        password.send_keys(' ')

        form.submit()

        self.assertIn(
            'Invalid username or password',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )


    def teste_form_login_invalid_credentials(self):
        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username = self.get_by_placeholder(form, 'Type your username')
        password = self.get_by_placeholder(form, 'Type your password')

        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        form.submit()

        self.assertIn(
            'Invalid credentials',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
