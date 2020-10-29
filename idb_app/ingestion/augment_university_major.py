import os
import us
import json
import requests
import traceback
from os import path

from idb_app.mongo import Connector
from idb_app.models import University, City, Major


# Script to add lat/lon,


def query(fields: list, arguments: dict) -> dict:
    base_url = "https://api.data.gov/ed/collegescorecard/v1/"
    api_key = os.environ["DEPT_ED_API_KEY"]
    resp = requests.get(f"{base_url}schools?api_key={api_key}&fields={','.join(fields)}", params=arguments)
    if resp.status_code == 429:
        print("Hit rate limit!")
    return resp.json()


# query over all results -- handles paginated responses
def query_all_schools(fields: list) -> list:
    results = []
    page = 0
    resp = None
    while resp is None or resp["metadata"]["total"] != len(results):
        # 3 for bachelors
        resp = query(fields, {"per_page": 100, "page": page, "school.degrees_awarded.predominant": 3})
        page += 1

        for school in resp["results"]:
            results.append(school)

    return results


# attempt to map data from DOE to an Uni document in the DB; return None if not possible
def match_university(doe_id, school_name, school_city, school_state) -> University:
    by_doe_id = University.objects(doe_id=doe_id).first()
    if by_doe_id is not None:
        return by_doe_id

    by_name_qs = University.objects(school_name=school_name)
    # cannot return unless we match just one
    if len(by_name_qs) == 1:
        return by_name_qs.first()

    state_name = us.states.lookup(school_state).name
    by_state_qs = University.objects(school_name=school_name, school_state=state_name)
    if len(by_state_qs) == 1:
        return by_state_qs.first()

    city = City.objects(name=school_city, state=state_name).first()
    by_city_qs = University.objects(school_name=school_name, school_state=state_name, school_city=city)
    if len(by_city_qs) == 1:
        return by_city_qs.first()

    return None


Connector.load_database_creds()

Connector.connect_prod_database()


def load_data() -> list:
    data_file = "/tmp/school_data.json"
    if not path.exists(data_file):
        query_results = query_all_schools(["id",
                                           "school.name",
                                           "school.state",
                                           "school.city",
                                           "latest.programs.cip_4_digit.earnings",
                                           "latest.programs.cip_4_digit.title",
                                           "latest.programs.cip_4_digit.credential.level",
                                           "latest.programs.cip_4_digit.ope6_id",
                                           "location.lat",
                                           "location.lon",
                                           ])
        with open(data_file, "w") as f:
            json.dump(query_results, f)
    else:
        with open(data_file, "r") as f:
            query_results = json.load(f)
    return query_results


def update_university(school_dict, u: University):
    u.doe_id = school_dict["id"]
    u.latitude = school_dict["location.lat"]
    u.longitude = school_dict["location.lon"]
    major_stats = [s for s in school_dict["latest.programs.cip_4_digit"] if s["credential"]["level"] == 3]
    for major_raw in major_stats:
        m = Major.get_or_create(cip_code=major_raw["ope6_id"], title=major_raw["title"])
        if major_raw["earnings"]["count"] is not None and major_raw["earnings"]["median_earnings"] is not None:
            m.earnings_count += major_raw["earnings"]["count"]
            m.earnings_weighted_sum += (major_raw["earnings"]["count"] * major_raw["earnings"]["median_earnings"])
        m.save()
        u.majors_cip.append(m)
    u.save()


raw_school_stats = load_data()

failures = 0
count = 0
for raw_school in raw_school_stats:
    if count % 100 == 0:
        print(f"======== done with {count} schools ========")
    count += 1
    uni = match_university(doe_id=raw_school["id"],
                           school_name=raw_school["school.name"],
                           school_city=raw_school["school.city"],
                           school_state=raw_school["school.state"],
                           )
    if uni is None:
        failures += 1
        continue
    if uni.latitude is not None:
        continue
    try:
        update_university(raw_school, uni)
    except Exception as e:
        print(e)
        failures += 1

print(f"num failures: {failures}")

Connector.disconnect_database()
