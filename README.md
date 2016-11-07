# Design

## HTTP Routes

| Method | URI | Action |
| --- | --- | --- |
| GET | /positions | Get all position records. |
| POST | /position | Add a position record. |
| DELETE | /position | Deactivate a position. |
| GET | /person | Get all employee records. |
| POST | /person | Add a person record. |
| DELETE | /person | Fire a person! |


## DB Tables

people

| Field | Type |
| --- | --- |
| \_id_ (PRIMARY KEY) | TEXT |
| email | TEXT |
| firstname | TEXT |
| lastname | TEXT |
| gender | TEXT |
| dob | DATE |
| address | TEXT |
| ssn (UNIQUE) | TEXT |


positions

| Field | Type |
| --- | --- |
| \_id_ (PRIMARY KEY) | TEXT |
| title | TEXT |
| status | INT |


jobs

| Field | Type | Constraints |
| --- | --- | --- |
| person_id (PRIMARY KEY) | TEXT | FOREIGN KEY (person_id) REFERENCES people (\_id_) |
| title_id | TEXT | FOREIGN KEY (title_id) REFERENCES positions (\_id_)


