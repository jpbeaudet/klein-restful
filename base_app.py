import json

from klein import Klein
from werkzeug.exceptions import MethodNotAllowed, NotFound


def getApp():
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
        invalid_path = request.path.decode('utf-8')
        return json.dumps({'error': 'Endpoint (%s) not found' % (invalid_path)})

    @app.handle_errors(MethodNotAllowed)
    def invalidMethod(request, failure):
        """
        Invalid method - 405
        """
        request.setResponseCode(405)
        method = request.method.decode('utf-8')
        endpoint = request.path.decode('utf-8')
        return json.dumps({'error': 'Invalid method call (%s) at %s endpoint' % (method, endpoint)})

    return app
