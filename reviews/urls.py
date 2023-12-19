from django.urls import path

from reviews.views import create_review, delete_review, update_review

urlpatterns = [
    path("reviews/create/<int:ticket_id>/", create_review, name="create_review"),
    path(
        "reviews/update/<int:ticket_id>/<int:review_id>/",
        update_review,
        name="update_review",
    ),
    path("reviews/delete/<int:review_id>/", delete_review, name="delete_review"),
]
