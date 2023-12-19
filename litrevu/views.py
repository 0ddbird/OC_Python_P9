from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Exists, F, OuterRef, Q, Subquery, Value
from django.db.models.functions import Concat
from django.shortcuts import render

from config import settings
from reviews.models import Review
from tickets.models import Ticket
from users.models import UserFollows

ID = int


def landing_page(request):
    return render(request, "landing_page.html")


@login_required
def feed(request):
    followed_user_ids = UserFollows.objects.filter(user=request.user).values_list(
        "followed_user", flat=True
    )

    # Tickets from current user or followed users
    tickets = Ticket.objects.filter(
        Q(user_id__in=Subquery(followed_user_ids)) | Q(user=request.user)
    ).annotate(
        content_type=Value("TICKET", CharField()),
        username=F("user__username"),
        has_review=Exists(Review.objects.filter(ticket_id=OuterRef("id"))),
    )

    user_tickets_subquery = Ticket.objects.filter(user=request.user).values_list(
        "id", flat=True
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

    # Reviews by followed users or by followers
    reviews = Review.objects.filter(
        Q(user_id__in=Subquery(followed_user_ids))
        | Q(
            ticket_id__in=Subquery(user_tickets_subquery)
        )  # 2e sous condition : pas de review d'utilisateurs bloqués
    ).annotate(
        content_type=Value("REVIEW", CharField()),
        ticket_title=F("ticket__title"),
        ticket_username=F("ticket__user__username"),
        review_username=F("user__username"),
        is_editable=Value(False),
    )

    posts = sorted(
        chain(reviews, tickets, user_reviews),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(request, "feed.html", context={"posts": posts})
