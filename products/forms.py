from django import forms
from django.contrib.auth.models import User


class AddProductForm(forms.Form):
    title = forms.CharField(max_length=255)
    price = forms.IntegerField()
    description = forms.CharField(max_length=255)



class RegisterForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Такая почта уже существует")
        return email


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())