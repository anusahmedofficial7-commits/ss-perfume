from django.contrib import admin
from .models import (
    Category,
    Perfume,
    PerfumeSize,
    Cart,
    Wishlist,
    Order,
    Review,
)


# ==========================
# CATEGORY
# ==========================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# ==========================
# PERFUME SIZE
# ==========================

class PerfumeSizeInline(admin.TabularInline):
    model = PerfumeSize
    extra = 1


# ==========================
# PERFUME
# ==========================

@admin.register(Perfume)
class PerfumeAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "brand",
        "category",
        "stock",
        "featured",
        "best_seller",
        "new_arrival",
    )

    list_filter = (
        "category",
        "featured",
        "best_seller",
        "new_arrival",
    )

    search_fields = (
        "name",
        "brand",
    )

    list_editable = (
        "stock",
        "featured",
        "best_seller",
        "new_arrival",
    )

    inlines = [PerfumeSizeInline]


# ==========================
# ORDER
# ==========================

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "order_number",
        "customer_name",
        "phone",
        "total_amount",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "customer_name",
        "phone",
    )

    list_editable = (
        "status",
    )


# ==========================
# CART
# ==========================

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "perfume",
        "size",
        "price",
        "quantity",
    )


# ==========================
# WISHLIST
# ==========================

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "perfume",
    )


# ==========================
# REVIEW
# ==========================

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "perfume",
        "rating",
        "created_at",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    search_fields = (
        "user__username",
        "perfume__name",
    )
    