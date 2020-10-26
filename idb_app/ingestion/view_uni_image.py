from PIL import Image
import matplotlib.pyplot as plt

from idb_app.models import UniversityImage
from idb_app.mongo import Connector

# standalone script to quickly cycle through university images
# Beware using this script with a lot of images. You can't kill the process (even with ctrl+C) once started

Connector.load_database_creds()

Connector.connect_prod_database()

query_set = UniversityImage.objects().limit(10)

fig, ax = plt.subplots()

time_delay_per_image = 0.1
for uni_image in query_set:
    plt.cla()
    plt.imshow(Image.open(uni_image.image))
    ax.set_title(f"{uni_image.university.school_name}")
    # Note that using time.sleep does *not* work here!
    plt.pause(time_delay_per_image)


Connector.disconnect_database()
