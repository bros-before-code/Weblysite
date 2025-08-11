from django.urls import path
from . import views

app_name = "website"  # <-- important
urlpatterns = [
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("", views.home, name="home"),          # if you have a home view
    path("growth/", views.growth, name="growth"),
]
