from django import forms


class AddProductForm(forms.Form):
    title = forms.CharField(max_length=255)
    price = forms.IntegerField()
    description = forms.CharField(max_length=255)



class RegisterForm(forms.Form):
    name = forms.CharField(max_length=255)
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, widget=forms.PasswordInput())