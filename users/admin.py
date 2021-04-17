from django.contrib import admin
from .models import SiteUsers, Roles, UserAddress, States, Countries

admin.site.register(Roles)
admin.site.register(SiteUsers)
admin.site.register(UserAddress)
admin.site.register(States)
admin.site.register(Countries)