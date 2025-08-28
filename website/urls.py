from django.urls import path
from . import views

app_name = "website"  # <-- important

urlpatterns = [
    path("about/", views.about, name="about"),
    path("self-starter/", views.self_starter, name="self-starter"),
    path("contact/", views.contact_view, name="contact"),  # <-- use contact_view
    path("", views.home, name="home"),
    path("growth/", views.growth, name="growth"),
]
