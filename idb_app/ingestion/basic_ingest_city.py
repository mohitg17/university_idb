from idb_app.models import City, choices
from idb_app.mongo import Connector

# standalone script to ingest City data into Mongo
# note that repeated runs (without clearing DB) may fail due to uniqueness constraints

# requires that you have a .env file with a mongo DB user/password
Connector.load_database_creds()

Connector.connect_prod_database()

example_cities = [
    {
        "name": "austin",
        "state": choices.STATE_TEXAS,
        "area": 579.4,
        "population": 950715,
        "population_density": 3780,
        "community_type": "Urban",
        "median_age": 33.4,
        "median_gross_rent": 1244,
    },
    {
        "name": "houston",
        "state": choices.STATE_TEXAS,
        "area": 251.5,
        "population": 2312717,
        "population_density": 3991,
        "community_type": "Urban",
        "median_age": 33.1,
        "median_gross_rent": 986,
    },
    {
        "name": "cambridge",
        "state": choices.STATE_MASSACHUSETTS,
        "area": 6.43,
        "population": 113630,
        "population_density": 17.675,
        "community_type": "Urban",
        "median_age": 30.5,
        "median_gross_rent": 2102,
    },
]

# example insertion
# could also init with m = City(name="x", field2=y, ...)
for city in example_cities:
    c = City(**city)
    c.save()

# example query
for city in example_cities:
    city_from_db = City.objects(name=city["name"]).first()
    assert city_from_db.name == city["name"]

Connector.disconnect_database()
