from django.test import TestCase

from account.forms import AccountLoginForm, AccountRegisterForm
from account.models import Account


class AccountFormTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create_user(email='testuser1@mail.com', username='testuser1', password='12345')

    def test_account_register_form_valid(self):
        form = AccountRegisterForm(data={
            'email': 'user_from_form@mail.com',
            'username': 'user_from_form',
            'password1': 'sfglkmfskjfsg',
            'password2': 'sfglkmfskjfsg',
        })
        self.assertTrue(form.is_valid())

    def test_account_register_form_without_username(self):
        form = AccountRegisterForm(data={
            'email': 'user_from_form@mail.com',
            'password1': 'sfglkmfskjfsg',
            'password2': 'sfglkmfskjfsg',
        })
        self.assertFalse(form.is_valid())

    def test_account_login_form_using_username(self):
        form = AccountLoginForm(data={
            'username': 'testuser1',
            'password': '12345',
        })
        self.assertTrue(form.is_valid())

    def test_account_login_form_using_email(self):
        form = AccountLoginForm(data={
            'username': 'testuser1@mail.com',
            'password': '12345',
        })
        self.assertTrue(form.is_valid())
