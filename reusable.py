from functools import wraps
import json

from klein import Klein
from twisted.internet import defer
from werkzeug.exceptions import MethodNotAllowed, NotFound


def baseApp():
    """
    Factory function that produces a base Klein object with default configurations.

    :return: Klein object
    """
    app = Klein()

    @app.handle_errors(NotFound)
    def routeNotFound(request, failure):
        """
        Endpoint not found - 404
        """
        request.setResponseCode(404)
        request.setHeader('Content-Type', 'application/json')
        invalid_path = request.path.decode('utf-8')
        return json.dumps({'error': 'Endpoint (%s) not found' % (invalid_path)})

    @app.handle_errors(MethodNotAllowed)
    def invalidMethod(request, failure):
        """
        Invalid method - 405
        """
        request.setResponseCode(405)
        request.setHeader('Content-Type', 'application/json')
        method = request.method.decode('utf-8')
        endpoint = request.path.decode('utf-8')
        return json.dumps({'error': 'Invalid method call (%s) at %s endpoint' % (method, endpoint)})

    return app


class JsonApi(object):
    """
    Reusable class for composing a JSON API easily with minimal
    repeated code.
    """

    def __init__(self, app=None, secret='twisted'):
        self.app = app if app else Klein()
        self.secret = secret

    def jsonMiddleware(self, f):
        """
        Middleware to set application/json as default header for
        all responses.
        """
        @wraps(f)
        def deco(*args, **kwargs):
            request = args[0]
            request.setHeader('Content-Type', 'application/json')
            result = defer.maybeDeferred(f, *args, **kwargs)
            result.addCallback(json.dumps)
            return result

        return deco

    def authenticate(self, f):
        """
        Middleware api-key authentication
        """
        @wraps(f)
        def deco(*args, **kwargs):
            request = args[0]
            apiKey = request.getHeader('Authorization')
            if not apiKey or apiKey != self.secret:
                request.setResponseCode(401)
                body = {
                    'scope': 'private',
                    'message': 'Sorry, valid credentials required to access content'}
                return body
            return f(*args, **kwargs)

        return deco

    def route(self, url, *args, **kwargs):
        """
        Extend the route functionality
        """
        def deco(f):
            restricted = kwargs.pop('restricted', False)
            if restricted:
                f = self.authenticate(f)
            f = self.jsonMiddleware(f)
            self.app.route(url, *args, **kwargs)(f)
        return deco

