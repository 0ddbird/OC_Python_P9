from django.shortcuts import get_object_or_404, redirect, render

from reviews.forms import ReviewForm
from tickets.forms import TicketForm
from tickets.models import Ticket


def create_ticket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect("feed")
    else:
        form = TicketForm()

    return render(request, "edit_ticket.html", {"form": form})


def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()
            return redirect("feed")
    else:
        form = TicketForm()

    return render(request, "edit_ticket.html", {"form": form})


def create_ticket_and_review(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and review_form.is_valid():
            new_ticket = ticket_form.save(commit=False)
            new_ticket.user = request.user
            new_ticket.save()

            new_review = review_form.save(commit=False)
            new_review.ticket = new_ticket
            new_review.user = request.user
            new_review.save()

            return redirect("feed")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()

    return render(
        request,
        "create_ticket_and_review.html",
        {"ticket_form": ticket_form, "review_form": review_form},
    )
