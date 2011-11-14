from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

class UserFunctions:
    """
    Monkeypatch the user to add extra functions
    """

    def get_absolute_url_full(self):
        site = Site.objects.get_current()
        
        return "http://%s%s" % (site.domain, reverse('api_users_detail', args=[self.email]),) 


User.__bases__ += (UserFunctions,)
