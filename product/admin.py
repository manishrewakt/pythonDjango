import tax as tax
from django.contrib import admin
from .models import Product, ProductCategory, ProductClass, Currency, Brand, Tax, ProductColor, ProductImages, TaxSlab

# Register your models here.
admin.site.register(ProductClass)
admin.site.register(Product)
admin.site.register(ProductCategory)
admin.site.register(Currency)
admin.site.register(Tax)
admin.site.register(TaxSlab)
admin.site.register(Brand)
admin.site.register(ProductColor)
admin.site.register(ProductImages)





