from base_app import getApp
from v1 import app as v1_app
from v2 import app as v2_app


main = getApp()


@main.route('/v1', branch=True)
def version_1(request):
    return v1_app.getResource()

@main.route('/v2', branch=True)
def version_2(request):
    return v2_app.getResource()


main.run('localhost', 9999)
