from django.contrib import admin

# Register your models here
from mysports.models import Order, OrderDetails
from users.models import UserAddress

admin.site.register(Order)
admin.site.register(OrderDetails)
