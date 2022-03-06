import json
from .models import *


#kinda acts as a REST API
def cookieCart(request):
    try: #parsing the cookie
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart ={} #if we don't have the cookie

    print('Cart: ', cart) #getting the cookies name 
    items = [] #empty list; for guest user
    order = {'get_cart_total': 0,'get_cart_items':0,'shipping': False} 
    cartItems = order['get_cart_items']  

    #buidling the order dictionary
    for i in cart: #looping through the string cookie dictionary
        try:
            cartItems += cart[i]["quantity"]

            product = Product.objects.get(id=i) #querying the product
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total;
            order['get_cart_items'] += cart[i]['quantity'] 
                
                #building the item dictionary that will be rendering out in the checkout page
            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price': product.price,
                    'imageURL':product.imageURL
                }, 
                'quantity':cart[i]['quantity'],
                'get_total':total,
                }
            items.append(item)

            #if the product
            if product.product_stock_status == False:
                    order['shipping'] = False
        except: #if anything fails; just ignored it
            pass

    return {'cartItems': cartItems, 'order':order, 'items': items}

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        #create it or find it with the attribute of customer and comeplete is false
        #this object will be created and use at line 20
        order, created = Order.objects.get_or_create(customer = customer, complete=False) #if a user has made an order before or wants to create an order
        
        #order(parent) can query to its child (by itself) and query everything related to order
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items

    else:
       cookieData = cookieCart(request)
       cartItems = cookieData['cartItems']
       order = cookieData['order']
       items = cookieData['items']

    return {'cartItems': cartItems, 'order':order, 'items': items}

def guestOrder(request, data):
    print("user is not logged in")
    print('Cookies: ', request.COOKIES)
    name = data['form']['name']
    email = data['form']['email']
    phone = data['form']['phone']
    # if the user is not logged in but keeps ordering from the website
    cookieData = cookieCart(request)
    items = cookieData['items']

    #all the previous transactions with the customer will be linked via email
    customer, created = Customer.objects.get_or_create(
        email = email,
    )
    customer.name = name
    customer.phone = phone
    customer.save() #creating the user 

    #saving the order in the database
    order = Order.objects.create(
        customer = customer, 
        complete = False,
    )
    
    for item in items: #this from the cookieCart in utils.py accessing the dictionary
        product = Product.objects.get(id = item['product']['id'])

        orderItem = OrderItem.objects.create(
            product = product,
            order = order,
            quantity = item['quantity']
        )
    return customer, order
