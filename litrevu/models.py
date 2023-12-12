from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Ticket(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="following",
    )
    followed_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="followed_by",
    )

    class Meta:
        unique_together = (
            "user",
            "followed_user",
        )
        verbose_name = "User Follows"
        verbose_name_plural = "User Follows"


class UserBlocked(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="blocking",
    )
    blocked_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="blocked_by",
    )

    class Meta:
        unique_together = (
            "user",
            "blocked_user",
        )
        verbose_name = "User blocks"
        verbose_name_plural = "User Blocks"
