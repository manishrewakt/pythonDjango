

    if(localStorage.getItem('cart')==null){
        var cart = {};
        console.log('This is new1 working');
    }
    else{
        cart = JSON.parse(localStorage.getItem('cart'));

    }

    $(document).on('click','.atc',function(){
        var item_id = this.id.toString();
        quantityElement = document.getElementById('quantity');
        var itemQuantity = 1
        if(quantityElement != null){
        itemQuantity = document.getElementById('quantity').value;
        }

        if (itemQuantity != null && itemQuantity != '' && itemQuantity >1) {
            itemQuantity = parseInt(document.getElementById('quantity').value);
        }
        else {
            itemQuantity = 1;
        }

        console.log('Quantity');
        if(cart[item_id]!=undefined){
            quantity = cart[item_id][0] + itemQuantity;
            cart[item_id][0] = quantity;
            cart[item_id][2] = cart[item_id][2] + ((cart[item_id][3])*itemQuantity);
        }
        else{
            quantity = itemQuantity;
            price = (parseFloat(document.getElementById("price"+item_id).innerHTML))*itemQuantity;
            unitPrice = parseFloat(document.getElementById("price"+item_id).innerHTML);
            name = document.getElementById("nm"+item_id).innerHTML;
            productId = document.getElementById('PI-'+item_id).innerHTML
            cart[item_id]=[quantity,name,price,unitPrice,productId,item_id];
        }
        localStorage.setItem('cart',JSON.stringify(cart));
        document.getElementById("cart").innerHTML = "Cart("+ Object.keys(cart).length +")";
        DisplayCart(cart);

    });

    DisplayCart(cart);

    function clearLocalStorage(cart){
        localStorage.clear();
        cart = {};
        document.getElementById("cart").setAttribute('data-content','');
        localStorage.setItem('cart',JSON.stringify(cart));
//        DisplayEmptyCart(cart)
        return false;
    }

    function DisplayCart(cart){
        var cartString ="";
        cartString += "<h5>This is your cart</h5>";
        var cartIndex = 1;

        for(var x in cart){
            cartString += cartIndex;
            cartString += "Title:" + cart[x][1] + "Qty:" + cart[x][0] + "Price:" + cart[x][2] + "Unit Price:" + cart[x][3] + "product Id:" + cart[x][4] +"</br>";

            cartIndex+=1;
        }

        cartString += "<a href='/checkout/'><button class='btn btn-warning' id='checkout'>Checkout</button></a> <button class='btn btn-warning' id='emptyCart' onClick='clearLocalStorage(cart);'>Empty Cart</button>";
        document.getElementById("cart").setAttribute('data-content',cartString);
        $('[data-toggle="popover"]').popover();
        document.getElementById("cart").innerHTML = "Cart("+ Object.keys(cart).length +")";
    }

    function DisplayEmptyCart(cart){
            var cartString ="";
            cartString += "<h5>This is your cart</h5>";
            var cartIndex = 1;
            cartString += "<a href='/checkout/'><button class='btn btn-warning' id='checkout'>Checkout</button></a> <button class='btn btn-warning' id='emptyCart' onClick='clearLocalStorage(cart);'>Empty Cart</button>";
            document.getElementById("cart").setAttribute('data-content',cartString);
            $('[data-toggle="popover"]').popover();
            document.getElementById("cart").innerHTML = "Cart("+ 0 +")";
        }

//   $(document).on('click','.rem',function(event, param1, param2){
//         alert( param1 + "\n" + param2 );
//        alert('ID'+id)
//        setTimeout("location.reload(true);");
//    });
