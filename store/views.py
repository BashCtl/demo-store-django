from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Product
from .forms import RegistrationForm

# Create your views here.


def home(request):
    products = Product.objects.all()

    context = {'products': products}
    return render(request, 'store/home.html')


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