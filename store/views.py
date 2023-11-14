from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Product, ProductCategory
from .forms import RegistrationForm
from .utils import get_pagination, items_for_page

# Create your views here.


def home(request):
    products = Product.objects.all()
    categories = ProductCategory.objects.all()
    page = request.GET.get('page', 1)
    products_pagination = get_pagination(products, page)
    products_list = items_for_page(products_pagination)

    context = {'products': products_pagination, 'products_list': products_list,
               'categories': categories}
    return render(request, 'store/home.html', context)


def category(request, name):
    products = Product.objects.filter(category__name=name)
    categories = ProductCategory.objects.all()
    page = request.GET.get('page', 1)
    products_pagination = get_pagination(products, page)
    products_list = items_for_page(products_pagination)

    context = {'products': products_pagination, 'products_list': products_list,
               'categories': categories}
    return render(request, 'store/home.html', context)

def product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    context = {'product': product}
    return render(request, 'store/product.html', context)

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
