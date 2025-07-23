from django.urls import path
from . import views


urlpatterns = [
    path("", views.expense_list, name="expense-list-page"),
    path("create/", views.expense_create, name="expense-create-page"),
    path("edit/<int:pk>/", views.expense_edit, name="expense-edit-page"),
    path("delete/<int:pk>/", views.expense_delete, name="expense-delete-page"),
]
