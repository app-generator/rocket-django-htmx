from django.urls import path

from . import views

urlpatterns = [
    path("", views.datatables, name="datatables"),
    path("products-list/", views.products_list, name="products_list"),
    path("add-product/", views.add_product, name="add_product"),
    path('delete-product/<int:id>/', views.delete_product, name="delete_product"),
    path('update-product/<int:id>/', views.update_product, name="update_product"),
]