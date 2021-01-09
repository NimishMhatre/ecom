from django.urls import path
from . import views
from .views import HomePage, Cart
urlpatterns = [
    path('', HomePage.as_view(), name = "home"),
    path('products/', views.products, name="products"), 
    path('products/<slug:slug>/', views.productDetail, name = "product_detail"),
    path('cart/', Cart.as_view(), name = "cart"),
    path('checkout/',views.checkOut, name = "checkout"),   
    
    
]