from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import redirect, render

from users.forms import RegistrationForm, UserActionForm
from users.models import UserBlocked, UserFollows


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
                    elif target_user == current_user:
                        messages.error(
                            request,
                            "You cannot follow yourself!",
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
