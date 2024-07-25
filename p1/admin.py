from django.contrib import admin
from .models import (
    Product,
    Variation,
    Category,
    Query,
    Order,
    Notification,
    Screen,
    Random,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("rank",)


class QueryInline(admin.TabularInline):
    model = Query.product_query.through


class VariationInline(admin.TabularInline):
    model = Variation.query_variation.through


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    inlines = [QueryInline]


@admin.register(Query)
class QueryAdmin(admin.ModelAdmin):
    inlines = [VariationInline]


admin.site.register(Variation)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(Random)


@admin.register(Screen)
class ScreenAdmin(admin.ModelAdmin):
    list_display = ["rank", "message"]
    ordering = ("rank",)
