from django.urls import path
from . import views
from .views import HomePage, Cart, Checkout, OrderDetails
app_name = 'store'
urlpatterns = [
    path('', HomePage.as_view(), name = "home"),
    path('products/<slug:slug>/', views.productDetail, name = "product_detail"),
    path('cart/', Cart.as_view(), name = "cart"),
    path('checkout',Checkout.as_view(), name = "checkout"),  
    path('orders/',OrderDetails.as_view(), name = 'order') ,
    
    
]