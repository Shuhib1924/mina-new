from django.contrib import admin
from .models import (
    Product,
    Variation,
    Category,
    Query,
    Notification,
    Screen,
    Random,
    Order,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("rank",)
    list_display = ["name", "rank"]
    list_editable = ("rank",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "price", "active"]
    list_editable = ("active",)


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ["name", "private", "rank", "required", "single", "active"]
    list_editable = ("required", "rank", "single", "active")


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]
    list_editable = ("price",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display = ["form_name", "form_phone", "form_pickup_time"]

    # list_editable = ("form_name", "form_phone", "form_pickup_time")

    ordering = ("-created_date",)
    # readonly_fields = ("paypal_data", "order_data")


admin.site.register(Random)
# class RandomAdmin(admin.ModelAdmin):
# list_display = ["name", "value"]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["message", "status"]
    list_editable = ("status",)


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ["rank", "message"]
    ordering = ("rank",)
