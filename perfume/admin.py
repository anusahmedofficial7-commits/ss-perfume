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
# PERFUME SIZE INLINE
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
        "created_at",
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
        "description",
    )

    list_editable = (
        "stock",
        "featured",
        "best_seller",
        "new_arrival",
    )

    ordering = ("-created_at",)

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
        "city",
        "total_amount",
        "payment_method",
        "payment_status",
        "status",
        "created_at",
    )

    list_filter = (
        "payment_method",
        "payment_status",
        "status",
        "created_at",
    )

    search_fields = (
        "order_number",
        "customer_name",
        "phone",
        "transaction_id",
    )

    list_editable = (
        "payment_status",
        "status",
    )

    readonly_fields = (
        "order_number",
        "created_at",
    )

    ordering = ("-created_at",)


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

    search_fields = (
        "user__username",
        "perfume__name",
    )


# ==========================
# WISHLIST
# ==========================

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "perfume",
        "created_at",
    )

    search_fields = (
        "user__username",
        "perfume__name",
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

    ordering = ("-created_at",)
    