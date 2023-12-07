from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from litrevu.forms import FollowUserForm, RegistrationForm, ReviewForm, TicketForm

from litrevu.models import Ticket, Review, UserFollows


def home(request):
    return render(request, "home.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect("feed")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


@login_required
def feed(request):
    # Users followed by current user
    following_users = UserFollows.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )

    # Followed users tickets + User tickets
    tickets = (
        Ticket.objects.filter(user__in=following_users)
        .union(Ticket.objects.filter(user=request.user))
        .order_by("-time_created")
    )

    # Reviews to user tickets
    my_ticket_ids = Ticket.objects.filter(user=request.user).values_list(
        "id", flat=True
    )

    reviews_for_my_tickets = Review.objects.filter(ticket__in=my_ticket_ids).order_by(
        "-time_created"
    )

    # Reviews by user and followed users
    reviews = (
        Review.objects.filter(user__in=following_users)
        .union(Review.objects.filter(user=request.user))
        .order_by("-time_created")
    )

    context = {
        "tickets": tickets,
        "reviews": reviews,
        "reviews_for_my_tickets": reviews_for_my_tickets,
    }
    return render(request, "feed.html", context)


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

    return render(request, "create_ticket.html", {"form": form})


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

    return render(request, "create_review.html", {"form": form, "ticket": ticket})


@login_required
def follow_view(request):
    if request.method == "POST":
        form = FollowUserForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["user_to_follow"]
            try:
                followed_user = get_user_model().objects.get(username=username)
                UserFollows.objects.get_or_create(
                    user=request.user, followed_user=followed_user
                )
            except get_user_model().DoesNotExist:
                # Gérer le cas où l'utilisateur n'existe pas
                pass
            return redirect("subscriptions")
    else:
        form = FollowUserForm()

    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)

    return render(
        request,
        "follow_view.html",
        {"form": form, "following": following, "followers": followers},
    )


@login_required
def unfollow_view(request, user_id):
    try:
        followed_user = get_user_model().objects.get(pk=user_id)
        UserFollows.objects.filter(
            user=request.user, followed_user=followed_user
        ).delete()
    except get_user_model().DoesNotExist:
        pass
    return redirect("subscriptions")
