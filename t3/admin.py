from django.contrib import admin
from .models import Item, RelatedObject

admin.site.register(Item)
admin.site.register(RelatedObject)
