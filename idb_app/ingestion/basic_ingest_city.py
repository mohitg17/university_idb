from idb_app.models import City, choices
from idb_app.mongo import Connector
from bs4 import BeautifulSoup
import requests
import re

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
# for city in example_cities:
#     c = City(**city)
#     c.save()

c = City.objects(area=1000000)

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


# def format_nums(stat):
#     try:
#         if stat[0].__contains__("."):
#             if stat[1] == "million":
#                 return int(float(stat[0]) * 1000000)
#             else:
#                 return float(stat[0])
#         else:
#             return int(stat[0])
#     except ValueError:
#         return 0


# for city in c:
#     print(city["name"] + ", " + city["state"])
#     r = requests.get(
#         base_url + "&input=" + city["name"] + "+" + city["state"] + "&output=json"
#     )
#     json_res = r.json()
#     if json_res["queryresult"]["success"] == False:
#         continue
#     for p in json_res["queryresult"]["pods"]:
#         if p["title"] == "Populations" or p["title"] == "Population":
#             population_data = p["subpods"][0]["plaintext"]
#             # find population from list and save
#             temp_pop = format_nums(
#                 population_data.split("|")[1].lstrip(" ").split(" ")[:2]
#             )
#             if temp_pop != 0:
#                 city["population"] = temp_pop
#                 city.save()
#         elif p["title"] == "Geographic properties":
#             area_data = p["subpods"][0]["plaintext"]
#             density_data = p["subpods"][0]["plaintext"]
#             # find area and density from list and save
#             if len(area_data.split("|")) < 3:
#                 temp_area = 0
#             else:
#                 temp_area = format_nums(
#                     area_data.split("|")[2].lstrip(" ").split(" ")[:2]
#                 )
#             if temp_area != 0:
#                 city["area"] = temp_area
#                 city.save()
#             if len(density_data.split("|")) < 3 or not density_data.__contains__(
#                 "density"
#             ):
#                 temp_density = 0
#             else:
#                 temp_density = format_nums(
#                     density_data.split("|")[len(density_data.split("|")) - 1]
#                     .lstrip(" ")
#                     .split(" ")[:2]
#                 )
#             if temp_density != 0:
#                 city["population_density"] = temp_density
#                 city.save()
#         else:
#             continue


# for city in c:
#     print(city["name"])
#     print(city["population"])
#     print(city["area"])
#     print(city["population_density"])
#     print()

# short_ans_url = "http://api.wolframalpha.com/v1/result?appid=38LR3Q-5V34V3KX75"

# for city in c:
#     print(city["name"] + ", " + city["state"])
#     r = requests.get(
#         short_ans_url + "&i=median+age+" + city["name"] + "+" + city["state"] + "%3f"
#     )
#     try:   
#         city["median_age"] = round(float(re.match(r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?', r.text).group()), 0)
#         city.save()
#     except AttributeError:
#         continue

# for city in c:
#     print(city["name"] + ", " + city["state"])
#     source = requests.get('https://city-data.com/city/'+ city["name"].replace(' ', '-') + "-" + city["state"].replace(' ', '-') + ".html")
#     soup = BeautifulSoup(source.content, 'lxml')

#     try:
#         rent_data = soup.find('section', class_='median-rent')
#         rent_stat = rent_data.text.split(':')[1]
#         gross_rent = int(rent_stat.strip().lstrip('$').rstrip('.').replace(',', ''))
#         print(gross_rent)
#         city["median_gross_rent"] = gross_rent
#         city.save()
#     except AttributeError:
#         continue

# source = requests.get('https://city-data.com/city/austin-texas.html')
# soup = BeautifulSoup(source.content, 'lxml')

# rent_data = soup.find('section', class_='median-rent')
# rent_stat = rent_data.p.text.split(':')[1]

# print(int(rent_stat.strip().lstrip('$').rstrip('.').replace(',', '')))

for city in c:
    print(city["name"])
    if city["population"] == 10000:
        city["population"] = 0
    if city["population_density"] == 10000:
        city["population_density"] = 0
    if city["area"] == 1000000:
        city["area"] = 0
    city.save()

Connector.disconnect_database()
