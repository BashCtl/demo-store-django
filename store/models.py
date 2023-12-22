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
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_total(self):
        total = sum([item.get_total for item in self.items.all()])
        return total

    @property
    def get_cart_items(self):
        return sum([item.quantity for item in self.items.all()])


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


class BillingAddress(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=250)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    cart = models.OneToOneField(
        Cart, on_delete=models.CASCADE, primary_key=True)
    
    def __str__(self):
        return f"first_name={self.first_name}, last_name={self.last_name}, cart={self.cart}"
