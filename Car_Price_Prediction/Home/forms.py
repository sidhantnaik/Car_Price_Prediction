from django import forms
# from django.contrib.auth.forms import UserCreationForm, AthenticationForm
# from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "w-full px-4 p-4 rounded-xl"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "w-full px-3 p-4 rounded-xl"}
        )
    )


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ( "username", "email", "password1", "password2") 

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "w-full px-4 p-4 rounded-xl"}
        )
    )

    email = forms.EmailField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Email", "class": "w-full px-3 p-4 rounded-xl"}
        )
    )

    phone = forms.IntegerField(
        max_value=12,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Mobile", "class": "w-full px-3 p-4 rounded-xl"}
        )
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "w-full px-3 p-4 rounded-xl"}
        )
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "class": "w-full px-3 p-4 rounded-xl",
            }
        )
    )
