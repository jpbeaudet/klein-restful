from base_app import getApp


app = getApp()

def getResource():
    return app.resource()

@app.route('/employees', methods=['GET'])
def listEmployees(reqest):
    return '(v2) List all employees'

@app.route('/employee', methods=['GET'])
def getEmployeeInfo(request):
    return '(v2) Get specific employee information'

@app.route('/positions', methods=['GET'])
def listAllPositions(request):
    return '(v2) List all positions within the company'

@app.route('/position', methods=['GET'])
def getPositionInfo(request):
    return '(v2) Get specific position info'

