import django
from django.db import models

# Create your models here.
from django.utils.timezone import now

from product.models import Product
from users.models import SiteUsers, States, Countries


class Order(models.Model):
    # items = models.CharField(max_length=1000)
    # name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    address1 = models.CharField(max_length=50,default='')
    address2 = models.CharField(max_length=50, null=True, blank=True)
    address3 = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    zip = models.CharField(max_length=10)
    mobile = models.IntegerField(max_length=10)
    email = models.CharField(max_length=100)
    total = models.CharField(max_length=10)
    orderedBy = models.ForeignKey(to=SiteUsers, on_delete=models.CASCADE,default=2)
    orderDate = models.DateTimeField(default= django.utils.timezone.now)

    class Meta:
        ordering = ('orderDate',)
        db_table = 'orders'
    def __str__(self):
        return str(self.id)


class OrderDetails(models.Model):
    orderId = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    itemId = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    itemQuantity = models.IntegerField()
    name = models.CharField(max_length=50)
    sellingPrice = models.FloatField()
    created = models.DateTimeField(default= django.utils.timezone.now)

    class Meta:
        ordering = ('created',)
        db_table = 'order_details'



