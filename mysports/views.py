import datetime
from random import randint

import requests
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, redirect

# Create your views here.
from mysports.models import Order, OrderDetails
from mysports.utility import sendEmail
from product.models import ProductClass, ProductCategory, Product
import json

from users.models import SiteUsers, UserAddress, States, Countries

from django.shortcuts import render
from django.template import Context, Template, RequestContext
import hashlib
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings

from utility.menu import getMenu


def index(request, userDetails=None):
    productClasses = ProductClass.objects.all().filter(isActive=True)
    productCategories = ProductCategory.objects.all()
    productList = Product.objects.all()
    # productList = Product.objects.get_queryset().order_by('id')
    search_item = request.GET.get('search_item')
    print(search_item)
    catagory = request.GET.get('catagory')
    if catagory != '' and catagory is not None:
        productList = productList.filter(prodCategoryId=catagory)
    if search_item != '' and search_item is not None:
        productList = productList.filter(prodDescription__icontains=search_item)
    classMenuDict = {

    }
    for productClass in productClasses:
        className = productClass.name
        classId = productClass.id
        classMenuDict.update({classId: className})

    # Pagination Logic
    page = request.GET.get('page')
    paginator = Paginator(productList,10)
    productList = paginator.get_page(page)
    context = {
        'classMenuDict': classMenuDict,
        'productCategories': productCategories,
        'productList': productList,
        'userDetails': userDetails
    }
    return render(request, 'mysports/index.html', context)


def details(request, id):
    # It will only fetch the details of one product
    productClasses = ProductClass.objects.all().filter(isActive=True)
    productCategories = ProductCategory.objects.all()
    classMenuDict = {

    }
    for productClass in productClasses:
        className = productClass.name
        classId = productClass.id
        classMenuDict.update({classId: className})

    product = Product.objects.get(id=id)
    context = {
        'classMenuDict': classMenuDict,
        'productCategories': productCategories,
        'product': product
    }
    return render(request, 'mysports/detail.html', context)


