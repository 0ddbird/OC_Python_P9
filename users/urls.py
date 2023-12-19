from django.urls import path

from users.views import social_view, unblock_view, unfollow_view

urlpatterns = [
    path("subscriptions/", social_view, name="subscriptions"),
    path("unfollow/<int:user_id>/", unfollow_view, name="unfollow_view"),
    path("unblock/<int:user_id>/", unblock_view, name="unblock_view"),
]
