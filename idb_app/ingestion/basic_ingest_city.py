from idb_app.models import City, choices
from idb_app.mongo import Connector
import requests
import re

# standalone script to ingest City data into Mongo
# note that repeated runs (without clearing DB) may fail due to uniqueness constraints

# requires that you have a .env file with a mongo DB user/password
Connector.load_database_creds()

Connector.connect_test_database()

example_cities = [
    {
        "name": "austin",
        "state": choices.STATE_TEXAS,
        "area": 579.4,
        "population": 950715,
        "population_density": 3780,
        "community_type": "City",
        "median_age": 33.4,
        "median_gross_rent": 1244,
    },
    {
        "name": "houston",
        "state": choices.STATE_TEXAS,
        "area": 251.5,
        "population": 2312717,
        "population_density": 3991,
        "community_type": "City",
        "median_age": 33.1,
        "median_gross_rent": 986,
    },
    {
        "name": "cambridge",
        "state": choices.STATE_MASSACHUSETTS,
        "area": 6.43,
        "population": 113630,
        "population_density": 17.675,
        "community_type": "City",
        "median_age": 30.5,
        "median_gross_rent": 2102,
    },
]

# example insertion
# could also init with m = City(name="x", field2=y, ...)
for city in example_cities:
    c = City(**city)
    c.save()

c = City.objects().limit(3)
base_url = "http://api.wolframalpha.com/v2/query?appid=38LR3Q-5V34V3KX75"

# example query
# for city in c:
#     r = requests.get(base_url + "&input=" + city["name"] + "+" + city["state"] + "&output=json")
#     json_res = r.json()
#     test1 = json_res["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
#     test2 = json_res["queryresult"]["pods"][16]["subpods"][0]["plaintext"]
#     print(re.findall("\d+", test1)[0])
#     print(re.findall("\d+", test2)[1])
#     print(re.findall("\d+", test2)[2])

# test1 = "city population | 113630 people (country rank: ≈262nd) (2017 estimate)\nurban area population | 4.032 million people (Boston urban area) (country rank: 7th) (2000 estimate)\nmetro area population | 4.591 million people (Boston metro area) (country rank: 10th) (2011 estimate)"
# print(re.findall("\d+", test1)[0])
# test2 = "elevation | 16 ft\narea | 6.3854 mi^2\npopulation density | 17795 people per square mile"
# print(re.findall("\d+\.\d+", test2)[0])
# print(re.findall("\d+\d+", test2)[2])

for city in c:
    r = requests.get(base_url + "&input=" + city["name"] + "+" + city["state"] + "&output=json")
    json_res = r.json()
    for p in json_res["queryresult"]["pods"]:
        if p["title"] == "Populations":

        elif p["title"] == "Geographic properties":

        else:
            continue
Connector.disconnect_database()
