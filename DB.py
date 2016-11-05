from __future__ import unicode_literals

import attr
from twisted.internet import defer
from twisted.enterprise.adbapi import ConnectionPool

@attr.s
class HumanResourcesDatabase(object):
    module_name = attr.ib()
    db_name = attr.ib()
    db_args = attr.ib(default=attr.Factory(list))
    db_kwargs = attr.ib(default=attr.Factory(dict))
    _connection = attr.ib(default=None)

    @property
    def connection_pool(self):
        if not self._connection:
            self._connection = ConnectionPool(
                self.module_name,
                self.db_name,
                *self.db_args,
                **self.db_kwargs)
        return self._connection

    def _createPerson(self, cursor):
        create_people = 'CREATE TABLE people ('\
            '_id_ TEXT PRIMARY KEY,'\
            'email TEXT,'\
            'firstname TEXT,'\
            'lastname TEXT,'\
            'gender TEXT,'\
            'dob DATE,'\
            'address TEXT,'\
            'ssn TEXT UNIQUE'\
            ')'
        cursor.execute(create_people)

    def _createPositions(self, cursor):
        create_positions = 'CREATE TABLE positions ('\
            '_id_ TEXT PRIMARY KEY,'\
            'title TEXT'\
            ')'
        cursor.execute(create_positions)

    def _createJobs(self, cursor):
        create_job = 'CREATE TABLE jobs ('\
            'person_id TEXT PRIMARY KEY,'\
            'title_id TEXT,'\
            'FOREIGN KEY (person_id) REFERENCES people (_id_),'\
            'FOREIGN KEY (title_id) REFERENCES positions (_id_)'\
            ')'
        cursor.execute(create_job)

    @defer.inlineCallbacks
    def createTables(self):
        yield self.connection_pool.runInteraction(self._createPerson)
        yield self.connection_pool.runInteraction(self._createPositions)
        yield self.connection_pool.runInteraction(self._createJobs)

    def _insert(self, cursor, table, fields, values):
        fields = ','.join(['"%s"' % (x) for x in fields])
        values = ','.join(['"%s"' % (x) for x in values])
        insert_stmt = 'INSERT INTO %s' \
            '(%s)' \
            'VALUES (%s)' % (table, fields, values)
        cursor.execute(insert_stmt)

    def insert(self, table, fields, values):
        """
        """
        return self.connection_pool.runInteraction(self._insert, table, fields, values)

    @defer.inlineCallbacks
    def getPeopleRecords(self):
        stmt = "SELECT jobs.person_id, people.lastname, people.firstname, positions.title"\
            " FROM people"\
            " JOIN jobs ON jobs.person_id=people._id_"\
            " JOIN positions ON positions._id_=jobs.title_id"\
            " ORDER BY people.lastname ASC"
        result = yield self.connection_pool.runQuery(stmt)
        defer.returnValue(result)
