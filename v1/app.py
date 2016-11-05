from reusable import baseApp


app = baseApp()

def getResource():
    return app.resource()

@app.route('/employees', methods=['GET'])
def listEmployees(reqest):
    return 'List all employees'

@app.route('/employee', methods=['GET'])
def getEmployeeInfo(request):
    return 'Get specific employee information'

@app.route('/positions', methods=['GET'])
def listAllPositions(request):
    return 'List all positions within the company'

@app.route('/position', methods=['GET'])
def getPositionInfo(request):
    return 'Get specific position info'

