from mptt.models import MPTTModel
from django.db import models
from django.core.cache import cache
from api import validators

class TrackingMixin(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UrlModel(MPTTModel, TrackingMixin):
    
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    url = models.CharField(max_length=255,)
    
    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        burl, messages = validators.validate_url_format(self.url)
        self.url = burl.url_socket
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ('url', 'created', )
