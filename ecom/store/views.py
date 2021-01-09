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
        print('cart',request.session['cart'])
        return redirect('home')
    def get(self, request):
        products = None
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_products_by_categoryId(categoryID)


        else:
            products = Product.get_all_products()

        context = {'products': products,
                'categories': categories}

        return render(request, 'store/home.html', context)


def products(request):
    product_variation_options = ProductVariationOption.objects.all()
    context = {'product_variation_options': product_variation_options,
               }
    return render(request, 'store/products.html', context)


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
    def get(self, request):
        product_id = list(request.session.get('cart').keys())
        products = ProductVariationOption.get_products_by_id(product_id)    
        context = {'products':products}
        return render(request, 'store/cart.html', context)



def checkOut(request):
    return render(request, 'store/checkout.html')
