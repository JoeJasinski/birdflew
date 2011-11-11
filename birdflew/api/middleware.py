# author: http://djangosnippets.org/snippets/708/
import new

def accepts( self, mime ):
    return mime in self.accepted_types

class AcceptMiddleware(object):
    def process_request(self, request):
        acc = [a.split(';')[0] for a in request.META.get('HTTP_ACCEPT','').split(',')]
        setattr(request, 'accepted_types', acc )
        request.accepts = new.instancemethod(accepts, request, request.__class__)
        return None