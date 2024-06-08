from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# variation =

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return f" {self.product.name}"