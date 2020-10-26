import os
from google_images_search import GoogleImagesSearch

from idb_app.models import University, UniversityImage
from idb_app.mongo import Connector

# requires that you have a .env file with a mongo DB user/password
# also required a google API key and google search CX
Connector.load_database_creds()

Connector.connect_prod_database()

# use .limit(X) if you only want to try to scrape for X schools
universities = University.objects().only("school_name").limit(100)

count = 0
for u in universities:
    # skip if we already have an image for that university
    if UniversityImage.objects(university=u).first() is None:
        if count % 100 == 0:
            print(f"=================== Done with {count} schools ===================")
        print(f"querying image for {u.school_name}")
        gis = GoogleImagesSearch(os.environ["GOOGLE_API_KEY"], os.environ["GOOGLE_SEARCH_CX"])
        # TODO consider limiting image sizes here
        search_params = {
             'q': u.school_name,
             'num': 1,
             'safe': 'high',
             'fileType': 'jpg|png',
             'imgType': 'photo',
             'rights': 'cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived'
        }
        download_path = "/tmp/"

        # TODO consider resizing here
        gis.search(search_params=search_params, path_to_dir=download_path)
        query_results = gis.results()

        # skip if no images found
        if query_results:
            image_file = query_results[0].path

            db_entry = UniversityImage(university=u, image=image_file, result_number=0)
            db_entry.save()
            # delete image file from local machine
            os.remove(image_file)
        else:
            print(f"No image found for: {u.school_name}")
    count += 1

Connector.disconnect_database()
