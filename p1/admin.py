from django.contrib import admin
from .models import Product, Variation, Category, CartItem, Order

admin.site.register(Variation)
admin.site.register(CartItem)
admin.site.register(Order)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

# class VariationInline(admin.TabularInline):
#     model = Product.variations.through

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    # inlines = [VariationInline]

class CartItemInline(admin.TabularInline):
    model = CartItem

# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
    # inlines = [CartItemInline]