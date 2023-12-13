from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from litrevu.models import Review, Ticket


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ("title", "description", "image")


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        model = Review
        fields = ("rating", "headline", "body")


class UserActionForm(forms.Form):
    user_to_act_on = forms.CharField(label="Username", widget=forms.TextInput())
    action = forms.ChoiceField(
        choices=[("follow", "Follow"), ("block", "Block")],
        widget=forms.RadioSelect,
        initial="follow",
    )
