from django import forms


class LoginForm(forms.Form):
    email_id = forms.CharField()
    password = forms.CharField()