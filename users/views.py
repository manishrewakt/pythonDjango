import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

from mysports.models import Order, OrderDetails
from mysports.utility import sendEmailPasswordRecovery
from product.models import ProductClass, ProductCategory
from .models import SiteUsers, Roles, UserAddress, States, Countries
import datetime
from mysports.views import index, repeatTheOrder
from django.contrib import messages
from utility.constants import ERROR_PHONE_EMAIL, fast2smsURL, fast2sms_headers, INFO_USERNAME_PWD_RECOVERY, \
    UNIQUE_EMAIL_PHONE_CONSTAINT_VIOLATION, UNIQUE_EMAIL_PASSWORD_CONSTAINT_VIOLATION, UNIQUE_EMAIL_DOESNOT_EXIST, \
    INFO_USERPERSONAL_DETAIL_CHANGED, ERROR_USER_PERSONAL_DETAILS, INFO_USERADDRESS_DETAIL_CHANGED
from utility.menu import *


# Create your views here.
def pullMenuDetails():
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
    return context


def createUser(request):
    context = getMenu()
    if request.method == "POST":
        try:
            login_data = request.POST.dict()
            print(login_data)
            context['login_data'] = login_data
            username = login_data.get("email")
            email = request.POST.get('email', '')
            password = request.POST.get('exampleInputPassword1', "")
            firstName = request.POST.get('firstName', "")
            lastName = request.POST.get('lastName', "")
            mobileNo = int(request.POST.get('mobileNo', ))
            role = request.POST.get('roles', )
            roleDetails = Roles.objects.get(role=role)
            print(roleDetails)

            # user = SiteUsers(first_name=firstName, last_name=lastName, email=email,
            #                  mobile=mobileNo, password=password, role=roleDetails,
            #                  createdBy='admin', createDate=datetime.datetime.now())

            # user.save()

            address1 = request.POST.get('address1', "")
            address2 = request.POST.get('address2', "")
            print(request.POST.get('country', ""))
            print('result')
            country = Countries.objects.get(country = request.POST.get('country', "").lower())
            print('Hi 2')
            zip = request.POST.get('zip', "")
            print('Hi 3')

            state = States.objects.get(state=request.POST.get('state', ""))
            # state = request.POST.get('state', "")
            city = request.POST.get('city', "")
            print('Hi 4')

            address3 = request.POST.get('address3', "")
            if address3 != '':
                address4 = request.POST.get('address4', "")
                print(request.POST.get('country', ""))
                country1 = Countries.objects.get(country=request.POST.get('country1', "").lower())
                zip1 = request.POST.get('zip1', "")
                state1 = States.objects.get(state=request.POST.get('state1', ""))
                # state = request.POST.get('state', "")
                city1 = request.POST.get('city1', "")
            else:
                address3 = address1
                address4 = address2
                country1 = country
                zip1 = zip
                state1 = state
                # state = request.POST.get('state', "")
                city1 = city

            print('Hi 4')
            # userAddress.save()
            with transaction.atomic():
                user = SiteUsers(first_name=firstName, last_name=lastName, email=email,
                                 mobile=mobileNo, password=password, role=roleDetails,
                                 createdBy='admin', createDate=datetime.datetime.now())

                userAddressShipping = UserAddress(userId=user, addressType='shipping', address1=address1, address2=address2,
                                          country=country, zip=zip, state=state, city=city)

                userAddressBilling = UserAddress(userId=user, addressType='billing', address1=address3, address2=address4,
                                          country=country1, zip=zip1, state=state1, city=city1)
                user.save()
                userAddressShipping.save()
                userAddressBilling.save()


            user.isLoggedIn = True;
            # Set a session value
            # request.session['user'] = user
            # Set a session value
            request.session['userId'] = user.id
            request.session['userLoggedIn'] = user.isLoggedIn
            request.session['userName'] = user.first_name
            print('Hi 2')
            # *******
            message = f'Your account with us is succeeefuly create. Your login id is {username}'
            url = fast2smsURL
            payload = f"sender_id=FSTSMS&message={message}&language=english&route=p&numbers={mobileNo}"
            headers = fast2sms_headers
            response = requests.request("POST", url, data=payload, headers=headers)
            # *******
            return index(request, user)
        except Exception as error:
            print(error)
            messages.error(request, error)
            print('Email id or phone already exist')

            return render(request, 'users/createUser.html', context)

    return render(request, 'users/createUser.html', context)


