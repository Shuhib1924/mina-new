from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to="category/", default="default/logo.png")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Categories"


class Variation(models.Model):
    name = models.CharField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # selected = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class Product(models.Model):
    image = models.ImageField(upload_to="product/", default="default/logo.png")
    created_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    variations = models.ManyToManyField(Variation, related_name="product_variation")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="proCat")
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name}"

class Order(models.Model):
    daily_id = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pickup_time = models.DateTimeField()
    email = models.EmailField(max_length=255)


    def __str__(self):
        return f"{self.daily_id} ({self.created_date}) - {self.total} | {self.pickup_time}"

class CartItem(models.Model):
    # cart_id = models.CharField(max_length=200, blank=True)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    # quantity = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"CartItem: {self.product.name}"

    def pro_var_sum(self):
        var_sum = sum(var.price for var in self.variations.all())
        return round(self.product.price + var_sum, 2)
