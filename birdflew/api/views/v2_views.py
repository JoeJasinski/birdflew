import uuid
from django.core.urlresolvers import reverse
from django.core import exceptions
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

from bcore.models import UrlModel, Category, Bookmark
from api import validators, forms
from api.views import (BlankView, prepxml, prepxhtml, messagexml, xml_to_xslt,
                       XMLEmitter, XHTMLEmitter)


from lxml import etree
from lxml.builder import ElementMaker 


users_list_cache_key = 'api_users_list'

def get_emitter(request, format=None):
    #return XMLEmitter()
    if format == 'xml':
        return XMLEmitter()
    else:
        return XHTMLEmitter()

class users_list(BlankView):
    
    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, *args, **kwargs):
        format = kwargs.get('format','')
        emitter = get_emitter(request, format)
        site = Site.objects.get_current()
        url_response = None #cache.get(users_list_cache_key)
        if not url_response:
            users = User.objects.all()
            E = ElementMaker()
            USERS = E.users
            USER = E.user
            NAME = E.name
            LINK = E.link
            A = E.a
            UUID = E.uuid
            status=200
            
            xml = USERS(*map(lambda x: USER(
                                        NAME(x.email), 
                                        LINK("http://%s%s" % (site.domain, reverse('api_users_detail', args=[x.email]),) )
                                        )
                             , users))
            
            
            if emitter.type == 'xhtml':
                xml = xml_to_xslt(xml=xml, template="api/v2_users_list.xslt", 
                                  context={'title':'Users List','heading':'Users List'})
                   
            url_response = emitter.run(etree.tostring(xml), status)
      
            cache.set(users_list_cache_key, url_response, settings.DEFAULT_CACHE_TIMEOUT)

        return url_response


    @method_decorator(validators.RateLimitDecorator)
    def post(self, request, *args, **kwargs):
        headers = {}
        emitter = get_emitter(request, 'xml')  
        form = forms.RawUserForm(data=request.raw_post_data)
        if form.is_valid():
            password = uuid.uuid4().hex
            username = form.cleaned_data.get('username')
            new_user = User.objects.create(username=username, 
                                           email=username,
                                           password=password)
            status = 201
            xml = messagexml("User Added", type="success")
        else:
            xml = messagexml('Error with form validation: %s' % form.errors)
            status = 500
            print form.errors

        return emitter.run(etree.tostring(xml), status, headers)
    

@receiver(signals.post_save, sender=User)
def del_api_lookupuurlsView(sender, instance, **kwargs):
    cache.delete(users_list_cache_key)


class users_detail(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, user, *args, **kwargs):
        format = kwargs.get('format','')
        emitter = get_emitter(request, format)    
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
            NODE = E.node
            URLS = E.urls
            xml = USER(EMAIL(user.email), 
                       NODE("http://%s" % site.domain),
                       URLS("http://%s%s" % (site.domain, reverse('api_users_bookmarks', args=[user.email,]))),
                       )
            status=201

        if emitter.type == 'xhtml':        
            xml = xml_to_xslt(xml=xml, template="api/v2_users_detail.xslt", 
                                  context={'title':'Users Detail','heading':'Users Detail'}) 
            
        return emitter.run(etree.tostring(xml), status)


class users_bookmarks(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, user, *args, **kwargs):
        format = kwargs.get('format','')
        emitter = get_emitter(request, format) 
        site = Site.objects.get_current()
        
        try:
            user = User.objects.get(email=user)
        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('Object does not exist')
            status=404
        else:
            url_list = user.user_bookmarks.all()
            E = ElementMaker()
            URLS = E.urls
            URL = E.url
            URI = E.uri
            BOOKMARK = E.bookmark
            ID = E.id
            status=200
            xml = URLS(*map(lambda x: URL(
                                          URI(x.get_absolute_url()), 
                                          BOOKMARK(x.url)), url_list))

            if emitter.type == 'xhtml': 
                xml = xml_to_xslt(xml=xml, template="api/v2_users_bookmarks.xslt", 
                          context={'title':'User URL List','heading':'User URL List'})
            
        return emitter.run(etree.tostring(xml), status)

    @method_decorator(csrf_exempt)
    @method_decorator(validators.RateLimitDecorator)
    def post(self, request, user, *args, **kwargs):
        headers = {}
        emitter = get_emitter(request, 'xml')  
        
        try:
            user = User.objects.get(email=user)
        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('User does not exist')
            status=404
            return prepxml(etree.tostring(xml), status)

        form = forms.RawBookmarkForm(data=request.raw_post_data)
        if form.is_valid():
            uri = form.cleaned_data.get('uri')
            new_categories = form.cleaned_data.get('categories')
            new_comments = form.cleaned_data.get('comments')
            
            bookmark_model, created = user.user_bookmarks.get_or_create(url=uri.url_socket, user=user)
            existing_categories = [c.category for c in bookmark_model.categories.all()]
            
            for new_category in new_categories:
        
                if new_category not in existing_categories:
                    category_obj, created = Category.objects.get_or_create(category__iexact=new_category,
                                            defaults={'category':new_category})
                    bookmark_model.categories.add(category_obj)
            #    bookmark_model, created = Bookmark.objects.get_or_create(url=u,)
            if new_comments:
                bookmark_model.bookmark_comments.all().delete()
                for new_comment in new_comments:
                    bookmark_model.bookmark_comments.create(comment=new_comment) 
            
            status = 201
            xml = messagexml("Bookmark Added", type="success")
            headers.update({'Location': bookmark_model.get_absolute_url() })
        else:
            xml = messagexml('Error with form validation: %s' % form.errors)
            status = 500
            print form.errors

        return emitter.run(etree.tostring(xml), status, headers)



