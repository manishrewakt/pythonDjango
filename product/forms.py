from django import forms
from .models import ProductClass, ProductCategory, Product, Tax, Brand,TaxSlab
from django.forms import ModelChoiceField


class CategoryForm(forms.ModelForm):
    productClass = forms.ModelChoiceField(queryset=ProductClass.objects.all(), initial=0)

    class Meta:
        model = ProductCategory
        fields = [
        "productClass",
        ]
class ProductForm(forms.ModelForm):
    Category = forms.ModelChoiceField(queryset=ProductCategory.objects.all(), initial=0)

    class Meta:
        model = Product
        fields = [
        "Category",
        ]

class TaxForm(forms.ModelForm):
    tax = forms.ModelChoiceField(queryset=Tax.objects.all(), initial=0)

    class Meta:
        model = Product
        fields = [
        "tax",
        ]
class BrandForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), initial=0)

    class Meta:
        model = Brand
        fields = [
        "brand",
        ]


class TaxSlabForm(forms.ModelForm):
    TaxSlab = forms.ModelChoiceField(queryset=TaxSlab.objects.all(), initial=0)

    class Meta:
        model = TaxSlab
        fields = [
        "TaxSlab",
        ]
