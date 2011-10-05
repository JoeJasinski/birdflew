from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import UrlModel

class UrlModelAdmin(MPTTModelAdmin):
    list_display = ['url','created','modified']
    

admin.site.register(UrlModel, UrlModelAdmin)