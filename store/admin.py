from django.contrib import admin
from .models import User, Product, ProductCategory, ProductInventory, Cart, CartItem

# Register your models here.


class ProductInventoryAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity')


admin.site.register(User)
admin.site.register(ProductCategory)
admin.site.register(ProductInventory, ProductInventoryAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
