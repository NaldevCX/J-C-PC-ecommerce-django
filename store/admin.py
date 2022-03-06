from django.contrib import admin

from .models import Product,ProductCategory,Customer,Order,OrderItem,ShippingAddress
# Register your models here.

#models from the app will be able to see in the admin dashboard
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)