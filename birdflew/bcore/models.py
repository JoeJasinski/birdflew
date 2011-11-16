import urllib2, socket, threading
from mptt.models import MPTTModel
from django.db import models
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django_extensions.db.fields import UUIDField
from django.dispatch import receiver
from django.db.models import signals
from api import validators

from lxml import etree
from lxml.builder import ElementMaker 

class TrackingMixin(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Comment(TrackingMixin):
    bookmark = models.ForeignKey('bcore.Bookmark', related_name='bookmark_comments')
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
    
    def get_absolute_url(self):
        site = Site.objects.get_current()
        return "http://%s%s" % (site.domain, 
            reverse('api_users_bookmark', args=[self.user.email, self.uuid]))
    
    
class UserInfo(models.Model):
    
    user = models.ForeignKey('auth.User', unique=True)
    uuid = UUIDField(version=1)        
    
User.profile = property(lambda u: UserInfo.objects.get_or_create(user=u)[0])  


class Subscriber(TrackingMixin, models.Model):

    user = models.ForeignKey('auth.User', blank=True, null=True, related_name='user_subscriptions')
    callback_url = models.CharField(max_length=255,)
    uuid = UUIDField(version=1)

    def __unicode__(self):
        return "%s - %s" % (self.uuid, self.callback_url)

   
def notify_subscribers_thread(user, xml, **kwargs):   

    for subscriber in Subscriber.objects.filter(user=user):

        request = urllib2.Request(subscriber.callback_url, data=etree.tostring(xml, pretty_print=True ))
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            pass
        except urllib2.URLError, e:
            pass


       
@receiver(signals.post_save, sender=Bookmark)
def notify_subscribers(sender, instance, **kwargs):
    user = instance.user
    bookmark = instance

    timeout = 10
    socket.setdefaulttimeout(timeout)

    E = ElementMaker()
    NOTICE = E.notice
    SUBSCRIPTION = E.subscription
    UPDATE = E.update
    xml = NOTICE(SUBSCRIPTION(user.get_absolute_url_full()), UPDATE(bookmark.get_absolute_url()))
    
    t = threading.Thread(target=notify_subscribers_thread,
                         args=[user, xml])


class Notification(TrackingMixin, models.Model):   
    
    user = models.ForeignKey('auth.User')
    subscription = models.CharField(u'Remote Subscription', max_length=255)
    bookmark = models.CharField(u'Updated Bookmark', max_length=255)

    def __unicode__(self):
        return "%s" % (self.subscription,)
       