class users_bookmark(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, user, url_id, *args, **kwargs):
        format = kwargs.get('format','')
        emitter = get_emitter(request, format)  
          
        try:
            user = User.objects.get(email=user)
        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('User does not exist')
            status=404
        else:
            try:
                bookmark = user.user_bookmarks.get(uuid=url_id)
                E = ElementMaker()
                URL = E.url
                DATE_ADDED = E.date_added
                SOURCE = E.source
                CATEGORIES = E.categories
                CAGEGORY = E.category
                COMMENTS = E.comments
                COMMENT = E.comment
                #DATE_ADDED = E.date_added #getattr(E, 'date-added')
                DATE_ADDED = getattr(E, 'date-added')
                status=200
                
                def CLASS(*args): # class is a reserved word in Python
                     return {"class":' '.join(args)}
                
                """
                xml = E.div(CLASS('url'), 
                        ABBR(CLASS("date-added"), title="%s" % bookmark.created.strftime('%Y-%m-%dT%H:%M:%S')), 
                        A(bookmark.url, rel="source", href=bookmark.url), 
                        UL(
                           LI(*map(lambda x: A(x.category, href=x.category, rel="category"), bookmark.category_set.all()))
                           ),
                        UL(
                           LI(*map(lambda x: A(x.comment, href=x.comment, rel="comments"), bookmark.comment_set.all()))
                           )
                        )
                """

                xml = URL(DATE_ADDED(bookmark.created.strftime('%Y-%m-%dT%H:%M:%S')),
                          SOURCE(bookmark.url),
                          CATEGORIES(*map(lambda x: CAGEGORY(x.category), bookmark.categories.all())),
                          COMMENTS(*map(lambda x: COMMENT(x.comment), bookmark.bookmark_comments.all())),
                          )

                if emitter.type == 'xhtml': 
                    xml = xml_to_xslt(xml=xml, template="api/v2_users_bookmark.xslt", 
                              context={'title':'URL Detail','heading':'URL Detail'})    
            except exceptions.ObjectDoesNotExist, e:
                xml = messagexml('Url does not exist')
                status=404
            
        return emitter.run(etree.tostring(xml), status)


class categories(BlankView):


    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, *args, **kwargs):
        format = kwargs.get('format','')
        emitter = get_emitter(request, format) 
        try:
            status = 200

            site = Site.objects.get_current()
            categories = Category.objects.all()
            
            E = ElementMaker()            
            CATEGORIES = E.categories
            CATEGORY = E.category
            URI = E.uri
            NAME = E.name
            
            xml = CATEGORIES(*map(lambda x:  CATEGORY(
                URI("http://%s%s" % ( site.domain, reverse('api_category', args=[x.category,]))), 
                NAME(x.category)
            ), categories))
            
            if emitter.type == 'xhtml': 
                xml = xml_to_xslt(xml=xml, template="api/v2_categories.xslt", 
                              context={'title':'Categories','heading':'Categories'}) 
        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('Category does not exist')
            status=404
        
        return emitter.run(etree.tostring(xml), status)
    

class category(BlankView):

    @method_decorator(validators.RateLimitDecorator)
    def get(self, request, category, *args, **kwargs):
        format = kwargs.get('format','')
        emitter = get_emitter(request, format)
        try:
            status = 200

            site = Site.objects.get_current()
            category = Category.objects.get(category=category)
            bookmarks = category.category_bookmarks.all()

        except exceptions.ObjectDoesNotExist, e:
            xml = messagexml('Category does not exist')
            status=404
        else:
            E = ElementMaker()
            URLS = E.urls
            URL = E.url
            URI = E.uri
            NAME = E.name
            LINK = E.link

            xml = URLS(*map(lambda b: URL(  URI(b.get_absolute_url()
                                    ), LINK(b.url)
                                ), bookmarks))
                          
            if emitter.type == 'xhtml': 
                xml = xml_to_xslt(xml=xml, template="api/v2_category.xslt", 
                              context={'title':'Category Bookmarks','heading':'Category Bookmarks'})
        
        return emitter.run(etree.tostring(xml), status)


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