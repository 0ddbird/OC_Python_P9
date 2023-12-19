from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserActionForm(forms.Form):
    user_to_act_on = forms.CharField(label="Username", widget=forms.TextInput())
    action = forms.ChoiceField(
        choices=[("follow", "Follow"), ("block", "Block")],
        widget=forms.RadioSelect,
        initial="follow",
    )


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
