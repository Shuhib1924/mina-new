from django.db import models
from django.utils import timezone
from PIL import Image
import threading
import datetime
from django.core.exceptions import ValidationError


class Random(models.Model):
    message = models.TextField()
    image = models.ImageField(upload_to="random/", default="default/logo.png")

    def __str__(self):
        return f"{self.message}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.background.path)
        if img.height > 400 or img.width > 400:
            img.thumbnail((400, 400), Image.LANCZOS)
            img.save(self.background.path)


class Notification(models.Model):
    message = models.CharField(max_length=300)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.message} - {self.status}"


class Screen(models.Model):
    image = models.ImageField(upload_to="screen/", default="default/logo.png")
    message = models.CharField(max_length=300)
    rank = models.IntegerField(default=0, unique=True)

    def __str__(self) -> str:
        return f"{self.rank}: {self.message}"


class Category(models.Model):
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to="category/", default="default/logo.png")
    background = models.ImageField(upload_to="category/", default="default/logo.png")
    rank = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.background.path)
        if img.height > 200 or img.width > 200:
            img.thumbnail((200, 200), Image.LANCZOS)
            img.save(self.background.path)


class Product(models.Model):
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to="product/", default="default/logo.png")
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)
    private = models.CharField(max_length=100, blank=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    rank = models.IntegerField(default=0, null=True)
    menu = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="product_menu",
    )

    def __str__(self) -> str:
        if self.private == "":
            return f"{self.name}"
        else:
            return f"PRIVAT: {self.private} | {self.name}"


class Query(models.Model):
    name = models.CharField(max_length=100)
    rank = models.IntegerField(default=0)
    private = models.CharField(max_length=100, blank=True)
    product_query = models.ManyToManyField(Product, related_name="product_query")
    required = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Queries"

    def __str__(self) -> str:
        if self.private == "":
            return f"{self.name}"
        else:
            return f"PRIVAT: {self.private} | {self.name}"


class Variation(models.Model):
    # active = models.BooleanField(default=True)
    name = models.CharField(max_length=100)
    private = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=6, default=0.00)
    image = models.ImageField(upload_to="variation_image/")
    rank = models.IntegerField(default=0, null=True)
    query_variation = models.ManyToManyField(Query, related_name="query_variation")

    def __str__(self) -> str:
        if self.private == "":
            return f"{self.name}"
        else:
            return f"PRIVAT: {self.private} | {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 200 or img.width > 200:
            img.thumbnail((200, 200), Image.LANCZOS)
            img.save(self.image.path)


class Order(models.Model):
    daily_id = models.PositiveIntegerField(unique=False)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    orderID = models.CharField(max_length=40, null=True)
    transactionID = models.CharField(max_length=40, null=True)
    paypal_total = models.DecimalField(
        max_digits=10, decimal_places=2, default=0, null=True
    )
    href = models.URLField(max_length=100, null=True)

    paypal_first_name = models.CharField(max_length=40, null=True)
    paypal_last_name = models.CharField(max_length=40, null=True)
    paypal_email = models.EmailField(max_length=40, null=True)
    paypal_id = models.CharField(max_length=40, null=True)

    form_pickup_time = models.CharField(max_length=40, null=True)
    form_name = models.CharField(max_length=40, null=True)
    form_email = models.EmailField(max_length=40, null=True)
    form_phone = models.CharField(max_length=40, null=True)

    order_data = models.TextField(blank=True, null=True)
    paypal_data = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            raise ValidationError("Updates are not allowed.")
        super(Order, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        raise ValidationError("Deletion is not allowed.")

    def __str__(self):
        return f"DailyID: {self.daily_id} Created:({self.created_date}) - {self.paypal_total} | {self.form_pickup_time} | TransactinID - {self.transactionID}"
