from django.db import models
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from django.db.models.deletion import CASCADE, SET_DEFAULT
from django.db.models.fields import DateField, DateTimeField, SlugField
from django.db.models.fields.related import ForeignKey
# Create your models here.
class Customer(models.Model):
    user_id = models.CharField(max_length=1000, default= None)
    first_name = models.CharField(max_length=200, null =True)
    last_name = models.CharField(max_length=200, null =True)
    phone = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=200, null= True)


    def __str__(self):
        return str(self.id)

    def save_customer_details(self):
        self.save()

    @staticmethod
    def get_customer_id(user_id):
        return Customer.objects.filter(id__in = user_id)

    @staticmethod
    def get_customerId_by_email(email):
        return Customer.objects.get(email=email)



  






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
        return str(self.adress)

    @staticmethod
    def get_address_by_customerId(customer):
        return ShippingAddress.objects.get(customer = customer)
    
    def save_address_details(self):
        self.save()


class Order(models.Model):
    STATUS = (
			('Pending', 'Pending'),
			('Out for delivery', 'Out for delivery'),
			('Delivered', 'Delivered'),
			)
    customer = models.ForeignKey(Customer, null = True, blank = True, on_delete = models.SET_NULL)
    product = models.ForeignKey(Product, null = True, blank = True, on_delete = models.SET_NULL)
    shipping_address = models.ForeignKey(ShippingAddress, null = True, blank = True, on_delete = models.SET_NULL)
    price = models.FloatField(null=True)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add = True)
    status = models.CharField(max_length=200, null=True, choices=STATUS, default= 'Pending')

    def __str__(self):
        return str(self.id)

    @staticmethod
    def get_orders_by_customerId(customer):
        return Order.objects.filter(customer=customer)

    def placeOrder(self):
        self.save()

    




