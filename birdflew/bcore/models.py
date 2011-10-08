from mptt.models import MPTTModel
from django.db import models
from django.core.cache import cache

class TrackingMixin(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UrlModel(MPTTModel, TrackingMixin):
    
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    url = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        self.url = self.url.rstrip("/")
        super(self.__class__, self).save(*args, **kwargs)

    class Meta:
        ordering = ('url', 'created', )
