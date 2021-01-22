from django.http import request
from django.shortcuts import get_object_or_404, render, redirect
from django.template import context
from .models import *
from django.views import View
# Create your views here.
class HomePage(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:    
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1 
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart

        
        return redirect('store:home')
    def get(self, request):
        products = None
        cart = request.session.get('cart')
        uid = request.session.get('uId')
        print(uid)
        if not cart:    
            request.session['cart'] = {}
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_products_by_categoryId(categoryID)


        else:
            products = Product.get_all_products()

        context = {'products': products,
                'categories': categories,
                }

        return render(request, 'store/home.html', context)




def productDetail(request, slug):
    products = get_object_or_404(Product, slug=slug)
    context = {'products': products}
    return render(request, 'store/details.html', context)


def categoryDetail(request, category_id):
    categories = Category.get_all_categories()
    products = Product.objects.get(category_id)
    context = {'categories': categories,
               'products': products}
    return render(request, 'store/categories_detail.html', context)


class Cart(View):
    def post(self,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:    
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1 
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart',request.session['cart'])
        return redirect('store:cart')
    def get(self, request):
        product_id = list(request.session.get('cart').keys())
        products = ProductVariationOption.get_products_by_id(product_id) 
        items = ProductVariationOption.get_products_by_id(product_id)    
        context = {'products':products, 'items':items}
        return render(request, 'store/cart.html', context)



class Checkout(View):
    def post(self, request):
        
        cart = request.session.get('cart')
        products = Product.get_product_by_id(list(cart.keys()))
        customer = request.session.get('customer')
        print("hello:",customer)
        for product in products:
            order = Order(customer = Customer(id=customer), product = product, 
                    shipping_address = ShippingAddress.get_address_by_customerId(customer),
                    price = product.price, quantity = cart.get(str(product.id)))
            order.placeOrder()

        request.session['cart'] = {}

        return redirect('store:cart')
  
    
class OrderDetails(View):
    def get(self,request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customerId(customer)
        context = {'orders': orders}
        return render(request, 'store/orders.html', context)



