from django.urls import path
from litrevu import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("feed/", views.feed, name="feed"),
    path("create_ticket/", views.create_ticket, name="create_ticket"),
    path(
        "create_ticket_and_review/",
        views.create_ticket_and_review,
        name="create_ticket_and_review",
    ),
    path("create_review/<int:ticket_id>/", views.create_review, name="create_review"),
    path("subscriptions/", views.follow_view, name="subscriptions"),
    path("unfollow/<int:user_id>/", views.unfollow_view, name="unfollow_view"),
]
