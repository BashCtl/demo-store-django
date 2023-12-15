from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
import json


from .models import User, Product, ProductCategory, CartItem, Cart
from .forms import RegistrationForm
from .utils import get_pagination, items_for_page, get_cart_data

# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    page = request.GET.get('page', 1)
    products_pagination = get_pagination(products, page)
    products_list = items_for_page(products_pagination)
    data = get_cart_data(request)
    cart_items = data['cart_items']

    context = {'products': products_pagination, 'products_list': products_list,
               'categories': categories, 'cart_items': cart_items}
    return render(request, 'store/home.html', context)


def category(request, name):
    products = Product.objects.filter(category__name=name)
    categories = ProductCategory.objects.all()
    page = request.GET.get('page', 1)
    products_pagination = get_pagination(products, page)
    products_list = items_for_page(products_pagination)

    data = get_cart_data(request)
    cart_items = data['cart_items']

    context = {'products': products_pagination, 'products_list': products_list,
               'categories': categories, 'cart_items': cart_items}
    return render(request, 'store/home.html', context)


@login_required
def product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    data = get_cart_data(request)
    cart_items = data['cart_items']

    context = {'product': product, 'cart_items': cart_items}
    return render(request, 'store/product.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    quantity = int(data['quantity'])

    user = request.user
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=user, complete=False)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart, product=product)
    cart_item.quantity += quantity

    cart_item.save()

    if cart_item.quantity <= 0:
        cart_item.delete()

    return JsonResponse('Item was updated.', safe=False)


def delete_item(request, id):
    product = get_object_or_404(Product, id=id)
    cart_item = get_object_or_404(CartItem, product=product)
    cart_item.delete()
    return JsonResponse('Item was deleted.', safe=False)


def cart(request):
    data = get_cart_data(request)
    cart = data['cart']
    items = data['items']
    cart_items = data['cart_items']

    context = {'items': items, 'cart': cart, 'cart_items': cart_items}
    return render(request, 'store/cart.html', context)


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration.')

    context = {'form': form}
    return render(request, 'store/registration.html', context)


def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except Exception as exc:
            messages.error(request, 'User does not exists.')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong credentials.')
    return render(request, 'store/login.html')


def user_logout(request):
    logout(request)
    messages.success(request, 'You Have Been Logged Out.')
    return redirect('home')
