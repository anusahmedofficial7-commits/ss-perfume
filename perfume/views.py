from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
import random

from .models import (
    Perfume,
    PerfumeSize,
    Cart,
    Wishlist,
    Order,
    Review,
)


# ==========================
# HOME
# ==========================

def home(request):

    query = request.GET.get("q", "")

    perfumes = Perfume.objects.all()

    if query:
        perfumes = perfumes.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )

    featured = perfumes.filter(featured=True)
    best_sellers = perfumes.filter(best_seller=True)
    new_arrivals = perfumes.filter(new_arrival=True)

    cart_count = 0
    wishlist_count = 0

    if request.user.is_authenticated:
        cart_count = Cart.objects.filter(user=request.user).count()
        wishlist_count = Wishlist.objects.filter(user=request.user).count()

    context = {
        "perfumes": perfumes,
        "featured": featured,
        "best_sellers": best_sellers,
        "new_arrivals": new_arrivals,
        "query": query,
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    }

    return render(request, "home.html", context)


# ==========================
# PRODUCT DETAIL
# ==========================

def product_detail(request, id):

    perfume = get_object_or_404(
        Perfume,
        id=id
    )

    if request.method == "POST":

        if not request.user.is_authenticated:
            return redirect("login")

        Review.objects.create(
            user=request.user,
            perfume=perfume,
            rating=request.POST.get("rating"),
            comment=request.POST.get("comment"),
        )

        messages.success(
            request,
            "Review submitted successfully."
        )

        return redirect(
            "product_detail",
            id=id
        )

    sizes = perfume.sizes.all()

    reviews = Review.objects.filter(
        perfume=perfume
    ).order_by("-created_at")

    related_products = Perfume.objects.filter(
        category=perfume.category
    ).exclude(
        id=perfume.id
    )[:4]

    return render(
        request,
        "product_detail.html",
        {
            "perfume": perfume,
            "sizes": sizes,
            "reviews": reviews,
            "related_products": related_products,
        },
    )
    # ==========================
# ADD TO CART
# ==========================

@login_required
def add_to_cart(request, id):

    perfume = get_object_or_404(Perfume, id=id)

    size = request.POST.get("size")

    if not size:
        messages.error(request, "Please select a perfume size.")
        return redirect("product_detail", id=id)

    perfume_size = get_object_or_404(
        PerfumeSize,
        perfume=perfume,
        size=size
    )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        perfume=perfume,
        size=size,
        defaults={
            "price": perfume_size.discount_price
            if perfume_size.discount_price
            else perfume_size.price
        }
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, "Product added to cart successfully.")

    return redirect("cart")


# ==========================
# CART
# ==========================

@login_required
def cart(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        item.subtotal = item.price * item.quantity
        total += item.subtotal

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total,
        }
    )


# ==========================
# INCREASE QUANTITY
# ==========================

@login_required
def increase_quantity(request, id):

    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect("cart")


# ==========================
# DECREASE QUANTITY
# ==========================

@login_required
def decrease_quantity(request, id):

    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")


# ==========================
# REMOVE FROM CART
# ==========================

@login_required
def remove_from_cart(request, id):

    item = get_object_or_404(
        Cart,
        id=id,
        user=request.user
    )

    item.delete()

    messages.success(
        request,
        "Item removed from cart."
    )

    return redirect("cart")


# ==========================
# WISHLIST
# ==========================

@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        "wishlist.html",
        {
            "wishlist_items": wishlist_items
        }
    )


# ==========================
# ADD TO WISHLIST
# ==========================

@login_required
def add_to_wishlist(request, id):

    perfume = get_object_or_404(
        Perfume,
        id=id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        perfume=perfume
    )

    messages.success(
        request,
        "Added to wishlist successfully."
    )

    return redirect("wishlist")
    # ==========================
# CHECKOUT
# ==========================

@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("home")

    total = 0

    for item in cart_items:
        item.subtotal = item.price * item.quantity
        total += item.subtotal

    context = {
        "cart_items": cart_items,
        "total": total,

        # Client apni details yahan change karega
        "bank_name": "Allied Bank Limited",
        "account_title": "YOUR ACCOUNT TITLE",
        "account_number": "0000-0000000000",
        "iban": "PK00ABCD0000000000000000",
        "jazzcash": "03XX-XXXXXXX",
        "easypaisa": "03XX-XXXXXXX",
    }

    return render(request, "checkout.html", context)


# ==========================
# PLACE ORDER
# ==========================

@login_required
def place_order(request):

    if request.method != "POST":
        return redirect("checkout")

    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect("home")

    total = sum(item.price * item.quantity for item in cart_items)

    payment_method = request.POST.get("payment_method")
    transaction_id = request.POST.get("transaction_id")

    order_number = "ORD" + str(random.randint(100000, 999999))

    while Order.objects.filter(order_number=order_number).exists():
        order_number = "ORD" + str(random.randint(100000, 999999))

    payment_status = "Pending"

    if payment_method == "COD":
        payment_status = "Pending"
    else:
        payment_status = "Paid" if transaction_id else "Pending"

    Order.objects.create(
        user=request.user,
        customer_name=request.POST.get("name"),
        phone=request.POST.get("phone"),
        address=request.POST.get("address"),
        city=request.POST.get("city"),
        total_amount=total,
        order_number=order_number,

        payment_method=payment_method,
        transaction_id=transaction_id,
        payment_status=payment_status,

        status="Pending",
        notes=request.POST.get("notes"),
    )

    cart_items.delete()

    messages.success(
        request,
        f"Your order has been placed successfully. Order Number: {order_number}"
    )

    return redirect("success")


# ==========================
# SUCCESS
# ==========================

@login_required
def success(request):
    return render(request, "success.html")
    # ==========================
# TRACK ORDER
# ==========================

def track_order(request):

    order = None

    if request.method == "POST":

        order_number = request.POST.get("order_number")

        order = Order.objects.filter(
            order_number=order_number
        ).first()

        if order is None:
            messages.error(
                request,
                "Order not found."
            )

    return render(
        request,
        "track_order.html",
        {
            "order": order
        }
    )


# ==========================
# SIGNUP
# ==========================

def signup(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("signup")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(request, "signup.html")


# ==========================
# LOGIN
# ==========================

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            messages.success(
                request,
                f"Welcome {user.username}"
            )

            return redirect("home")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "login.html")


# ==========================
# LOGOUT
# ==========================

@login_required
def logout_view(request):

    logout(request)

    messages.success(
        request,
        "Logged out successfully."
    )

    return redirect("home")


# ==========================
# PROFILE
# ==========================

@login_required
def profile(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    total_orders = orders.count()

    return render(
        request,
        "profile.html",
        {
            "orders": orders,
            "total_orders": total_orders,
        }
    )


# ==========================
# ABOUT
# ==========================

def about(request):
    return render(request, "about.html")
    