from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Exists, F, OuterRef, Q, Subquery, Value
from django.db.models.functions import Concat
from django.shortcuts import render

from config import settings
from reviews.models import Review
from tickets.models import Ticket
from users.models import UserBlocked, UserFollows

ID = int


def landing_page(request):
    return render(request, "landing_page.html")


@login_required
def feed(request):
    followed_user_ids = UserFollows.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )

    user_tickets_subquery = Ticket.objects.filter(user=request.user).values_list(
        "id", flat=True
    )

    user_tickets = Ticket.objects.filter(
        id__in=Subquery(user_tickets_subquery)
    ).annotate(
        content_type=Value("TICKET", CharField()),
        username=F("user__username"),
        has_review=Exists(Review.objects.filter(ticket_id=OuterRef("id"))),
        is_editable=Value(True),
    )

    # Tickets from current user or followed users
    followed_users_tickets = Ticket.objects.filter(
        user_id__in=Subquery(followed_user_ids)
    ).annotate(
        content_type=Value("TICKET", CharField()),
        username=F("user__username"),
        has_review=Exists(Review.objects.filter(ticket_id=OuterRef("id"))),
        is_editable=Value(False),
    )

    # Reviews by current user
    user_reviews = Review.objects.filter(user=request.user).annotate(
        content_type=Value("USER_REVIEW", CharField()),
        ticket_title=F("ticket__title"),
        ticket_description=F("ticket__description"),
        ticket_username=F("ticket__user__username"),
        ticket_image_url=Concat(
            Value(settings.MEDIA_URL), F("ticket__image"), output_field=CharField()
        ),
        ticket_time_created=F("ticket__time_created"),
        review_username=F("user__username"),
        is_editable=Value(True),
    )

    blocked_users_subquery = UserBlocked.objects.filter(user=request.user).values_list(
        "blocked_user_id", flat=True
    )

    # Reviews by followed users or by followers
    reviews = (
        Review.objects.filter(
            Q(user_id__in=Subquery(followed_user_ids))
            | Q(ticket_id__in=Subquery(user_tickets_subquery))
        )
        .exclude(user_id__in=Subquery(blocked_users_subquery))
        .annotate(
            content_type=Value("REVIEW", CharField()),
            ticket_title=F("ticket__title"),
            ticket_username=F("ticket__user__username"),
            review_username=F("user__username"),
            is_editable=Value(False),
        )
    )

    posts = sorted(
        chain(reviews, user_tickets, followed_users_tickets, user_reviews),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(request, "feed.html", context={"posts": posts})
