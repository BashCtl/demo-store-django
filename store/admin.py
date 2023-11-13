from django.contrib import admin
from .models import User, Product, ProductCategory, ProductInventory

# Register your models here.
admin.site.register(User)
admin.site.register(ProductCategory)
admin.site.register(ProductInventory)
admin.site.register(Product)