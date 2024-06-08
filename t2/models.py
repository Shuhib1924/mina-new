from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

class ProductVariation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_name = models.CharField(max_length=50)
    is_selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.variation_name}"