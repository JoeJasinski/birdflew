from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UrlModel, Bookmark, UserInfo, Comment, Category

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 0

class UrlModelAdmin(MPTTModelAdmin):
    list_display = ['url','parent','created','modified']
    readonly_fields = ['uuid',]

admin.site.register(UrlModel, UrlModelAdmin)

class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)

class BookmarkAdmin(MPTTModelAdmin):
    list_display = ['url','user','parent','created','modified']
    inlines = [CommentInline, ]
    readonly_fields = ['uuid',]

admin.site.register(Bookmark, BookmarkAdmin)


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    extra = 0


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('date_joined','last_login')
    list_filter = UserAdmin.list_filter + ('is_active',)
    inlines = [UserInfoInline,]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
