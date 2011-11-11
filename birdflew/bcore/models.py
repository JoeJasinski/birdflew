from mptt.models import MPTTModel
from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField
from api import validators

class TrackingMixin(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Comment(TrackingMixin):
    bookmark = models.ForeignKey('bcore.Bookmark')
    comment = models.TextField()
 
 
class Category(TrackingMixin):

    category = models.CharField(max_length=20) 
   
    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = "Categories"

    def __unicode__(self):
        return self.category

class UrlModel(MPTTModel, TrackingMixin):
    
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    url = models.CharField(max_length=255,)
    uuid = UUIDField(version=1)
    
    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        burl, messages = validators.validate_url_format(self.url)
        self.url = burl.url_socket
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ('url', 'created', )

    def get_errorcount(self):
        count = cache.get("error_count_url_%s" % self.id, 0)
        return count
            
    def get_errormessage(self):
        messages = cache.get("error_message_url_%s" % self.id, '')
        return messages


class Bookmark(MPTTModel, TrackingMixin):
    
    user = models.ForeignKey('auth.User', blank=True, null=True, related_name='user_bookmarks')
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    url = models.CharField(max_length=255,)
    uuid = UUIDField(version=1)
    categories = models.ManyToManyField('bcore.Category', related_name='category_bookmarks', blank=True, null=True)
    
    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        burl, messages = validators.validate_url_format(self.url)
        self.url = burl.url_socket
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ('url', 'created', )

    def get_errorcount(self):
        count = cache.get("error_count_url_%s" % self.id, 0)
        return count
            
    def get_errormessage(self):
        messages = cache.get("error_message_url_%s" % self.id, '')
        return messages
    
class UserInfo(models.Model):
    
    user = models.ForeignKey('auth.User', unique=True)
    uuid = UUIDField(version=1)        
    
User.profile = property(lambda u: UserInfo.objects.get_or_create(user=u)[0])          