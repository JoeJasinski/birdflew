from piston.handler import AnonymousBaseHandler, BaseHandler

from piston.handler import PistonView, Field


class IPsView(PistonView):
    fields = [
            Field('', lambda x: x, destination='ips'),
            ]


class LookupURLsHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        ips = {'ips':['10.0.0.1', '10.0.0.2', '10.0.0.3']}

        return IPsView(ips)


class RegisterURLsHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        return {'test':'test'}


class WhoamiHandler(BaseHandler):
    methods_allowed = ('GET',)

    def read(self, request):
        return {'test':'test'}


