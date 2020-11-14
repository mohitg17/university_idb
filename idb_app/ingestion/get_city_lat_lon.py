from idb_app.models import City, choices
from idb_app.mongo import Connector
import requests
import re

Connector.load_database_creds()

Connector.connect_prod_database()

cities = City.objects(latitude__exists=False)

for city in cities:
    print(city.name, city.state)
    try:
        resp = requests.get(f'https://maps.googleapis.com/maps/api/geocode/json?address={city.name},+{city.state}&key=AIzaSyBlPUyI4CmXPR9lFr_jMld3AqUBaD2LbjM')
        data = resp.json()
        latitude = data['results'][0]['geometry']['location']['lat']
        longitude = data['results'][0]['geometry']['location']['lng']
        city.latitude = latitude
        city.longitude = longitude
        city.save()
    except IndexError:
        pass