def checkout(request):
    context = getMenu()
    if request.method == "POST":
        print('Its Post')
        items = request.POST.get('items', '')
        print('Its Post',items)
        # converting string to json
        final_order = json.loads(items)
        # printing final result
        for key in final_order:
            # getting length of list
            list = final_order[key]
            length = len(list)

            # Iterating the index
            # same as 'for i in range(len(list))'
            # for i in range(length):
            #     print(list[i])
        user = None
        userAddress = None
        email = None
        firstname = None
        lastname = None
        mobile = None
        address1 = None
        address2 = None
        city = None
        state = None
        country = None
        zipcode = None
        if request.session.get('userId') is not None:
            print(request.session['userId'])
            userId= int(request.session['userId'])
            try:
                user = getUser(userId)
                email = user.email
                userAddress = getUserAddress(int(request.POST.get('shipping')))
            except Exception as ex:
                print(ex)
        # else:
            # email = request.POST.get('email', "")
            # user = getUserId(email)
            # if user == None:
            #     firstname = request.POST.get('first_name', "")
            #     lastname = request.POST.get('last_name', "")
            #     mobile = request.POST.get('mobileNo', "")
            #     address1 = request.POST.get('address1', "")
            #     address2 = request.POST.get('address2', "")
            #     city = request.POST.get('city', "")
            #     state = request.POST.get('state', "")
            #     country = request.POST.get('country', "")
            #     zipcode = request.POST.get('zipcode', "")
            # else:
            #     # userAddress = getUserAddress(int(request.POST.get('shipping')))
            #     firstname = user.first_name
            #     email= user.email
            #     lastname = user.last_name
            #     mobile = user.mobile
            #     address1 = request.POST.get('address1', "")
            #     address2 = request.POST.get('address2', "")
            #     city = request.POST.get('city', "")
            #     state = request.POST.get('state', "")
            #     country = request.POST.get('country', "")
            #     zipcode = request.POST.get('zipcode', "")
            #     pass
        total = request.POST.get('total', "")
        # user = getUserId(email)
        # Payment Initiated
        postDataToPayU = makePayment(request,user)
        # postDataToPayU = makePaymentToPayU(request)
        postDataToPayU['classMenuDict'] = context['classMenuDict']
        postDataToPayU['productCategories'] = context['productCategories']
        print(postDataToPayU)
        # print('My responce is ',response)
        # Payment ended
        with transaction.atomic():
            order = None
            if user != None:
                if userAddress != None:
                    order = Order(
                                  first_name=user.first_name ,last_name=user.last_name,
                                  email=user.email, mobile=user.mobile,address1=userAddress.address1,
                                  address2=userAddress.address2, city=userAddress.city,
                                  state=userAddress.state, zip=userAddress.zip,
                                  total=total,orderedBy=user)
                # else:
                    # order = Order(
                    #     first_name=user.first_name, last_name=user.last_name,
                    #     email=user.email, mobile=user.mobile, address1=address1,
                    #     address2=address2, city=city,
                    #     state=state, zip=zip,
                    #     total=total, orderedBy=user)
            # else:
                # user = SiteUsers(first_name=firstname, last_name=lastname, email=email,
                #                  mobile=mobile, password='test1234',
                #                  createdBy='admin', createDate=datetime.datetime.now())
                # print(state)
                # state = States.objects.get(state=state)
                # country = Countries.objects.get(country=country)
                #
                # userAddressShipping = UserAddress(userId=user, addressType='shipping', address1=address1,
                #                                   address2=address2,
                #                                   country=country, zip=zip, state=state, city=city)
                #
                # userAddressBilling = UserAddress(userId=user, addressType='billing', address1=address1,
                #                                  address2=address2,
                #                                  country=country, zip=zip, state=state, city=city)
                # print('saving user')
                # user.save()
                # userAddressShipping.save()
                # userAddressBilling.save()
                # print('Saved')
                # order = Order(
                #     first_name=firstname, last_name=lastname,
                #     email=email, mobile=mobile, address1=address1,
                #     address2=address2, city=city,
                #     state=state, zip=zip,
                #     total=total, orderedBy=user)
            order.save()
            # # Saving the order details
            for key in final_order:
                # getting length of list
                list = final_order[key]
                orderDetail = OrderDetails(orderId=order,itemId=Product.objects.get(pk=key),itemQuantity=list[0],name = list[1],sellingPrice =list[3])
                orderDetail.save()

        context['order_details'] = order
        context['orderedItems'] = final_order
        sendEmail(orderid=order.id, orderedItems=final_order, email=email)
        print('Competed')
        # return render(request, 'mysports/success.html', context)
        # return render(request, 'mysports/checkout.html', context)

        # return redirect("https://test.payu.in/_payment",postDataToPayU)
        # # print(responceObject)
        # return render(request, 'payment/payUhomeBackup.html', postDataToPayU)
        return render(request, 'payment/payUhome.html', postDataToPayU)
    else:

        print('Id:',request.session.get('userId'))
        if request.session.get('userId') is not None:
            print(request.session['userId'])
            userId= int(request.session['userId'])
            try:
                print('Request',request.session['userId'])
                user = getUser(userId)
                print('Request', request.session['userId'])
                userAddress = UserAddress.objects.filter(userId=userId).filter(isActive=True)
                print("User: ")
                context['user'] = user
                context['userAddress'] = userAddress
            except Exception as ex:
                 print(ex)

        else:
            print('User not logged in')
        return render(request, 'mysports/checkout.html', context)



def getUserId(email):
    print(email)
    try:
        user = SiteUsers.objects.get(email=email)
    except Exception as ex:
        print(ex)
        return None
    return user


