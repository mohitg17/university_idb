import sys
from PIL import Image

from idb_app.models import University, UniversityImage
from idb_app.mongo import Connector

Connector.load_database_creds()

Connector.connect_prod_database()

# change this name to view another university image
university_name = "The University of Texas Health Science Center at Houston"
uni = University.objects(school_name=university_name).first()
assert uni is not None

uni_image = UniversityImage.objects(university=uni).first()
assert uni_image is not None

image = Image.open(uni_image.image)
image.show()


Connector.disconnect_database()
