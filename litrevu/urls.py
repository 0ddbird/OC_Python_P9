from django.urls import path

from litrevu.views import feed, landing_page

urlpatterns = [
    path("", landing_page, name="landing_page"),
    path("feed/", feed, name="feed"),
]