def makePayment(request,user):
    MERCHANT_KEY = settings.PAYU_MERCHANT_KEY
    key = ""
    SALT = settings.PAYU_MERCHANT_SALT
    # Merchant ID: 5004161
    PAYU_BASE_URL = settings.PAYU_BASE_URL
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid = hash_object.hexdigest()[0:20]

    action = ''
    posted = {}
    if user == None:
        posted['firstname'] = request.POST.get('first_name', '')
        email = request.POST.get('email', "")
        mobileNo = request.POST.get('mobileNo', "")
        posted['email'] = email
        posted['udf1'] = request.POST.get('last_name', '')
        posted['udf2'] = request.POST.get('address1', '')
        posted['udf3'] = request.POST.get('address2', '')
        posted['udf4'] = request.POST.get('city', '')
        posted['udf5'] = request.POST.get('state', '')
        posted['udf6'] = request.POST.get('country', '')
        posted['udf7'] = request.POST.get('zipcode', '')
    else:
        # print('Shipping Address' , request.POST.get('shipping'))
        posted['firstname'] = user.first_name
        email = user.email
        mobileNo = user.mobile
        posted['email'] = email
        posted['udf1'] = user.last_name
        userAddress = getUserAddress(request.POST.get('shipping'))
        if userAddress == None:
            posted['udf2'] = request.POST.get('address1', '')
            posted['udf3'] = request.POST.get('address2', '')
            posted['udf4'] = request.POST.get('city', '')
            posted['udf5'] = request.POST.get('state', '')
            posted['udf6'] = request.POST.get('country', '')
            posted['udf7'] = request.POST.get('zipcode', '')
        else:
            posted['udf2'] = userAddress.address1
            posted['udf3'] = userAddress.address2
            posted['udf4'] = userAddress.city
            posted['udf5'] = userAddress.state
            posted['udf6'] = userAddress.country
            posted['udf7'] = userAddress.zip
    # user = getUserId(email)
    posted['amount'] = request.POST.get('total', "")
    items =  request.POST.get('items', '')
    if items != None or items != '':
        posted['productinfo'] = request.POST.get('items', '')
        print('Nothing')
    else:
        posted['productinfo'] = 'Repeat order'
        print('Everything')
    posted['txnid'] = txnid
    posted['key'] = MERCHANT_KEY


    # # Merchant Key and Salt provided y the PayU.
    # for i in request.POST:
    #     posted[i] = request.POST[i]
    #     print(i,posted[i])
    # for i in posted:
    #     # posted[i] = request.POST[i]
    #     print(i,posted[i])
    hashh = ''
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    # print(hash_string)
    hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    action = PAYU_BASE_URL
    host = request.get_host()
    # print( request.is_secure())

    posted['surl'] = request.scheme+'://'+host+'/payment/success/'
    # posted['furl'] = 'http://127.0.0.1:8000/payment/failure/'
    posted['furl'] = request.scheme+'://'+host+'/payment/failure/'
    # print('Calling PAY PAISA')
    postDataToPayU = {}
    if (posted.get("key") != None and posted.get("txnid") != None and
            posted.get("productinfo") != None and posted.get("firstname") != None
            and posted.get("email") != None):
        postDataToPayU = {"posted": posted, "hashh": hashh,
                          "MERCHANT_KEY": MERCHANT_KEY,
                          "txnid": txnid,
                          "hash_string": hash_string,
                           "action": action}

    else:
        postDataToPayU = {"posted": posted, "hashh": hashh,
                          "MERCHANT_KEY": MERCHANT_KEY,
                          "txnid": txnid,
                          "hash_string": hash_string,
                          "action": action}

    return postDataToPayU

def makePaymentToPayU(request):
    data = {}
    user = getUserId(request.POST.get('email', ""))
    txnid = get_transaction_id()
    hash_ = generate_hash(request, txnid)
    hash_string = get_hash_string(request, txnid)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = settings.PAYU_BASE_URL
    data["amount"] = request.POST.get('total', "")
    data["productinfo"] = request.POST.get('items', '')
    data["key"] = settings.PAYU_MERCHANT_KEY
    data["txnid"] = txnid
    data["hash"] = hash_
    data["hash_string"] = hash_string
    data["firstname"] = user.first_name
    data["email"] = request.POST.get('email', "")
    data["phone"] = user.mobile
    # data["service_provider"] = constants.SERVICE_PROVIDER
    host = request.get_host()
    data["furl"] = request.scheme + '://' + host + '/payment/success/'
    # posted['furl'] = 'http://127.0.0.1:8000/payment/failure/'
    data["surl"]  = request.scheme + '://' + host + '/payment/failure/'
    return data
    # return render(request, "students/payment/payment_form.html", data)
# generate the hash
def generate_hash(request, txnid):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request,txnid)
        generated_hash = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        # logging.getLogger("error_logger").error(traceback.format_exc())
        return None

# create hash string using all the fields
def get_hash_string(request, txnid):
    user = getUserId(request.POST.get('email', ""))
    hash_string = settings.PAYU_MERCHANT_KEY+"|"+txnid+"|"+request.POST.get('total', "")+"|"+request.POST.get('items', '')+"|"
    hash_string += user.first_name+"|"+request.POST.get('email', "")+"|"
    hash_string += "||||||||||"+settings.PAYU_MERCHANT_SALT

    return hash_string

# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid

def showCart(request):
    context = getMenu()
    if request.method == "POST":
        items = request.POST.get('items', '')
        # converting string to json
        final_order = json.loads(items)
        # printing final result
        for key in final_order:
            # getting length of list
            list = final_order[key]
            length = len(list)

            # Iterating the index
            # same as 'for i in range(len(list))'
            for i in range(length):
                print(list[i])

        # firstname = request.POST.get('firstname', "")
        # email = request.POST.get('email', "")
        # lastname = request.POST.get('lastname', "")
        # address1 = request.POST.get('address1', "")
        # address2 = request.POST.get('address2', "")
        # city = request.POST.get('city', "")
        # state = request.POST.get('state', "")
        # country = request.POST.get('country', "")
        # zipcode = request.POST.get('zipcode', "")
        # total = request.POST.get('total', "")
        # user = getUserId(email)
        # Payment Initiated
        postDataToPayU = makePayment(request)
        # postDataToPayU = makePaymentToPayU(request)
        postDataToPayU['classMenuDict'] = classMenuDict
        postDataToPayU['productCategories'] = productCategories
        print(postDataToPayU)
        # print('My responce is ',response)
        # Payment ended

        # order = Order(email=email, address=address, city=city, state=state, zipcode=zipcode,
        #               total=total,orderedBy=user)
        # order.save()
        # # Saving the order details
        # for key in final_order:
        #     # getting length of list
        #     list = final_order[key]
        #     orderDetail = OrderDetails(orderId=order,itemId=Product.objects.get(pk=key),itemQuantity=list[0],name = list[1],sellingPrice =list[3])
        #     orderDetail.save()
        # context['order_details'] = order
        # context['orderedItems'] = final_order
        # sendEmail(orderid=order.id, orderedItems=final_order, email=email)
        # print('Competed')
        # return render(request, 'mysports/success.html', context)
        # return render(request, 'mysports/checkout.html', context)

        # return redirect("https://test.payu.in/_payment",postDataToPayU)
        # # print(responceObject)
        # return render(request, 'payment/payUhomeBackup.html', postDataToPayU)
        return render(request, 'payment/payUhome.html', postDataToPayU)
    else:
        return render(request, 'mysports/showCart.html', context)


