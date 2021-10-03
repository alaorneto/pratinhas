from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, max_length=50)
    email = forms.EmailField(required=True, max_length=75)
    password = forms.CharField(required=True)
