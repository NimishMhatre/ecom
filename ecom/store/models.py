from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.db.models.deletion import CASCADE, SET_DEFAULT
from django.db.models.fields import DateField, DateTimeField, SlugField
from django.db.models.fields.related import ForeignKey
# Create your models here.
class Customer(models.Model):
    username = models.OneToOneField(User, null=True, blank= True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null =True)
    email = models.EmailField(max_length=200, null= True)


    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=255, null= False)
    slug = models.SlugField(max_length=255, null= False)
    image = models.ImageField(upload_to = 'uploads/category/', null = True, blank = True)

    class Meta:
        verbose_name_plural = 'Categories'


    @staticmethod
    def get_all_categories():
        return Category.objects.all()


    def __str__(self):
        return self.category_name


class Product(models.Model):
    
    category = models.ForeignKey(Category, null = True, blank= True,related_name= 'products', on_delete= models.CASCADE)
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField(max_length=255, null= True)
    price = models.FloatField( null=True)
    image = models.ImageField( null = True, blank= True)
    description = models.CharField(max_length = 200, null = True)
    date_created = models.DateTimeField(auto_now_add = True, null = True)

    @staticmethod
    def get_all_products():
        return Product.objects.all()


    @staticmethod
    def get_product_by_id(product_id):
        return Product.objects.filter(id__in = product_id)
        


    @staticmethod
    def get_products_by_categoryId(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products()
 
    
    def __str__(self):
        return self.name


class ProductVariationOption(models.Model):
    SIZE = (
        ('Small','S'),
        ('Large','L'),
        ('Extra Large', 'XL'),
        ('Double Extra large', 'XXL'),
    )
    COLOUR = (
        ('Black', 'Black'),
        ('Red', 'Red'),
        ('Blue', 'Blue'),
    )
    product = models.ForeignKey(Product, null = True, blank= True,related_name= 'products', on_delete= models.CASCADE)
    size = models.CharField(max_length=200, null=True, choices = SIZE)
    colour = models.CharField(max_length=200, null=True, choices=COLOUR)



    def __str__(self):
        return str(self.id)


    @staticmethod
    def get_products_by_id(product_id):
        return ProductVariationOption.objects.filter(id__in = product_id)



class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    adress = models.CharField(max_length=300, null =False)
    city = models.CharField(max_length=100, null =False)
    state = models.CharField(max_length=100, null =False)
    counrty = models.CharField(max_length=100, null =False)
    pin_code = models.CharField(max_length=50, null =False)

    def __str__(self):
        return str(self.address)


class Order(models.Model):
    STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
    customer = models.ForeignKey(Customer, null = True, blank = True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null = True, blank = True, on_delete = models.SET_NULL)
    shipping_address = models.ForeignKey(ShippingAddress, null = True, blank = True, on_delete = models.SET_NULL)
    ordered_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)

    def __str__(self):
        return str(self.id)
    

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, null = True, blank = True, on_delete = models.SET_NULL)
    quantity = models.IntegerField(default = 0, null = True, blank = True)
    product_variation_option = models.ForeignKey(ProductVariationOption, null=True, blank=True,on_delete=models.SET_NULL)


    def __str__(self):
        return str(self.id)


