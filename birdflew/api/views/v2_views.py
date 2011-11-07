from django.core.urlresolvers import reverse
from django.core import exceptions
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.db.models import signals
from django.dispatch import receiver
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


from django.contrib.auth.models import User

from bcore.models import UrlModel, Category
from api import validators 
from api.views import BlankView, prepxml, messagexml

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
            A = E.a
            UUID = E.uuid
            status=200
            
            xml = USERS(*map(lambda x: USER(x.email), users))
            #xml = USERS(*map(lambda x: A(href=reverse('api_users_detail',args=[x.email]), rel=x.email), users))
            url_response = prepxml(etree.tostring(xml), status)
            cache.set(users_list_cache_key, url_response, settings.DEFAULT_CACHE_TIMEOUT)

        return url_response


@receiver(signals.post_save, sender=User)
def del_api_lookupuurlsView(sender, instance, **kwargs):
    cache.delete(users_list_cache_key)


class users_detail(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, user, *args, **kwargs):
    
        try:
            user = User.objects.get(email=user)
        except exceptions.ObjectDoesNotExist, e:
             xml = messagexml('Object does not exist')
             status=404
        else:
            site = Site.objects.get_current()
            E = ElementMaker()
            USER = E.user
            EMAIL = E.email
            URL = E.url
            xml = USER(EMAIL(user.email), URL("http://%s" % site.domain))
            status=201
            
        return prepxml(etree.tostring(xml), status)


class users_urls(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, user, *args, **kwargs):
    
        try:
            user = User.objects.get(email=user)
        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('Object does not exist')
            status=404
        else:
            url_list = user.user_urls.all()
            E = ElementMaker()
            URLS = E.urls
            URL = E.url
            URI = E.uri
            ID = E.id
            status=200
            xml = URLS(*map(lambda x: URL(URI(x.url), ID(x.uuid)), url_list))
            
        return prepxml(etree.tostring(xml), status)


class users_url(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, user, url_id, *args, **kwargs):
    
        try:
            user = User.objects.get(email=user)
        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('User does not exist')
            status=404
        else:
            try:
                url = user.user_urls.get(uuid=url_id)
                E = ElementMaker()
                URL = E.url
                URI = E.uri
                ID = E.id
                ABBR = E.abbr
                A = E.a
                UL = E.ul
                LI = E.li
                status=200
                
                def CLASS(*args): # class is a reserved word in Python
                     return {"class":' '.join(args)}
                
                xml = E.div(CLASS('url'), 
                        ABBR(CLASS("date-added"), title="%s" % url.created.strftime('%Y-%m-%dT%H:%M:%S')), 
                        A(url.url, rel="source", href=url.url), 
                        UL(LI(*map(lambda x: A(x.category, href=x.category, rel="category"), url.category_set.all()))))
            except exceptions.ObjectDoesNotExist, e:
                xml = messagexml('Url does not exist')
                status=404
            
        return prepxml(etree.tostring(xml), status)


class categories(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, *args, **kwargs):

        try:
            
            def CLASS(*args): # class is a reserved word in Python
                 return {"class":' '.join(args)}

            site = Site.objects.get_current()
            E = ElementMaker()
            status = 200
            
            categories = Category.objects.all()
            xml = E.div(*map(lambda x: E.a(x.category, CLASS('category'), href="http://%s%s" % (
                    site.domain, reverse('api_category', args=[x.category,]))), categories))
        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('Category does not exist')
            status=404
        
        return prepxml(etree.tostring(xml), status)
    

class category(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, category, *args, **kwargs):

        try:
            def CLASS(*args): # class is a reserved word in Python
                 return {"class":' '.join(args)}

            site = Site.objects.get_current()
            E = ElementMaker()
            status = 200
            
            category = Category.objects.get(category=category)
            xml = E.div(E.a(category.category, CLASS('category'), href="http://%s%s" % (
                    site.domain, reverse('api_category', args=[category.category,]))))
        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('Category does not exist')
            status=404
        
        return prepxml(etree.tostring(xml), status)


    """
    /v2/users/{alice}/urls/{5}/categories/
    GET <categories>
           <category></category>
           ...
        </categories
        
    PUT - same xml document 
    
    
    def post(self, request, user, *args, **kwargs):
        POST THIS
        <url>
          <url>http://www.google.com</url>
          <categories>
            <category></category>?
          </categories>
          <comments>
            <comment></comment>?
          </comments>
        <urls>
        RETURN THIS 
        - 201 Created
    """

"""
class user_subscriptions(self, request, user, *args, **kwargs):
    8:15 - 8:30+  10/31/2011
    - add a subscription
      - give callback URL
    - remove subscription 
      -  
"""