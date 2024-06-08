from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('cat/<int:cid>/', views.category, name="category"),
    path('pro/<int:pid>/', views.detail, name="detail"),
    path('add_cart/', views.add_cart, name="add_cart"),
    path('delete/<int:id>', views.delete_item, name="delete"),
    path('cart/', views.cart, name="cart"),
]
