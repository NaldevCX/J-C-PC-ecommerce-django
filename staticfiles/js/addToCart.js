var addBtns = document.getElementsByClassName('update-cart')

//looping through the query set
for (var i = 0; i < addBtns.length; i++) {
    addBtns[i].addEventListener('click', function(){
        //using the addBtns variable that is current pointing to class that has 'update=cart'
        var productID = this.dataset.product
        var action = this.dataset.action
        console.log("productID: ", productID, 'ACTION: ', action)
        console.log('USER: ', user)

        if (user == 'AnonymousUser') {
            addCookieItem(productID, action)
        } else {
            updateUserOrder(productID, action)
        }
    })
    
}

function addCookieItem(productID, action){
    console.log('User is not authenticated')
    //what the cart cookie should look like
    // cart = {
    //    productId
    //     1: {'quantity': 4},
    //     3: {'quantity': 1},
    //     6: {'quantity': 1},
    // }
    if(action =='add'){
        if(cart[productID]==undefined){
            cart[productID] = {'quantity':1}
        }else{
            cart[productID]['quantity'] += 1
        }
    } 
    
    if(action =='remove'){
        cart[productID]['quantity'] -= 1
        if(cart[productID]['quantity'] <= 0){ //removing item from the cookie
            console.log('Item should be deleted');
            delete cart[productID] //delete the key in the cookie
        }
    }
    console.log('Cart: ', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    
    location.reload()
    
}

function updateUserOrder(productID, action) {
    console.log('User is authenticated, sending data..')

    //Sending the data using FETCH API

    //send data in a URL and have a response after sending data
    var url = '/update_item/'

    fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },

            //body is the data we will be sending to the backend
            //we need to send it as a string since JSON can process object
            body: JSON.stringify({
                'productID': productID,
                'action': action
            })
        })

        //we need to return a promise/response
        //**send data to the view, and once the data is processed and organized we need to response 
        //with a promise **

        .then((response) => {
            return response.json()
        })

        //seeing the data what we are sending to the view,py updateItem function
        .then((data) => {
            console.log('Data: ', data)
            location.reload();
        })
}