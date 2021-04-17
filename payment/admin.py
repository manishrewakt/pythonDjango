from django.contrib import admin

# Register your models here.
from payment.models import PaymentDetails

admin.site.register(PaymentDetails)
