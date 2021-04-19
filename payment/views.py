from django.shortcuts import render
from django.template import Context, Template, RequestContext
import hashlib
from django.views.decorators.csrf import csrf_protect, csrf_exempt



from mysports.models import Order, OrderDetails
from mysports.utility import sendEmail
from payment.models import PaymentDetails
from product.models import ProductClass, ProductCategory, Product
import json

from users.models import SiteUsers


def home(request):
    MERCHANT_KEY = "oBkA8OgU"
    key = ""
    SALT = "TrpZ52Rdwb"
    # Merchant ID: 5004161
    PAYU_BASE_URL = "https://test.payu.in/_payment"
    action = ''
    posted = {}
    # Merchant Key and Salt provided y the PayU.
    for i in request.POST:
        posted[i] = request.POST[i]
        print(posted[i])
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid = hash_object.hexdigest()[0:20]
    hashh = ''
    posted['txnid'] = txnid
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    posted['key'] = MERCHANT_KEY
    hash_string = ''
    hashVarsSeq = hashSequence.split('|')
    for i in hashVarsSeq:
        try:
            hash_string += str(posted[i])
        except Exception:
            hash_string += ''
        hash_string += '|'
    hash_string += SALT
    print(hash_string)
    hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
    print('hashh:', hashh)
    action = PAYU_BASE_URL
    posted['surl'] = 'http://127.0.0.1:8000/payment/success/'
    posted['furl'] = 'http://127.0.0.1:8000/payment/failure/'
    if (posted.get("key") != None and posted.get("txnid") != None and posted.get("productinfo") != None and posted.get(
            "firstname") != None and posted.get("email") != None):
        print('Here 123')
        return render(request, 'payment/payUhome.html', {"posted": posted, "hashh": hashh,
                                                                                    "MERCHANT_KEY": MERCHANT_KEY,
                                                                                    "txnid": txnid,
                                                                                    "hash_string": hash_string,
                                                                                    "action":action})
        # return render('payUhome.html', RequestContext(request, {"posted": posted, "hashh": hashh,
        #                                                                             "MERCHANT_KEY": MERCHANT_KEY,
        #                                                                             "txnid": txnid,
        #                                                                             "hash_string": hash_string,
        #                                                                             "action": "https://test.payu.in/_payment"}))
    else:
        return render(request, 'payment/payUhome.html', {"posted": posted, "hashh": hashh,
                                                                 "MERCHANT_KEY": MERCHANT_KEY,
                                                                 "txnid": txnid,
                                                                 "hash_string": hash_string,
                                                                 "action": "."})
        # return render('payUhome.html', RequestContext(request, {"posted": posted, "hashh": hashh,
        #                                                                             "MERCHANT_KEY": MERCHANT_KEY,
        #                                                                             "txnid": txnid,
        #                                                                             "hash_string": hash_string,
        #                                                                             "action": "."}))


