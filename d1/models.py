from django.db import models

class Meat(models.Model):
    name = models.CharField(max_length=40, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"

class Salat(models.Model):
    name = models.CharField(max_length=40, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"

class Souce(models.Model):
    name = models.CharField(max_length=40, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name}"

class Kebap(models.Model):
    daily_id = models.PositiveIntegerField(unique=False, null=True)
    name = models.CharField(max_length=40, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    meats = models.ManyToManyField(Meat)
    salat = models.ManyToManyField(Salat)
    souce = models.ManyToManyField(Souce)

    def __str__(self):
        return f"{self.name}"