def signIn(request):
    print('Inside Sign in')
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
    print(request.method)
    if request.method == "POST":
        login_data = request.POST.dict()
        context['login_data'] = login_data
        # username = login_data.get("email")
        email = request.POST.get('email')
        password = request.POST.get('password')
        # mobileNo = int(request.POST.get('mobileNo', ))
        user = ''

        try:
            user = SiteUsers.objects.get(email=email)
            if user.password != password:
                messages.error(request, UNIQUE_EMAIL_PASSWORD_CONSTAINT_VIOLATION)
                return render(request, 'users/signIn.html', context)
        except Exception as error:
            print(error)
            messages.error(request, UNIQUE_EMAIL_DOESNOT_EXIST)
            return render(request, 'users/signIn.html', context)

        user.isLoggedIn = True;
        print(user.first_name)

        # Set a session value
        request.session['userId'] = user.id
        request.session['userLoggedIn'] = user.isLoggedIn
        request.session['userName'] = user.first_name

        print(user.id)
        print(user.isLoggedIn)
        userRole = user.role
        print('User role', userRole.role)
        if userRole.role == 'prm':
            print('I am here')
            return render(request, 'users/productAdminHome.html', context)
        print('I am nothing')
        return index(request, user)
    print('Done')
    return render(request, 'users/signIn.html', context)


def signOut(request):
    print('User ID is ', request.session['userId'])
    # del request.session['name']
    # del request.session['password']
    request.session.flush()
    return index(request)


def forgotIdPwd(request):
    print('I forgot my password')
    context = {}
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
    if request.method == "POST":
        email = request.POST.get('email')
        # password = request.POST.get('password')
        phone = request.POST.get('phone#', )
        print('Phone:', phone)
        print('email:', email)
        user = ''
        try:
            if (email != None and email != ''):
                print('email:', email)
                user = SiteUsers.objects.get(email=email)
                sendEmailPasswordRecovery(email=email, password=user.password)
                messages.success(request, INFO_USERNAME_PWD_RECOVERY)
                print('Success recovered')
                return render(request, 'users/forgetIDPWD.html', context)
            elif (phone != None and phone != ''):
                print('Phone:', phone)
                print(phone)
                user = SiteUsers.objects.get(mobile=phone)
                getUserNameAndPwd(user)
                messages.success(request, INFO_USERNAME_PWD_RECOVERY)
                print('Success recovered')
                return render(request, 'users/forgetIDPWD.html', context)
        except ObjectDoesNotExist:
            messages.error(request, ERROR_PHONE_EMAIL)
            return render(request, 'users/forgetIDPWD.html', context)

        return index(request, user)

    return render(request, 'users/forgetIDPWD.html', context)


def userOrders(request, id):
    context = pullMenuDetails()
    # Get the user email
    order = Order.objects.filter(orderedBy=id)
    orderDetails = OrderDetails.objects.filter(orderId__in=order)
    context['orders'] = order
    context['orderDetails'] = orderDetails

    return render(request, 'users/userOrders.html', context)


def userAccount(request, id):
    context = pullMenuDetails()
    user = SiteUsers.objects.get(pk=id)
    orders = Order.objects.filter(orderedBy=id)
    userAddresses = UserAddress.objects.filter(userId=id).filter(isActive = True)
    context['user'] = user
    context['orders'] = orders
    context['userAddresses'] = userAddresses
    print(userAddresses)

    return render(request, 'users/userAccount.html', context)


