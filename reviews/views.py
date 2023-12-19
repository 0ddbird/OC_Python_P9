from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from reviews.forms import ReviewForm
from reviews.models import Review
from tickets.models import Ticket


def create_review(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.ticket = ticket
            new_review.user = request.user
            new_review.save()
            return redirect("feed")
    else:
        form = ReviewForm()

    return render(request, "edit_review.html", {"form": form, "ticket": ticket})


def update_review(request, ticket_id, review_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("feed")
    else:
        form = ReviewForm(instance=review)

    return render(
        request, "edit_review.html", {"form": form, "ticket": ticket, "review": review}
    )


@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect("feed")
