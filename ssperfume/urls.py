from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from perfume.views import (
    home,
    product_detail,
    add_to_cart,
    cart,
    increase_quantity,
    decrease_quantity,
    remove_from_cart,
    wishlist,
    add_to_wishlist,
    checkout,
    place_order,
    success,
    track_order,
    signup,
    login_view,
    logout_view,
    profile,
    about,   # <-- ADD THIS
)

urlpatterns = [
    # Home
    path("", home, name="home"),

    # Admin
    path("admin/", admin.site.urls),

    # Product
    path("product/<int:id>/", product_detail, name="product_detail"),

    # Cart
    path("cart/", cart, name="cart"),
    path("add-to-cart/<int:id>/", add_to_cart, name="add_to_cart"),
    path("increase/<int:id>/", increase_quantity, name="increase_quantity"),
    path("decrease/<int:id>/", decrease_quantity, name="decrease_quantity"),
    path("remove-cart/<int:id>/", remove_from_cart, name="remove_from_cart"),

    # Wishlist
    path("wishlist/", wishlist, name="wishlist"),
    path("add-to-wishlist/<int:id>/", add_to_wishlist, name="add_to_wishlist"),

    # Checkout
    path("checkout/", checkout, name="checkout"),
    path("place-order/", place_order, name="place_order"),
    path("success/", success, name="success"),

    # Track Order
    path("track-order/", track_order, name="track_order"),

    # About
    path("about/", about, name="about"),

    # Authentication
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/", profile, name="profile"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    