from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('growth/', views.growth, name='growth'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]

