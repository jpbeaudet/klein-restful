from twisted.internet import defer

from reusable import baseApp, JsonApi
from DB import HumanResourcesDatabase


app = baseApp()
json_api = JsonApi(app=app, secret='secret-v2')
hr_db = HumanResourcesDatabase(
    module_name='sqlite3',
    db_name='HR.sqlite',
    db_kwargs={'check_same_thread': False, 'cp_max': 10})


def getResource():
    return app.resource()


@json_api.route('/employees', methods=['GET'], restricted=True)
@defer.inlineCallbacks
def listEmployees(reqest):
    """
    Produce a set of all currently employed individuals in the company.
    """
    query = yield hr_db.getEmployees()
    records = []
    for index, record in enumerate(query):
        person = {}
        person['id'], person['lastname'], person['firstname'], person['title'] = record
        records.append(person)

        if index % 100 == 0:
            yield

    return records

@json_api.route('/employee', methods=['GET'], restricted=True)
def getEmployeeInfo(request):
    return '(v2) Get specific employee information'

@json_api.route('/positions', methods=['GET'], restricted=True)
@defer.inlineCallbacks
def listAllPositions(request):
    """
    Get the active positions in the company.
    """
    query = yield hr_db.getPositions()
    records = []
    for index, record in enumerate(query):
        position = {}
        position['id'], position['title'] = record
        records.append(position)

        if index % 100 == 0:
            yield

    return records

@json_api.route('/position', methods=['GET'], restricted=True)
def getPositionInfo(request):
    return '(v2) Get specific position info'

