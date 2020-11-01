import os
from google_images_search import GoogleImagesSearch

from idb_app.models import University, UniversityImage
from idb_app.mongo import Connector

# requires that you have a .env file with a mongo DB user/password
# also required a google API key and google search CX
Connector.load_database_creds()

Connector.connect_prod_database()

# school names we want to try and get better images for
raw_school_names = """Kentucky Christian University
Saint Joseph Seminary College
North American University
Westfield State University 
Rhode Island School of Design
Fresno Pacific University 
Western Connecticut State University 
Post University 
Wilmington University 
Research College of Nursing
Southern New Hampshire University 
Purdue University Global-Omaha
Rabbinical College of America 
Marist College 
University of Wisconsin-Milwaukee Flex 
Northeastern University Lifelong Learning Network
California Jazz Conservatory 
Chamberlain University-Nevada
Hussian College-Studio School Los Angeles
DeVry University-Missouri
University of North Carolina at Asheville
Yeshiva Derech Chaim
Rabbinical Academy Mesivta Rabbi Chaim Berlin
Nazareth College
North Central University
Western New England University"""

schools = raw_school_names.split("\n")
for raw in schools:
    uni_entry = University.objects(school_name=raw.strip()).first()
    if uni_entry is None:
        print(f"ERROR: school '{raw}' not found")
    else:
        uni_image = UniversityImage.objects(university=uni_entry).first()
        if uni_image is None:
            print(f"ERROR: no image for school id={uni_entry.id}")
        else:
            offset = uni_image.result_number
            gis = GoogleImagesSearch(
                os.environ["GOOGLE_API_KEY"], os.environ["GOOGLE_SEARCH_CX"]
            )
            search_params = {
                "q": uni_entry.school_name,
                "num": offset + 2,
                "safe": "high",
                "imgType": "photo",
                "rights": "cc_publicdomain|cc_attribute|cc_sharealike|cc_noncommercial|cc_nonderived",
            }
            download_path = "/tmp/"

            gis.search(
                search_params=search_params,
                path_to_dir=download_path,
                width=400,
                height=200,
            )
            query_results = gis.results()

            # skip if no images found
            if query_results is not None and len(query_results) > offset + 1:
                image_file = query_results[offset + 1].path
                uni_image.result_number += 1
                uni_image.image = image_file
                uni_image.save()

                # delete image file from local machine
                os.remove(image_file)
            else:
                print(f"ERROR: No image found for: {uni_entry.school_name}")

Connector.disconnect_database()
