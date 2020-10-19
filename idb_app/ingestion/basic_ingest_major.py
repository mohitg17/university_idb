from idb_app.models import Major
from idb_app.mongo import Connector

# standalone script to ingest Major data into Mongo
# note that repeated runs (without clearing DB) will fail because we are forcing major names to be unique

# requires that you have a .env file with a mongo DB user/password
Connector.load_database_creds()

Connector.connect_prod_database()

example_majors = [
    {
        "name": "education",
        "median_starting_salary": 34900,
        "median_midcareer_salary": 52000,
        "num_certificate_programs": 376,
        "num_associate_programs": 696,
        "num_bachelor_programs": 1169,
    },
    {
        "name": "history",
        "median_starting_salary": 39200,
        "median_midcareer_salary": 71000,
        "num_certificate_programs": 21,
        "num_associate_programs": 185,
        "num_bachelor_programs": 1233,
    },
    {
        "name": "engineering",
        "median_starting_salary": 58957,
        "median_midcareer_salary": 99257,
        "num_certificate_programs": 95,
        "num_associate_programs": 464,
        "num_bachelor_programs": 619,
    },
]


# example insertion
# could also init with m = Major(name="x", median_starting_salary=y, ...)
for major in example_majors:
    m = Major(**major)
    m.save()

# example query
for major in example_majors:
    major_from_db = Major.objects(name=major["name"]).first()
    assert major_from_db.name == major["name"]
    assert major_from_db.median_starting_salary == major["median_starting_salary"]
    assert major_from_db.num_bachelor_programs == major["num_bachelor_programs"]


Connector.disconnect_database()
