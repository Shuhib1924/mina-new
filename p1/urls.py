from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:cslug>/", views.category, name="category"),
    path("product/<slug:pslug>/", views.detail, name="detail"),
    path("cart/", views.cart, name="cart"),
    path("delete/<int:index>", views.delete, name="delete"),
    path("checkout/", views.checkout, name="checkout"),
    path("order/", views.order, name="order"),
    path("success/", views.success, name="success"),
    path("failed/", views.failed, name="failed"),
    # path("printing/", views.printing, name="printing"),
]
