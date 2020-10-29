from idb_app.models import Major, University
from idb_app.mongo import Connector


Connector.load_database_creds()

Connector.connect_prod_database()

count = 0
for m in Major.objects(cip_code__ne=None, program_count_estimate=None):
    if count % 100 == 0:
        print(f"======== done with {count} majors ========")
    m.program_count_estimate = University.objects(majors_cip=m).count()
    m.save()
    count += 1

Connector.disconnect_database()
