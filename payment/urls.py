from django.urls import path
from .views import  home, success, failure
# https://realpython.com/django-redirects/
urlpatterns = [
    # path('pay/', initiate_payment, name='pay'),
    # path('callback/', callback, name='callback'),
    path('home/',home),
    path('success/',success),
    path('failure/',failure),
]

