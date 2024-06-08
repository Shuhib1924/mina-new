from django.db import models

class RelatedObject(models.Model):
    name = models.CharField(max_length=100)
    selected = models.BooleanField(default=False)

class Item(models.Model):
    name = models.CharField(max_length=100)
    related_objects = models.ManyToManyField(RelatedObject)