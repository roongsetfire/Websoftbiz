from django.urls import path
from . import views

app_name = "m35"

urlpatterns = [
    path("", views.m35, name="m35"),
    # path("get_items_by_r_c_no/", views.get_items_by_r_c_no, name="get_items_by_r_c_no"),
    # path("update_textstamp/", views.update_textstamp, name="update_textstamp"),
]