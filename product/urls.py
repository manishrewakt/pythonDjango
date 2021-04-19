from django.contrib import admin
from django.urls import path

from product import views

urlpatterns = [
    path('addProductClass/', views.addProductClass, name='addProductClass'),
    path('addProductCategory/', views.addProductCategory, name='addProductCategory'),
    path('addProduct/', views.addProduct, name='addProduct'),
    path('listProductClass/<int:userId>/', views.listProductClass, name='listProductClass'),
    path('listProductCategory/<int:userId>/', views.listProductCategory, name='listProductCategory'),
    path('listProductCategoryClassWise/<int:userId>/', views.listProductCategoryClassWise, name='listProductCategoryClassWise'),
    path('listOfProducts/<int:userId>/', views.listProduct, name='listProduct'),

    path('inactivateProductClass/<int:classId>/<int:userId>/', views.inactivateProductClass, name='inactivateProductClass'),
    path('inactivateProductCategory/<int:categoryId>/<int:userId>/', views.inactivateProductCategory, name='inactivateProductCategory'),
    path('inactivateProduct/<int:productId>/<int:userId>/', views.inactivateProduct,name='inactivateProduct'),



    path('bulkUploadProductClass/', views.bulkUploadProductClass, name='bulkUploadProductClass'),
    path('bulkUploadProductCategory/', views.bulkUploadProductCategory, name='bulkUploadProductCategory'),
    path('bulkUploadProducts/', views.bulkUploadProducts, name='bulkUploadProducts'),

    path('searchProductClass/<int:userId>/', views.searchProductClass, name='searchProductClass'),
    path('searchProductCategory/<int:userId>/', views.searchProductCategory, name='searchProductCategory'),
    path('searchProduct/<int:userId>/', views.searchProduct, name='searchProduct'),

]