from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UrlModel, Bookmark, UserInfo, Comment, Category, Subscriber, Notification

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

class BookmarkInline(admin.StackedInline):
    model = Bookmark
    extra = 0

class BookmarkAdmin(MPTTModelAdmin):
    list_display = ['url','user','parent','created','modified']
    inlines = [CommentInline, ]
    readonly_fields = ['uuid',]

admin.site.register(Bookmark, BookmarkAdmin)


class UserInfoInline(admin.StackedInline):
    model = UserInfo
    extra = 0


class SubscriberInline(admin.StackedInline):
    model = Subscriber
    extra = 0

class SubscriberAdmin(admin.ModelAdmin):
    pass

admin.site.register(Subscriber, SubscriberAdmin)


class NotificationAdmin(admin.ModelAdmin):
    readonly_fields = ['created','modified']
    list_display = ['bookmark','created','modified']

admin.site.register(Notification, NotificationAdmin)


class CustomUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('date_joined','last_login')
    list_filter = UserAdmin.list_filter + ('is_active',)
    inlines = [UserInfoInline,BookmarkInline,SubscriberInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)