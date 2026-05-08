from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("product/<int:id>/", views.product_detail, name="product_detail"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart_view, name="cart"),
    path("increase/<int:item_id>/", views.increase_quantity, name="increase_quantity"),
    path("decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
]