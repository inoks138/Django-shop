from django.test import TestCase

from account.models import Account


class AccountModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Account.objects.create_user(email='testuser1@mail.com', username='testuser1', password='12345')

    def test_account_str_method(self):
        user = Account.objects.get(pk=1)
        self.assertEqual(str(user), 'testuser1')

    def test_account_manager_create_superuser(self):
        superuser = Account.objects.create_superuser(email='superuser1@mail.com', username='superuser1',
                                                     password='12345')
        self.assertTrue(superuser.is_staff)

    def test_account_manager_create_user_with_no_email(self):
        with self.assertRaises(ValueError) as context:
            Account.objects.create_superuser(email='', username='user', password='12345')

        self.assertTrue('Users must have an email address' in str(context.exception))

    def test_account_manager_create_user_with_no_username(self):
        with self.assertRaises(ValueError) as context:
            Account.objects.create_superuser(email='user@mail.com', username='', password='12345')

        self.assertTrue('Users must have a username' in str(context.exception))
