# from django.urls import path
# from . import views


# urlpatterns = [
#     path("", views.m34, name="m34-page"),
# ]

# urls.py
from django.urls import path
from . import views


urlpatterns = [
    path("", views.m34, name="m34-page"),
    # path("get-record/<int:record_id>/", views.get_record, name="get_record"),
    # path("delete-record/<int:record_id>/", views.delete_record, name="delete_record"),
    # path("bills/create/", views.create_bill, name="create_bill"),
    # path("bills/<int:bill_id>/update/", views.update_bill, name="update_bill"),
    # path("bills/<int:bill_id>/delete/", views.delete_bill, name="delete_bill"),
    # path("bills/<int:bill_id>/", views.get_bill, name="get_bill"),
    # path("bills/search/", views.search_bills, name="search_bills"),
    # path("bills/generate-number/", views.generate_bill_no, name="generate_bill_no"),
]
