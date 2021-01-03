from django.urls import path
from . import views
urlpatterns = [
    path('', views.homePage, name = "home"),
    path('products/', views.products, name="products"), 
    path('products/<slug:slug>/', views.productDetail, name = "product_detail"),
    path('cart/', views.cart, name = "cart"),
    path('checkout/',views.checkOut, name = "checkout"),   
    
    
]