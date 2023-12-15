from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('category/<str:name>', views.category, name='category'),
    path('product/<int:pk>', views.product, name='product'),
    path('update-item/', views.update_item, name='update_item'),
    path('delete-item/<int:id>', views.delete_item, name='delete_item'),
    path('cart/', views.cart, name='cart'),
]
