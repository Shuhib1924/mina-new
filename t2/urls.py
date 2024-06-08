from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list2'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart2'),
    path('cart/', views.cart, name='cart2'),
    path('test', views.test, name='test'),
    path('delete/', views.delete_session, name='delete_session')
]