def getUser(id):
    try:
        user = SiteUsers.objects.get(id=id)
    except Exception as ex:
        print(ex)
        return None
    return user

def getUserAddress(id):
    print('Add id',id)
    if id == None:
        return None
    userAddress = UserAddress.objects.get(id=int(id))
    return userAddress


def repeatOrderPLacement(request, orderId, context):
    login_data = request.POST.dict()
    user = None
    userAddress = None
    order = Order.objects.get(id=orderId)
    orderDetails = OrderDetails.objects.filter(orderId=order)
    products = []
    for orderdetail in orderDetails:
        products.append(Product.objects.get(id=orderdetail.itemId.id))
    final_order = ''
    if request.session.get('userId') is not None:
        # print('User id is ',request.session['userId'])
        # print(login_data)
        userId = int(request.session['userId'])
        try:
            user = getUser(userId)
            email = user.email
            userAddress = getUserAddress(int(request.POST.get('shipping')))
            # print(userAddress)
        except Exception as ex:
            print(ex)

    totalAmount = request.POST.get('total', "")
    # Payment Initiated
    postDataToPayU = makePayment(request, user)
    postDataToPayU['classMenuDict'] = context['classMenuDict']
    postDataToPayU['productCategories'] = context['productCategories']
    with transaction.atomic():
        order = None
        if user != None:
            if userAddress != None:
                order = Order(
                    first_name=user.first_name, last_name=user.last_name,
                    email=user.email, mobile=user.mobile, address1=userAddress.address1,
                    address2=userAddress.address2, city=userAddress.city,
                    state=userAddress.state, zip=userAddress.zip,
                    total=totalAmount, orderedBy=user)
        order.save()
        # Saving the order details
        final_order = 'Your final order is /n'
        for product in products:
            pid = product.id
            quantityOrdered = request.POST.get(f"{pid}-quantity")
            if int(quantityOrdered) > 0:
                final_order = final_order + product.name +':' + str(product.sellingPrice) + '/n'
                orderDetail = OrderDetails(orderId=order, itemId=product, itemQuantity=quantityOrdered,
                                           name=product.name, sellingPrice=product.sellingPrice)
                orderDetail.save()
        final_order = final_order + f'Total Cost of the order is:{totalAmount}'
    context['order_details'] = order
    context['orderedItems'] = final_order
    sendEmail(orderid=order.id, orderedItems=final_order, email=email)
    # print('Competed')
    # # return render(request, 'mysports/success.html', context)
    # # return render(request, 'mysports/checkout.html', context)
    # # return redirect("https://test.payu.in/_payment",postDataToPayU)
    # # # print(responceObject)
    # # return render(request, 'payment/payUhomeBackup.html', postDataToPayU)
    return render(request, 'payment/payUhome.html', postDataToPayU)


def repeatTheOrder(request,id):
    context = getMenu()
    if request.method == 'POST':
        print(7*'++')
        return repeatOrderPLacement(request,id,context)
    order = Order.objects.get(id=id)
    orderDetails = OrderDetails.objects.filter(orderId = order)
    products = []

    for orderdetail in orderDetails:
        products.append(Product.objects.get(id=orderdetail.itemId.id))

    user= getUser(order.orderedBy.id)
    userAddress = UserAddress.objects.filter(userId=user.id).filter(isActive=True)


    context['products'] = products
    context['user'] = user
    context['userAddress'] = userAddress
    context['orderId'] = id
    context['total'] = order.total
    print('total no of products', len(products))
    context['totalProducts'] = len(products)
    return render(request, 'mysports/repeatOrder.html',context)

# https://developers.payu.com/en/restapi.html
