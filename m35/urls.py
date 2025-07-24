from django.urls import path
from . import views

app_name = "m35"

urlpatterns = [
    path("", views.m35, name="m35"),

]