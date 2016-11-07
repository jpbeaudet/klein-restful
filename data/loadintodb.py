import imp
from os import path, getcwd
from random import choice
from string import ascii_letters

from faker import Faker
from twisted.internet import task, defer

# stupid hack need to find better solution
DB = imp.load_source('DB', path.join(getcwd(), 'DB.py'))
HumanResourcesDatabase = DB.HumanResourcesDatabase

def genID(faker):
    letter = choice(ascii_letters).lower()
    card_types = ['discover', 'amex', 'visa', 'mastercard']
    first = faker.credit_card_security_code(card_type=choice(card_types))
    second = faker.credit_card_number(card_type=choice(card_types))
    return '%s%s-%s' % (letter, first, second)

def genName(faker, gender):
    if gender.lower() == 'female':
        first = faker.first_name_female()
    else:
        first = faker.first_name_male()
    return '%s %s' % (first, faker.last_name())

def genBirthday(faker, start='-70y', end='-18y'):
    return faker.date_time_between(start_date=start, end_date=end)

def genAddress(faker):
    return faker.address().replace('\n', ' ')

def genPeople(faker, gender, n=50):
    """
    """
    for x in range(n):
        person = {}
        person['_id_'] = genID(faker)
        person['email'] = faker.email()
        person['firstname'], person['lastname'] = genName(faker, gender).split(' ')
        person['gender'] = gender
        person['dob'] = genBirthday(faker)
        person['address'] = genAddress(faker)
        person['ssn'] = faker.ssn()
        yield person

def genPositions(faker, n=50):
    for x in range(n):
        positions = {}
        positions['_id_'] = choice(ascii_letters).upper() + faker.ean(length=choice([8, 13]))
        positions['title'] = faker.job()
        yield positions

def genJobTitles(people, position_titles):
    for person in people:
        job = {}
        job['title_id'] = choice(position_titles)
        job['person_id'] = person['id']
        yield job

@defer.inlineCallbacks
def main(reactor):
    # generate db
    hr_db = HumanResourcesDatabase(module_name='sqlite3', db_name='HR.sqlite', db_kwargs={'check_same_thread': False, 'cp_max': 10})
    yield hr_db.createTables()

    # populate db
    faker = Faker()
    title_ids = []
    person_ids = []

    for position in genPositions(faker, n=30):
        fields = []     # store fields
        values = []     # store values
        for key, val in position.items():
            fields.append(key)
            values.append(val)
        title_ids.append(position['_id_'])      # store position id for later

        # insert into the db sequentially
        yield hr_db.insert(
            table='positions',
            fields=fields,
            values=values)

    for gender in ['male', 'female']:
        num_of_ppl = 100
        for person in genPeople(faker, gender, num_of_ppl):
            fields = []
            values = []
            for key, val in person.items():
                fields.append(key)
                values.append(val)
            person_ids.append(person['_id_'])

            yield hr_db.insert(
                table='people',
                fields=fields,
                values=values)

    for person_id in person_ids:
        fields = ['title_id', 'person_id', 'status']
        values = [
            choice(title_ids),
            person_id,
            choice([0, 1, 1, 1, 1])]    # decrease chances of setting 0
        yield hr_db.insert(
            table='jobs',
            fields=fields,
            values=values)

if __name__ == '__main__':
    task.react(main)

