from typing import Tuple
from django.db import models
import uuid
from django.contrib.auth.models import User
from django.db.models.base import Model

# Create your models here.

#After the user signs/register in the database
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null= True)
    email = models.CharField(max_length=200, null= True)
    phone = models.CharField(max_length=12, null=True)
    def __str__(self):
        return str(self.name)

class Product(models.Model):
    #makes unique id in 16 characters
    name = models.CharField(max_length=200)
    price = models.DecimalField(default=0000.0, decimal_places=2, max_digits=7, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    product_category = models.ForeignKey('ProductCategory', on_delete=models.CASCADE, null=False, blank=False)
    featured_image = models.ImageField(upload_to='product_images',null=False, blank=False)
    date_added = models.DateTimeField(auto_now_add=True)
    product_stock_status = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Products'

    #shows what is first thing you will see in the database
    def __str__(self):
        return self.name
    
    @property #lets rendering out data by the method instead of by attrib
    def imageURL(self):
          try:
               img = self.featured_image.url
          except:
               img = ''
          return img

    #formatting the price field with a dollar sign
    @property
    def price_display(self):
        return 'Php {0}'.format(self.price)

    @property
    def shortDesc(self):
        return f"{self.description[:50]}..."
        """ Return a string representtation of the model`"""    

    
class ProductCategory(models.Model):
    title = models.CharField(max_length=200)
    #upload_to will go to base_dir/static/media/product_images then it will go to category_images dir
    image = models.ImageField(upload_to='category_images', null=True, blank = False)
    created = models.DateTimeField(auto_now_add=True)
    category_id = models.UUIDField(default= uuid.uuid4, editable=False, unique=True, primary_key=True)

    class Meta:
        verbose_name_plural = 'Product Category'

    def  __str__(self):     
          return self.title

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete = models.SET_NULL, blank = True, null= True)
    date_ordered = models.DateTimeField(auto_now_add = True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return F"Transaction ID: {str(self.id)}"

    #check if a product is selected or manage to be in the cart to page
    @property
    def shipping(self): 
        shipping = False
        orderItems = self.orderitem_set.all()
        for i in orderItems:
            if i.product.product_stock_status == True: #means if the product is available
                shipping = True
        return shipping

    @property
    def get_cart_total(self): #total cart value
        #query all the objects and child orderitem model
        orderItems = self.orderitem_set.all()

        #run a loop and calculate the total of the item get_total (per product in a row)
        #item = is the iterator (think of it as foreach method)
        total = sum([item.get_total for item in orderItems]) 
        return total
    
    @property
    def get_cart_items(self): #
        orderItems = self.orderitem_set.all()
        total =  sum([item.quantity for item in orderItems])
        return total

    @property
    def orderId(self):
        return F"Transaction ID: {str(self.id)}"

class OrderItem(models.Model): #checkout
    product = models.ForeignKey(Product, on_delete = models.SET_NULL, blank = True, null= True)
    order = models.ForeignKey(Order, on_delete = models.SET_NULL, blank = True, null= True)
    quantity = models.IntegerField(default=0, null= True, blank= True)
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'Ordered Item'

    def __str__(self):
        return f"Order ID: {self.order}"
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=200, null=True)
    province = models.CharField(max_length=200, null=True)
    nearestlandmark = models.CharField(max_length=200, null=True)
    barangay = models.CharField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name_plural = 'Shipping Address'

    def __str__(self):
        return f"{self.order}"

