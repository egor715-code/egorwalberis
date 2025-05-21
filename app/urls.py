from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<str:product_slug>", views.product_detail, name="product_detail"),

    # Маршруты для корзины
    path("cart/add/<str:product_slug>", views.cart_add, name="cart_add"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/remove/<int:item_id>", views.cart_remove, name="cart_remove"),
]