def specificUserOrder(request, userid, orderid):
    print('hi')
    context = pullMenuDetails()
    user = getUserSessionData(request)
    if user == None:
        user = SiteUsers.objects.get(pk=userid)
    print('hi 1')
    order = Order.objects.filter(pk=orderid)
    orderDetails = OrderDetails.objects.filter(orderId__in=order)
    context['orders'] = order
    context['orderDetails'] = orderDetails
    context['user'] = user
    print('hi 2')
    return render(request, 'users/userOrders.html', context)


def getUserSessionData(request):
    # Set a session value
    if request.session.get('userId', True):
        print('Exists')
        return request.session['userId']
    else:
        print('Does not Exists')
        return None


def getUserNameAndPwd(user):
    # *******
    message = f'Your login id is {user.email} and password is {user.password}'
    url = fast2smsURL
    payload = f"sender_id=FSTSMS&message={message}&language=english&route=p&numbers={user.mobile}"
    headers = fast2sms_headers
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    # *******


def updateUserDetails(request,id,changeType):
    if request.session.get('userId'):
        context = pullMenuDetails()
        if request.method == "POST":
            email = request.POST.get('email')
            mobile = request.POST.get('mobileNo')
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')
            type = request.POST.get('type')
            role = request.POST.get('roles', )
            context['type'] = type

            print('id:',id,'Type:',type)
            user = ''
            if type == '1':
                try:
                    roleDetails = Roles.objects.get(role=role)
                    user = SiteUsers.objects.get(pk=id)
                    user.email = email
                    user.mobile = mobile
                    user.first_name = firstName
                    user.last_name = lastName
                    user.role = roleDetails
                    user.save()
                    messages.success(request, INFO_USERPERSONAL_DETAIL_CHANGED)
                    return userAccount(request,user.id)
                except Exception as error:
                    messages.error(request, error)
                    return render(request, 'users/changeUserPersonalDetails.html', context)
            elif type == '2':
                try:
                    userAddresses = UserAddress.objects.get(pk=id)
                    context['userAddresses'] = userAddresses
                    if userAddresses.addressType == 'shipping':
                        userAddresses.address1 = request.POST.get('address1')
                        userAddresses.address2 = request.POST.get('address2')
                        userAddresses.city = request.POST.get('city')
                        userAddresses.state = States.objects.get(state=request.POST.get('state', ""))
                        userAddresses.country = Countries.objects.get(country=request.POST.get('country', "").lower())
                        userAddresses.zip = request.POST.get('zip')
                    elif userAddresses.addressType == 'billing':
                        userAddresses = UserAddress.objects.get(pk=id)
                        userAddresses.address1 = request.POST.get('address3')
                        userAddresses.address2 = request.POST.get('address4')
                        userAddresses.city = request.POST.get('city1')
                        userAddresses.state = States.objects.get(state=request.POST.get('state1', ""))
                        userAddresses.country = Countries.objects.get(country=request.POST.get('country1', "").lower())
                        userAddresses.zip = request.POST.get('zip1')
                    userAddresses.save()
                    messages.success(request, INFO_USERADDRESS_DETAIL_CHANGED)
                    return userAccount(request,userAddresses.userId.id)
                except Exception as error:
                    messages.error(request, error)
                    return render(request, 'users/changeUserAddress.html', context)

            return render(request, 'users/userAccount.html', context)
        htmlPage = ''
        if changeType == 1:
            user = SiteUsers.objects.get(pk=id)
            context['user'] = user
            context['type'] = changeType
            htmlPage = 'users/changeUserPersonalDetails.html'
        elif changeType == 2:
            userAddresses = UserAddress.objects.get(pk=id)
            context['userAddresses'] = userAddresses
            context['type'] = changeType
            htmlPage = 'users/changeUserAddress.html'

        # context['user'] = user
        # context['userAddresses'] = userAddresses
        # print(userAddresses)

        return render(request, htmlPage, context)
    else:
        return signIn(request)


