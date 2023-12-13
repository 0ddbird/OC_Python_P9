from itertools import chain

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import CharField, F, Q, Subquery, Value
from django.shortcuts import get_object_or_404, redirect, render

from litrevu.forms import (
    RegistrationForm,
    ReviewForm,
    TicketForm,
    UserActionForm
)
from litrevu.models import Review, Ticket, UserBlocked, UserFollows


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
            messages.error(request, "Passwords do not match")
    else:
        form = RegistrationForm()

    return render(request, "registration/register.html", {"form": form})


ID = int


@login_required
def feed(request):
    followed_user_ids = UserFollows.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )

    tickets = Ticket.objects.filter(
        Q(user_id__in=Subquery(followed_user_ids)) | Q(user=request.user)
    ).annotate(
        content_type=Value("TICKET", CharField()), ticket_username=F("user__username")
    )

    user_tickets_subquery = Ticket.objects.filter(user=request.user).values_list(
        "id", flat=True
    )

    reviews = Review.objects.filter(
        Q(user_id__in=Subquery(followed_user_ids))
        | Q(user=request.user)
        | Q(ticket_id__in=Subquery(user_tickets_subquery))
    ).annotate(
        content_type=Value("REVIEW", CharField()),
        ticket_title=F("ticket__title"),
        ticket_username=F("ticket__user__username"),
        review_username=F("user__username"),
    )

    posts = sorted(
        chain(reviews, tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(request, "feed.html", context={"posts": posts})


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
def social_view(request):
    if request.method == "POST":
        current_user = request.user
        form = UserActionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data["action"]
            target_username = form.cleaned_data["user_to_act_on"]
            target_user = User.objects.filter(username=target_username).first()

            if target_user:
                if action == "follow":
                    user_is_blocking = UserBlocked.objects.filter(
                        user=current_user, blocked_user=target_user
                    ).exists()
                    user_is_blocked = UserBlocked.objects.filter(
                        user=target_user, blocked_user=current_user
                    ).exists()

                    if user_is_blocked:
                        messages.error(
                            request, "Sorry but you have been blocked by this user!"
                        )
                    elif user_is_blocking:
                        messages.error(
                            request,
                            "You need to unblock this user first!",
                        )
                    else:
                        UserFollows.objects.get_or_create(
                            user=current_user, followed_user=target_user
                        )
                        messages.success(request, "User added successfully.")

                elif action == "block":
                    UserBlocked.objects.get_or_create(
                        user=request.user, blocked_user=target_user
                    )
                    UserFollows.objects.filter(
                        Q(user=current_user, followed_user=target_user)
                        | Q(user=target_user, followed_user=current_user)
                    ).delete()
                    messages.success(request, "User blocked successfully.")
            else:
                messages.error(request, "User not found")
            return redirect("subscriptions")
    else:
        form = UserActionForm()

    following = UserFollows.objects.filter(user=request.user)
    followers = UserFollows.objects.filter(followed_user=request.user)
    blocked = UserBlocked.objects.filter(user=request.user)
    return render(
        request,
        "follow_view.html",
        {
            "form": form,
            "following": following,
            "followers": followers,
            "blocked": blocked,
        },
    )


@login_required
def unfollow_view(request, user_id):
    followed_user = User.objects.filter(pk=user_id).first()
    if followed_user:
        followed_user = User.objects.get(pk=user_id)
        UserFollows.objects.filter(
            user=request.user, followed_user=followed_user
        ).delete()

    return redirect("subscriptions")


@login_required
def unblock_view(request, user_id):
    blocked_user = User.objects.filter(pk=user_id).first()
    if blocked_user:
        UserBlocked.objects.filter(
            user=request.user, blocked_user=blocked_user
        ).delete()

    return redirect("subscriptions")
