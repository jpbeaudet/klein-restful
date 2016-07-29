from csv import reader as CSVReader
from sys import argv
from datetime import datetime

from twisted.internet import reactor
from twisted.enterprise.adbapi import ConnectionPool


def unixTime(dt):
    """
    :param dt: datetime.
    :return: Epoch time as int.
    """
    return int((dt - datetime(1970, 1, 1)).total_seconds())

def uhh(filename):
    rows = []
    with open(filename) as f:
        for i, row in enumerate(CSVReader(f)):
            if i == 0:
                continue
            row[0] = unixTime(datetime.strptime(row[0], '%Y-%m-%d'))
            if row[21] != '':
                row[21] = row[21].split('-')
            else:
                row[21] = []
            rows.append(row)

def createdb(cursor, tablename):
    schema = 'CREATE TABLE {0}' \
        '(Date INTEGER PRIMARY KEY,' \
        'MaxTemperatureF INTEGER,' \
        'MeanTemperatureF INTEGER,' \
        'MinTemperatureF INTEGER,' \
        'MaxDewPointF INTEGER,' \
        'MeanDewPointF INTEGER,' \
        'MinDewpointF INTEGER,' \
        'MaxHumidity INTEGER,' \
        'MeanHumidity INTEGER,' \
        'MinHumidity INTEGER,' \
        'MaxSeaLevelPressureIn FLOAT,' \
        'MeanSeaLevelPressureIn FLOAT,' \
        'MinSeaLevelPressureIn FLOAT,' \
        'MaxVisibilityMiles INTEGER,' \
        'MeanVisibilityMiles INTEGER,' \
        'MinVisibilityMiles INTEGER,' \
        'MaxWindSpeedMPH INTEGER,' \
        'MeanWindSpeedMPH INTEGER,' \
        'MaxGustSpeedMPH INTEGER,' \
        'PrecipitationIn FLOAT,' \
        'CloudCover INTEGER,' \
        'Events TEXT,' \
        'WindDirDegrees INTEGER)'
    cursor.execute(schema.format(tablename))

if __name__ == '__main__':
    dbpool = ConnectionPool('sqlite3', 'Weather.sqlite3')
    dbpool.runInteraction(createdb, 'DCA_2015')
    # uhh(argv[1])
    reactor.run()
