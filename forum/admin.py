from django.contrib import admin
from forum.models import OrdinaryUser, Messages
# Register your models here.  

admin.site.register(OrdinaryUser)
admin.site.register(Messages)

