import os
from idb_app.models import University
from idb_app.mongo import Connector

Connector.load_database_creds()

Connector.connect_prod_database()

print(len(University.objects()))

count = 0
for uni in University.objects():
    if count % 100 == 0:
        print(f" == Finished {count} schools == ")
    uni.cost_category = uni.calculate_cost_cat()
    uni.save()
    count += 1

Connector.disconnect_database()