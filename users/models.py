import django
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


ROLES_CHOICES = (
    ('user','USER'),
    ('prm', 'Product Manager'),
    ('dm','Division Manager'),
    ('ca','Company Admin'),

)
STATES_CHOICES = (
     ('Andhra Pradesh','Andhra Pradesh'),
     ('Andaman and Nicobar Islands','Andaman and Nicobar Islands'),
     ('Arunachal Pradesh','Arunachal Pradesh'),
     ('Assam','Assam'),
     ('Bihar','Bihar'),
     ('Chandigarh','Chandigarh'),
     ('Chhattisgarh','Chhattisgarh'),
     ('Dadar and Nagar Haveli','Dadar and Nagar Haveli'),
     ('Daman and Diu','Daman and Diu'),
     ('Delhi','Delhi'),
     ('Lakshadweep','Lakshadweep'),
     ('Puducherry','Puducherry'),
     ('Goa','Goa'),
     ('Gujarat','Gujarat'),
     ('Haryana','Haryana'),
     ('Himachal Pradesh','Himachal Pradesh'),
     ('Jammu and Kashmir','Jammu and Kashmir'),
     ('Jharkhand','Jharkhand'),
     ('Karnataka','Karnataka'),
     ('Kerala','Kerala'),
     ('Madhya Pradesh','Madhya Pradesh'),
     ('Maharashtra','Maharashtra'),
     ('Manipur','Manipur'),
     ('Meghalaya','Meghalaya'),
     ('Mizoram','Mizoram'),
     ('Nagaland','Nagaland'),
     ('Odisha','Odisha'),
     ('Punjab','Punjab'),
     ('Rajasthan','Rajasthan'),
     ('Sikkim','Sikkim'),
     ('Tamil Nadu','Tamil Nadu'),
     ('Telangana','Telangana'),
     ('Tripura','Tripura'),
     ('Uttar Pradesh','Uttar Pradesh'),
     ('Uttarakhand','Uttarakhand'),
     ('West Bengal','West Bengal')

)
COUNTRY_CHOICES = (
    ('india','India'),

)


class States(models.Model):
    state = models.CharField(max_length=50,choices=STATES_CHOICES,)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.state
    class Meta:
        db_table = 'states'




class Countries(models.Model):
    country = models.CharField(max_length=50,choices=COUNTRY_CHOICES)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.country
    class Meta:
        db_table = 'countries'




class Roles(models.Model):
    role = models.CharField(max_length=6, choices=ROLES_CHOICES,default='user')
    roleDescription = models.CharField(max_length=200)
    isActive = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=200)
    createDate = models.DateTimeField()
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.role


class SiteUsers(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.IntegerField(max_length=10,unique=True)
    email = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=20,)
    lastOTP = models.IntegerField(max_length=4, null=True, blank=True)
    role = models.ForeignKey(to=Roles, on_delete=models.SET_NULL,null=True,default='user')
    isActive = models.BooleanField(default=True)
    isLoggedIn = models.BooleanField(default=False)
    isAdmin = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=200)
    createDate = models.DateTimeField()
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.first_name + ' '+self.last_name

#
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         SiteUsers.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.SiteUsers.save()

class UserAddress(models.Model):
    userId = models.ForeignKey(to=SiteUsers, on_delete=models.CASCADE,null=True)
    addressType = models.CharField(max_length=10)
    address1 = models.CharField(max_length=50)
    address2 = models.CharField(max_length=50,null=True,blank=True)
    address3 = models.CharField(max_length=20,null=True,blank=True)
    city = models.CharField(max_length=20)
    state = models.ForeignKey(to=States,on_delete=models.CASCADE)
    country = models.ForeignKey(to=Countries,on_delete=models.CASCADE)
    zip = models.CharField(max_length=10)
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=200,null=True,blank=True)
    createDate = models.DateTimeField(default= django.utils.timezone.now)
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.address1

    class Meta:
        db_table = 'Address'