@csrf_protect
@csrf_exempt
def success(request):
    # It will only fetch the details of one product
    productClasses = ProductClass.objects.all()
    productCategories = ProductCategory.objects.all()
    classMenuDict = {

    }
    for productClass in productClasses:
        className = productClass.name
        classId = productClass.id
        classMenuDict.update({classId: className})

    context = {
        'classMenuDict': classMenuDict,
        'productCategories': productCategories,
        # 'product': product
    }
    print('Method is ', request.method)
    #-------------------Checking return data
    # hash_value = check_hash(request.POST)
    # print('Hash Values',hash_value)
    # if check_hash(request.POST):
    #     return HttpResponse("Transaction has been Successful.")
    status = request.POST["status"]
    print('status -- All the Input params -- ', status)
    print("--------------------------------------")
    for i in request.POST:
        print(i, request.POST[i])
    print("--------------------------------------")

    if request.method == "POST":
        items = request.POST.get('productinfo', '')
        final_order = json.loads(items)
        # printing final result
        for key in final_order:
            # getting length of list
            list = final_order[key]
            length = len(list)


        # name = request.POST.get('name', "")
        email = request.POST.get('email', "")
        address = request.POST.get('address', "")
        city = request.POST.get('city', "")
        state = request.POST.get('state', "")
        zipcode = request.POST.get('zipcode', "")
        total = request.POST.get('amount', "")
        user = getUserId(email)
        print(user)
        order = Order(email=email, address=address, city=city, state=state, zipcode=zipcode,
                       total=total,orderedBy=user)
        order.save()
        print(order)
        # # Saving the order details
        for key in final_order:
            # getting length of list
            list = final_order[key]
            orderDetail = OrderDetails(orderId=order,itemId=Product.objects.get(pk=key),itemQuantity=list[0],name = list[1],sellingPrice =list[3])
            orderDetail.save()
        # Saving the transaction OrderDetails
        print(order)
        transactionalDetail = PaymentDetails(paymentType=request.POST['mode'],
                                             orderId=order,
                                             mihpayid=request.POST['mihpayid'],
                                             status=request.POST['status'],
                                             txnid=request.POST['status'],
                                             payuMoneyId=request.POST['payuMoneyId'],
                                             net_amount_debit=request.POST['net_amount_debit'],
                                             paidBy=user
                                             )

        transactionalDetail.save()
        #End of Saving details
        context['order_details'] = order
        context['orderedItems'] = final_order
        sendEmail(orderid=order.id, orderedItems=final_order, email=email)
        print('Competed')
    #
    # c = {}
    # c.update(request)
        status = request.POST["status"]
        print(status)
        firstname = request.POST["firstname"]
        amount = request.POST["amount"]
        txnid = request.POST["txnid"]
        posted_hash = request.POST["hash"]
        key = request.POST["key"]
        productinfo = request.POST["productinfo"]
        email = request.POST["email"]
        salt = "TrpZ52Rdwb"
        try:
            additionalCharges = request.POST["additionalCharges"]
            retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        except Exception:
            retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
        if (hashh != posted_hash):
            print
            "Invalid Transaction. Please try again"
        else:
            print
            "Thank You. Your order status is ", status
            print
            "Your Transaction ID for this transaction is ", txnid
            print
            "We have received a payment of Rs. ", amount, ". Your order will soon be shipped."
        # context = {"txnid": txnid, "status": status, "amount": amount}
        # return render('paymentsuccess.html',
        #                           RequestContext(request, {"txnid": txnid, "status": status, "amount": amount}))
    return render(request, 'payment/paymentsuccess.html', context)

@csrf_protect
@csrf_exempt
def failure(request):
    context = {}
    # It will only fetch the details of one product
    productClasses = ProductClass.objects.all()
    productCategories = ProductCategory.objects.all()
    classMenuDict = {

    }
    for productClass in productClasses:
        className = productClass.name
        classId = productClass.id
        classMenuDict.update({classId: className})

    context = {
        'classMenuDict': classMenuDict,
        'productCategories': productCategories,
        # 'product': product
    }
    status = request.POST["status"]
    firstname = request.POST["firstname"]
    amount = request.POST["amount"]
    txnid = request.POST["txnid"]
    posted_hash = request.POST["hash"]
    key = request.POST["key"]
    productinfo = request.POST["productinfo"]
    email = request.POST["email"]
    salt = "TrpZ52Rdwb"
    try:
        additionalCharges = request.POST["additionalCharges"]
        retHashSeq = additionalCharges + '|' + salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    except Exception:
        retHashSeq = salt + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    status = request.POST["status"]
    print('status -- All the Input params -- ', status)
    for i in request.POST:
        print(i, request.POST[i])
    if hashh != posted_hash:
        print("Invalid Transaction. Please try again")
    else:
        print("Thank You. Your order status is ", status)
        print("Your Transaction ID for this transaction is ", txnid)
        print("We have received a payment of Rs. ", amount, ". Your order will soon be shipped.")
    return render(request, 'payment/Failure.html', context)
    # return render("Failure.html", RequestContext(request, c))

# Brand - LearnManish
# password -Kaju05@laddu
# https://www.payumoney.com/dev-guide/apireference.html#operation/Manage%20InvoicesControllerUsingPUT
#https://developer.payumoney.com/test-mode/

def getUserId(email):
    user = SiteUsers.objects.get(email=email)
    return user