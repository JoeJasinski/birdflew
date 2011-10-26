from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.cache import cache
from django.db.models import signals
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from django.contrib.auth.models import User

from bcore.models import UrlModel
from api import validators 
from api.views import BlankView, prepxml

from lxml import etree
from lxml.builder import ElementMaker 


users_list_cache_key = 'api_users_list'

class users_list(BlankView):
    
    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, *args, **kwargs):
        
        url_response = None #cache.get(users_list_cache_key)
        if not url_response:
            users = User.objects.all()
            E = ElementMaker()
            USERS = E.users
            USER = E.user
            USERNAME = E.username
            UUID = E.uuid
            status=200
            
            xml = USERS(*map(lambda x: USER(USERNAME(x.username), UUID('test')), users))
            url_response = prepxml(etree.tostring(xml), status)
            cache.set(users_list_cache_key, url_response, settings.DEFAULT_CACHE_TIMEOUT)

        return url_response


@receiver(signals.post_save, sender=User)
def del_api_lookupuurlsView(sender, instance, **kwargs):
    cache.delete(users_list_cache_key)


class users_detail(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, *args, **kwargs):
    
        form = RawUrlForm(data=request.raw_post_data)
        if form.is_valid():
            url_list = form.cleaned_data.get('urls')
            for u in url_list:
                url_model, created = UrlModel.objects.get_or_create(url=u,)
                
            num_added = len(url_list)
            xml = messagexml("Added %s Records" % (num_added))
        else:
            xml = messagexml('Error with form validation: %s' % form.errors)
            print form.errors
        
        status=201
        return prepxml(etree.tostring(xml), status)
