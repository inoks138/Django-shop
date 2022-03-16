from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from account.models import Account


class AccountLoginForm(AuthenticationForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2',)


class AccountRegisterForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2',)
