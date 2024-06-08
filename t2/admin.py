from django.contrib import admin
from .models import Product, ProductVariation

admin.site.register(Product)
admin.site.register(ProductVariation)