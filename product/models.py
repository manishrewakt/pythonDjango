from datetime import datetime

from django.db import models

from users.models import SiteUsers

TAX_TYPE_CHOICES = (
    ('NOTAX', 'NoTax'),
    ('GST','GST'),
    ('VAT', 'VAT'),

)

# Create your models here.
class Currency(models.Model):
    countryCode = models.CharField(max_length=5)
    currencyDes = models.CharField(max_length=40,null=True)
    isActive = models.BooleanField(default= True)

    def __str__(self):
        return self.countryCode

class ProductClass(models.Model):
    name = models.CharField(max_length=50)
    classDescription = models.CharField(max_length=200)
    isActive = models.BooleanField(default=True)
    createdBy = models.ForeignKey(to=SiteUsers, on_delete=models.SET_NULL,null=True,blank=True)
    createDate = models.DateTimeField(default=datetime.now())
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name;


class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    categoryDescription = models.CharField(max_length=200)
    isActive = models.BooleanField(default=True)
    productClass = models.ForeignKey(to=ProductClass, on_delete=models.CASCADE)
    createdBy = models.ForeignKey(to=SiteUsers, on_delete=models.SET_NULL, null=True, blank=True)
    createDate = models.DateTimeField(default=datetime.now())
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.name

class Tax(models.Model):
    TaxType = models.CharField(max_length=10,choices=TAX_TYPE_CHOICES,null=True,blank=True,default='GST')
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=200)
    createDate = models.DateTimeField(default=datetime.now,blank=True)
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.TaxType

class TaxSlab(models.Model):
    TaxType = models.ForeignKey(to=Tax, on_delete=models.CASCADE)
    TaxPercentage = models.IntegerField(max_length=2,default=0)
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=200)
    createDate = models.DateTimeField(default=datetime.now,blank=True)
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.TaxPercentage.__str__()




class Brand(models.Model):
    brandName = models.CharField(max_length=500,default='Generic')
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=200)
    createDate = models.DateTimeField(default=datetime.now,blank=True)
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.brandName

class Product(models.Model):
    name = models.CharField(max_length=50)
    prodDescription = models.CharField(max_length=500)
    brand = models.ForeignKey(to=Brand,on_delete=models.CASCADE,null=True,blank=True)
    prodCategoryId = models.ForeignKey(to=ProductCategory,on_delete=models.CASCADE)
    MRP = models.FloatField()
    sellingPrice =  models.FloatField()
    currency = models.ForeignKey(to=Currency,on_delete=models.CASCADE,default=1)
    isDiscountAvailable = models.BooleanField(default=False)
    discountPercentage = models.IntegerField(default=0)
    isProductAvailable = models.BooleanField(default = True)
    isStockAvailabe =  models.BooleanField(default = True)
    isActive = models.BooleanField(default=True)
    productSpecification = models.CharField(max_length=1000,null=True,blank=True)
    batchNumber = models.CharField(max_length=50,default=0)
    manufactureDate = models.DateTimeField(default=datetime.now,blank=True,null=True)
    tax = models.ForeignKey(to=Tax,on_delete=models.SET_NULL,null=True,blank=True)
    taxSlab = models.ForeignKey(to=TaxSlab, on_delete=models.SET_NULL, null=True, blank=True)
    expiryDate = models.DateTimeField(default=datetime.now,null=True,blank=True)
    createdBy = models.ForeignKey(to=SiteUsers, on_delete=models.SET_NULL, null=True, blank=True)
    createDate = models.DateTimeField(default=datetime.now())
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)
    # image = models.CharField(max_length=300,null=True,blank=True)
    image = models.FileField()
    def __str__(self):
        return self.name

class ProductImages(models.Model):
    ProductImageLocation = models.CharField(max_length=500,)
    product = models.ForeignKey(to=Product,on_delete=models.CASCADE)
    IsPrimaryImage = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)
    createdBy = models.CharField(max_length=200)
    createDate = models.DateTimeField()
    modifiedBy = models.CharField(max_length=200, null=True, blank=True)
    modifiedDate = models.DateTimeField(null=True, blank=True)
    def __str__(self):
        return self.product

class ProductColor(models.Model):
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    productcol = models.CharField(max_length=50, null=True, blank=True)
    def __str__(self):
        return self.productcol
