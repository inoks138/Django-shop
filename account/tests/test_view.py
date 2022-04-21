from django.test import TestCase
from django.urls import reverse

from account.models import Account


class AccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create_user(email='testuser1@mail.com', username='testuser1', password='12345')

    def test_register_view_access(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_register_view_invalid(self):
        response = self.client.post(reverse('register'), data={
            'username': 'user_from_form',
            'password1': 'sfglkmfskjfsg',
            'password2': 'sfglkmfskjfsg',
        })
        self.assertFormError(response, 'form', 'email', 'Обязательное поле.')

    def test_register_view_valid(self):
        response = self.client.post(reverse('register'), data={
            'email': 'user_from_form@mail.com',
            'username': 'user_from_form',
            'password1': 'sfglkmfskjfsg',
            'password2': 'sfglkmfskjfsg',
        })
        self.assertRedirects(response, reverse('home'))

    def test_login_view_access(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_login_view_invalid(self):
        response = self.client.post(reverse('login'), data={
            'username': 'testuser1',
            'password': 'invalid_password',
        })
        self.assertFormError(response, 'form', '__all__',
                             'Пожалуйста, введите правильные Email и пароль. '
                             'Оба поля могут быть чувствительны к регистру.')

    def test_login_view_valid(self):
        response = self.client.post(reverse('login'), data={
            'username': 'testuser1',
            'password': '12345',
        })
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
