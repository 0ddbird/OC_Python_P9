from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])

    class Meta:
        model = Review
        fields = ("rating", "headline", "body")