def addUserShippingAddress(request,id):
    print(request.get_full_path())
    if request.session.get('userId'):
        context = getMenu()
        user = SiteUsers.objects.get(pk=id)
        context['user'] = user
        if request.method == "POST":
            try:
                login_data = request.POST.dict()
                print(login_data)
                context['login_data'] = login_data
                address1 = request.POST.get('address1', "")
                address2 = request.POST.get('address2', "")
                country = Countries.objects.get(country=request.POST.get('country', "").lower())

                zip = request.POST.get('zip', "")
                state = States.objects.get(state=request.POST.get('state', ""))
                city = request.POST.get('city', "")
                userAddressShipping = UserAddress(userId=user, addressType='shipping', address1=address1, address2=address2,
                                          country=country, zip=zip, state=state, city=city)

                userAddressShipping.save()
                messages.success(request, INFO_USERPERSONAL_DETAIL_CHANGED)
                return userAccount(request, user.id)

            except Exception as error:
                print(error)
                messages.error(request, error)
                print('Email id or phone already exist')

                return render(request, 'users/addNewShippingAddress.html', context)

        return render(request, 'users/addNewShippingAddress.html', context)
    else:
        return signIn(request)

def deleteUserShippingAddress(request,id):
    # if request.session.get('userId', None):
    #     print('Not an active session')
    #     return signIn(request)
    if request.session.get('userId'):
        context = pullMenuDetails()
        if request.method == "POST":
            try:
                userAddresses = UserAddress.objects.get(pk=id)
                userAddresses.isActive = False
                userAddresses.save()
                context['userAddresses'] = userAddresses
                messages.success(request, INFO_USERADDRESS_DETAIL_CHANGED)
                return userAccount(request, userAddresses.userId.id)
            except ObjectDoesNotExist:
                messages.error(request, ERROR_USER_PERSONAL_DETAILS)
                return render(request, 'users/inactivateUserAddress.html', context)
        userAddresses = UserAddress.objects.get(pk=id)
        context['userAddresses'] = userAddresses
        return render(request, 'users/inactivateUserAddress.html', context)
    else:
        return signIn(request)

def popupAddressChange(request,addressid,orderId):
    context = {}
    addressId = request.GET.get('addressId')
    if request.method == "POST":
        try:
            print('Form is submitted now')
            login_data = request.POST.dict()
            userAddresses = UserAddress.objects.get(pk=addressid)
            userAddresses.address1 = login_data['address1']
            userAddresses.address2 = login_data['address2']
            userAddresses.city = login_data['city']
            userAddresses.state = States.objects.get(state=login_data['state'])
            userAddresses.country = Countries.objects.get(country=login_data['country'].lower())
            userAddresses.zip = request.POST.get('zip')
            userAddresses.save()
            print(login_data)
            return repeatTheOrder(request,orderId)

        except Exception as error:
            print(error)
            messages.error(request, error)
            return repeatTheOrder(request,orderId)
    else:
        userAddresses = UserAddress.objects.get(pk=addressid)
        context['userAddresses'] = userAddresses
        context['orderId'] = orderId
        return render(request, 'users/popupAddressEdit.html', context)

def popupPersonalDetailsChange(request,userId,orderId):
    context = {}
    user = SiteUsers.objects.get(pk=userId)
    if request.method == "POST":
        try:
            print('Form is submitted now')
            login_data = request.POST.dict()
            print(login_data)

            user.first_name = login_data['first_name']
            user.last_name = login_data['last_name']
            user.email = login_data['email']
            user.mobile = login_data['mobile']
            user.save()
            return repeatTheOrder(request,orderId)

        except Exception as error:
            print(error)
            messages.error(request, error)
            return repeatTheOrder(request,orderId)
    else:
        user = SiteUsers.objects.get(pk=userId)
        context['user'] = user
        context['orderId'] = orderId
        context['userId'] = userId
        return render(request, 'users/popupPersonalDetailsEdit.html', context)


def productAdminHome(request,userId):
    user = SiteUsers.objects.get(pk=userId)
    context ={}
    context['user'] = user
    return render(request, 'users/productAdminHome.html',)
