from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class ProductCategory(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductInventory(models.Model):
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.quantity)


class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images', default='default.jpg')
    badge = models.CharField(max_length=15, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, related_name='products')
    inventory = models.OneToOneField(
        ProductInventory, on_delete=models.CASCADE, related_name='product')

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        # total = sum([item.get_total for item in self.items])
        return 0



class CartItem(models.Model):
    quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, null=True, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self) -> str:
        return f"{self.product.name}: {self.quantity}"