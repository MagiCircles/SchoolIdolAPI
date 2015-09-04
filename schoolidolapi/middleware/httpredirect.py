from django.http import HttpResponseRedirect
from web.utils import HttpRedirectException

class HttpRedirectMiddleware(object):
    def process_exception(self, request, exception):
        if isinstance(exception, HttpRedirectException):
            return HttpResponseRedirect(exception.args[0])
