from django.db import models
from django.core.cache import cache

class TrackingMixin(models.Model):

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UrlModel(TrackingMixin):
    
    url = models.CharField(max_length=255)
    
    def __unicode__(self):
        return self.url


    class Meta:
        ordering = ('url', 'created', )
