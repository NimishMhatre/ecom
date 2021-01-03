from django.http import request
from django.shortcuts import get_object_or_404, render, redirect
from .models import *

# Create your views here.
def homePage(request):
    
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_products_by_categoryId(categoryID)


    else:
        products = Product.get_all_products()
        
        
    context = { 'products': products,
                'categories': categories}

    return render(request, 'store/home.html', context)



def products(request):
    product_variation_options = ProductVariationOption.objects.all()
    context = {'product_variation_options' : product_variation_options,
                }
    return render(request, 'store/products.html', context)  


def productDetail(request, slug):
    products = get_object_or_404(Product, slug=slug)
    context ={'products' : products}
    return render(request, 'store/details.html', context)  


def categoryDetail(request, category_id):
    categories = Category.get_all_categories()
    products = Product.objects.get(category_id)
    context = {'categories':categories, 
                'products': products}
    return render(request, 'store/categories_detail.html', context) 


def cart(request):
    return render(request, 'store/cart.html')


def checkOut(request):
    return render(request, 'store/checkout.html')



