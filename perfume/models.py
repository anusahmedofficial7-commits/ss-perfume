from django.db import models
from django.contrib.auth.models import User


# ==========================
# CATEGORY
# ==========================

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# ==========================
# PERFUME
# ==========================

class Perfume(models.Model):

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    description = models.TextField()

    image = models.ImageField(upload_to="perfumes/")

    stock = models.PositiveIntegerField(default=0)

    featured = models.BooleanField(default=False)
    best_seller = models.BooleanField(default=False)
    new_arrival = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ==========================
# PERFUME SIZE
# ==========================

class PerfumeSize(models.Model):

    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE,
        related_name="sizes"
    )

    size = models.CharField(max_length=20)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.perfume.name} - {self.size}"


# ==========================
# CART
# ==========================

class Cart(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE
    )

    size = models.CharField(max_length=20)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "perfume", "size")

    def __str__(self):
        return f"{self.user.username} - {self.perfume.name} ({self.size})"
        # ==========================
# ORDER
# ==========================

class Order(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Processing", "Processing"),
        ("Shipped", "Shipped"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    PAYMENT_METHODS = [
        ("COD", "Cash On Delivery"),
        ("ALLIED", "Allied Bank Transfer"),
        ("JAZZCASH", "JazzCash"),
        ("EASYPAISA", "EasyPaisa"),
    ]

    PAYMENT_STATUS = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    customer_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=20)

    address = models.TextField()

    city = models.CharField(
        max_length=100,
        default=""
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    order_number = models.CharField(
        max_length=20,
        unique=True
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHODS,
        default="COD"
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default="Pending"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    notes = models.TextField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.order_number} - {self.customer_name}"


# ==========================
# WISHLIST
# ==========================

class Wishlist(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "perfume")

    def __str__(self):
        return f"{self.user.username} - {self.perfume.name}"


# ==========================
# REVIEW
# ==========================

class Review(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    perfume = models.ForeignKey(
        Perfume,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    rating = models.PositiveSmallIntegerField(
        default=5
    )

    comment = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.perfume.name}"
        