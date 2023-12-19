from django.urls import path

from tickets.views import create_ticket, create_ticket_and_review

urlpatterns = [
    path("create_ticket/", create_ticket, name="create_ticket"),
    path(
        "create_ticket_and_review/",
        create_ticket_and_review,
        name="create_ticket_and_review",
    ),
]
