from idb_app.models import University
from idb_app.mongo import Connector

# standalone script to test university querying
# gets the first 3 universities it finds and prints some details 

Connector.load_database_creds()

Connector.connect_prod_database()

universities = University.objects().limit(3)

for u in universities:
    print(f"Name: {u.name}")
    print(f"Location: {str(u.city)}")
    print(f"Acceptance_rate: {u.acceptance_rate} %")
    print(f"Median admitted SAT score: {u.sat_median}")
    print("="*80)

Connector.disconnect_database()

