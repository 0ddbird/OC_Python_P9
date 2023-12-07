from django.contrib import admin
from litrevu.models import Ticket, Review, UserFollows
from django.db.models.expressions import F


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "time_created")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "ticket_display",
        "headline",
        "rating",
        "user",
        "time_created",
    )

    def ticket_display(self, obj):
        return obj.ticket_title

    ticket_display.short_description = "Ticket"

    def get_queryset(self, request):
        qs = super().get_queryset(request).annotate(ticket_title=F("ticket__title"))
        return qs


@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    list_display = ("user", "followed_user")
