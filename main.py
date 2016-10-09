from base_app import getApp
from v1 import app as v1_app
from v2 import app as v2_app


mainApp = getApp()

@mainApp.route('/v1', branch=True)
def version_1(request):
    return v1_app.getResource()

@mainApp.route('/v2', branch=True)
def version_2(request):
    return v2_app.getResource()

@mainApp.route('/hr', branch=True)
def humanResources(request):
    header = request.getHeader('Content-Type')
    if header == 'application/json/2.1':
        return v2_app.getResource()
    else:
        return v1_app.getResource()


if __name__ == '__main__':
    from twisted.python.usage import Options
    class CliArgs(Options):
        optParameters = [
            ['host', 'H', 'localhost', 'Hostname'],
            ['port', 'P', 8000, 'Port number', int],
            ['log', 'L', None, 'Log file path'],
            ]

    options = CliArgs()
    options.parseOptions()
    
    host = options['host']
    port = options['port']
    logFile = options['log']
    if logFile:
        logFile = open(logFile, 'a')

    mainApp.run(host=host, port=port, logFile=logFile)
