from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder #utility package

#sending emails
from django.core.mail import send_mail
from django.core.mail.message import EmailMessage
from django.conf import settings
from django.core import mail

from django.template.loader import render_to_string

#Homepage
def browse(request): 
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        'products': products, 
        'cartItems':cartItems
        } 
    return render(request, 'store/product.html',context)


def category_laptop(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.filter(ProductCategory__title__contains ="Laptop")
    context = {
        'products': products, 
        'cartItems':cartItems
        } 
    
    return render(request, 'store/laptop.html', context)

def faq(request): 
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {
        'products': products, 
        'cartItems':cartItems
        } 
    return render(request, 'store/faq.html',context)

#Cartpage
def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems #numbers of items in the cart page
                }

    return render(request, 'store/cart.html',context)

def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    #the dictionary will be sent in to the html file
    context = {
        'items':items,
        'order':order,
        'cartItems':cartItems
            }

    return render(request, 'store/checkout.html',context)

#JSON Response
def updateItem(request):
    #implementing sending POST REQUEST using an API
    # request.body is where the dictionary of our data is stored
    data = json.loads(request.body)

    #contains the value of productID from the FETCH api
    productID = data['productID']
    action = data['action']

    print("productID: ", productID)
    print("Action: ", action)

    # Querying all the data for the order table
    # getting the user that is currently logged in
    customer = request.user.customer
    product = Product.objects.get(id=productID)
    #transaction for the OrderTable
    order, created = Order.objects.get_or_create(customer=customer, complete= False)
    

    """
    if the OrderItem object isnt created, we need to change the order value if it doesnt exist

    Note:
        Return value of OrderItem.objects.get_or_create()
        set the order value to the order we just query, and set the product that is also queried
    
    -  reasone why to use get_or_create is because if the OrderItem already exist according to product and order
        *we dont want to create a new orderItem. we just want to change the quantity

        *in short: pag naglagay ka ng item sa cart mo dun lang sa cart page mo lang siya pwede i-edit yugn quantity*
    """
    #the add-to-cart 
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    #the 'add' is coming from the product.html that has a data-action ='add'
    if action =='add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('Item was Added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if(request.user.is_authenticated): #processsing the logged in user
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete= False)

    else: #for processing the guest user's order
        customer, order = guestOrder(request, data) #data is from the JSON file (javascript stuff)

    #regardless, that the user is logged in or not 
    #getting the user data from json 
    total = float(data['form']['total'])
    email = data['form']['email']
    customerName = data['form']['name']
    order_id = order.orderId
    order_date = datetime.datetime.now() 
    order.transaction_id = transaction_id

    if total == order.get_cart_total: 
        order.complete = True
        #saving the trasaction or commit = true
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            nearestlandmark = data['shipping']['nearestlandmark'],
            province = data['shipping']['province'],
            barangay = data['shipping']['barangay'],
        )
    
    #email sending starts here
    template = render_to_string('store/invoice.html', {
        'name':customerName,
        'total':total,
        'transaction_id':transaction_id,
        'order_date':order_date,
        'order_id':order_id
    })

    connection = mail.get_connection()
    connection.open()
    email = mail.EmailMessage(
        'Thanks you for Purchasing from J&C PC',
        template,
        settings.EMAIL_HOST_USER,
        [email],
    )
    email.fail_silently = False
    connection.send_messages([email])
    connection.close()

    return JsonResponse('Payment complete..', safe = False)

