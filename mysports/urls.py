from django.contrib import admin
from django.urls import path

from mysports import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('detail/<int:id>', views.details, name='detail'),
    path('checkout/', views.checkout,name='checkOut'),
    path('showCart/', views.showCart,name='showCart'),
    path('repeatTheOrder/<int:id>/', views.repeatTheOrder,name='showCart'),

]
