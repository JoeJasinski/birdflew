from django.contrib import admin
from .models import UrlModel

class UrlModelAdmin(admin.ModelAdmin):
    list_display = ['url','created','modified']
    

admin.site.register(UrlModel, UrlModelAdmin)