import os
import requests
import responses
import googlemaps.maps as gmaps
import googlemaps
import datetime

from json import dumps
from idb_app.models import City, CityImage
from idb_app.mongo import Connector

# requires that you have a .env file with a mongo DB user/password
# also requires a google API key (which can be found in the google maps section of our GCP project) in .env
Connector.load_database_creds()

Connector.connect_prod_database()

# TODO currently only ingests 10 images
# use .limit(X) if you only want to try to scrape for X cities
cities = City.objects().only("name", "state")

API_KEY = os.environ["GOOGLE_MAPS_API_KEY"]
client = googlemaps.Client(API_KEY)

url = "https://maps.googleapis.com/maps/api/staticmap"
responses.add(responses.GET, url, status=200)

# A test showing that searching for a fake place will still yield a usable image
# location_string = "kdjafn, asdn"
# filename = "tmp/badimg.png"

# response = client.static_map(
#     size=(400, 400),
#     zoom=12,
#     center=location_string,
#     maptype="satellite",
#     format="png",
#     scale=1,
# )

# f = open(filename, 'wb')
# for chunk in response:
#     if chunk:
#         f.write(chunk)
# f.close()

response_times = []
count = 0
for c in cities:
    start_time = datetime.datetime.now()
    # skip if we already have an image for that city
    if CityImage.objects(city=c).first() is None:
        location_string = f"{c.name}, {c.state}"
        filename = f"tmp/{c.name}_{c.state}.png"
        if count % 100 == 0:
            print(f"=================== Done with {count} cities ===================")
            if not len(response_times) == 0:
                avg = sum(response_times) / len(response_times)
                print("Average time: ", avg)
            else:
                print("No response times")
        print(f"querying image for {location_string}")
        response = client.static_map(
            size=(400, 400),
            zoom=14,
            center=location_string,
            maptype="satellite",
            format="png",
            scale=1,
        )

        f = open(filename, "wb")
        for chunk in response:
            if chunk:
                f.write(chunk)
        f.close()

        db_entry = CityImage(city=c, image=filename)
        db_entry.save()
        # Delete file locally
        os.remove(filename)
        response_times.append((datetime.datetime.now() - start_time).total_seconds())

    count += 1

if not len(response_times) == 0:
    avg = sum(response_times) / len(response_times)
    print("Average time: ", avg)
else:
    print("No response times")
print("Total time: ", sum(response_times))
Connector.disconnect_database()
