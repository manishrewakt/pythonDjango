from import_export import resources
from .models import ProductClass

class ProductClassResource(resources.ModelResource):
    class Meta:
        model = ProductClass
        fields = ('name', 'classDescription','isActive')

#https://django-import-export.readthedocs.io/en/latest/getting_started.html#creating-import-export-resource