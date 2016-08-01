import json

from klein import Klein
from werkzeug.exceptions import NotFound


def getApp():
    """
    Factory function that produces a base Klein object with default configurations.

    :return: Klein object
    """
    app = Klein()

    @app.handle_errors(NotFound)
    def routeNotFound(request, failure):
        request.setResponseCode(404)
        return json.dumps({'error': 'Invalid endpoint %s' % (request.path)})

    return app
