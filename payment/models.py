import django
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

from mysports.models import Order
from users.models import SiteUsers

User = get_user_model()

class Transaction(models.Model):
    made_by = models.ForeignKey(User, related_name='transactions',
                                on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)

class PaymentDetails(models.Model):
    paymentType = models.CharField(max_length=50)
    orderId = models.ForeignKey(to=Order, on_delete=models.CASCADE)
    mihpayid = models.CharField(max_length=50,default='123456789')
    status  = models.CharField(max_length=50,default='success')
    txnid = models.CharField(max_length=50,default='1000000')
    bank_ref_num  =  models.CharField(max_length=50,blank=True,null=True)
    bankcode = models.CharField(max_length=50,blank=True,null=True)
    name_on_card = models.CharField(max_length=50,blank=True,null=True)
    cardnum = models.CharField(max_length=50,blank=True,null=True)
    payuMoneyId = models.CharField(max_length=50,default='1112263210')
    net_amount_debit = models.FloatField(max_length=50,default=0.0)
    isActive = models.BooleanField(default=True)
    paidBy = models.ForeignKey(to=SiteUsers, on_delete=models.CASCADE)
    paidDate = models.DateTimeField(default=django.utils.timezone.now)
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)




    class Meta:
        # ordering = ('paymentFor',)
        db_table = 'Payment_Details'

    def __str__(self):
        return str(self.orderId);

