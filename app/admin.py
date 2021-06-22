from django.contrib import admin

# Register your models here.
from django.apps import apps


from .models import *

admin.site.register(Customer)
admin.site.register(Adress)
admin.site.register(Product)
admin.site.register(Cart) 