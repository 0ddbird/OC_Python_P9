from django.contrib.auth.models import User
from django.db import models


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
