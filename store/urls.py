from django.urls import path
from . import views

urlpatterns = [
    #homepage
    path('',views.browse, name="browse"),

    #add to cart page
    path('cart/', views.cart, name="cart"),

    #faq page
    path('faq/', views.faq, name="faq"),
    
    #laptop page
    path('category_laptop/', views.category_laptop, name="laptop"),

    #checkout page
    path('checkout/', views.checkout, name="checkout"),

    #Json Response
    path('update_item/', views.updateItem, name="update_item"),
    
    #Json Response
    path('process_order/', views.processOrder, name="process_order")
    
]
