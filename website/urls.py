from django.urls import path
from . import views

app_name = "website"  # <-- important

urlpatterns = [
    path("about/", views.about, name="about"),
    path("examples/", views.examples_index, name="examples_index"),
    path("examples/<slug:slug>/", views.example_detail, name="example_detail"),
    path("contact/", views.contact_view, name="contact"),  # <-- use contact_view
    path("", views.home, name="home"),
    path("growth/", views.growth, name="growth"),
]
