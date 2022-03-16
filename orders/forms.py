from django import forms
from .models import Order
from phonenumber_field.modelfields import PhoneNumberField


class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "control"}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "control"}))
    patronymic = forms.CharField(widget=forms.TextInput(attrs={"class": "control"}))
    phone = PhoneNumberField()
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "control"}))

    address = forms.CharField(widget=forms.TextInput(attrs={"class": "control"}))
    postal_code = forms.CharField(widget=forms.TextInput(attrs={"class": "control"}))

    paid = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "control"}))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'patronymic', 'phone', 'city', 'address', 'postal_code', 'paid']
