from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("date", views.index, name="date"),
    path("week", views.weekly, name="week"),
    path("month", views.monthly, name="month"),
    path("year", views.anually, name="year"),
    path("year", views.anually, name="number"),
    path("productos", views.productos, name="productos"),
    path("productos/<str:cat>", views.productos, name="productoCategoria"),
    path("productos/producto/<int:productID>/edit", views.editProduct, name="editProduct"),
    path("productos/producto/<int:productID>", views.getProduct, name="getProduct"),
    path("test", views.test, name="test"),
]