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


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ["name", "price", "active"]
    list_editable = ("active",)


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    list_display = ["name", "required"]
    list_editable = ("required",)


admin.site.register(Variation)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(Random)


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ["rank", "message"]
    ordering = ("rank",)
