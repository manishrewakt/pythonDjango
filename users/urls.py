from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [
    path('createUser/', views.createUser, name='createUser'),
    path('signIn/', views.signIn, name='signIn'),
    path('signOut/', views.signOut, name='signOut'),
    path('forgotIdPwd/', views.forgotIdPwd, name='forgotIdPwd'),
    path('userOrders/<int:id>', views.userOrders, name='userOrders'),
    path('userAccount/<int:id>', views.userAccount, name='userAccount'),
    path('specificUserOrder/<int:userid>/<int:orderid>', views.specificUserOrder, name='specificUserOrder'),
    path('updateUserDetails/<int:id>/<int:changeType>', views.updateUserDetails, name='updateUserDetails'),
    path('addUserShippingAddress/<int:id>', views.addUserShippingAddress, name='addUserShippingAddress'),
    path('deleteUserShippingAddress/<int:id>', views.deleteUserShippingAddress, name='deleteUserShippingAddress'),
    path('popupAddressChange/<int:addressid>/<int:orderId>', views.popupAddressChange, name='popupAddressChange'),
    path('popupPersonalDetailsChange/<int:userId>/<int:orderId>', views.popupPersonalDetailsChange, name='popupPersonalDetailsChange'),
    path('productAdminHome/<int:userId>/',views.productAdminHome,name='productAdminHome')

]