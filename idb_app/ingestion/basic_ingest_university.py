from idb_app.models import University, City, Major
from idb_app.mongo import Connector

from idb_app.models import choices

# standalone script to ingest Uni data into Mongo
# note that repeated runs (without clearing DB) will fail because we are forcing some fields to be unique
# will not work without ingesting Cities and Majors

# requires that you have a .env file with a mongo DB user/password
Connector.load_database_creds()

Connector.connect_prod_database()

example_universities = [
    {
        "name": "the_university_of_texas_at_austin",
        "student_population": 40329,
        "acceptance_rate": 38.52,
        "in_state_tuition": 10610,
        "out_of_state_tuition": 37580,
        "city": City.objects(name="austin", state=choices.STATE_TEXAS).first(),
        "website": "http://utexas.edu",
        "sat_median": 1367,
        "act_median": 30,
        "percent_black": 4.23,
        "percent_white": 39.97,
        "percent_asian": 22.11,
        "percent_hispanic": 23.54,
        "percent_male": 46.15,
        "percent_female": 53.85,
        "median_debt": 11514,
        "avg_cost": 16505,
        "predominant_degree": "Bachelor's",
        "highest_degree": "Doctorate",
        # TODO check this
        "completion_overall": 0.5938,
        "completion_rate_black": 74.06,
        "completion_rate_asian": 87.93,
        "completion_rate_hispanic": 73.91,
        "completion_rate_white": 86.12,
        "earnings": 58200,
        "retention_rate": 94.95,
        # will need to update this once all the Major models are in
        "majors_offered": Major.objects().all(),
    },
    {
        "name": "harvard_university",
        "student_population": 7582,
        "acceptance_rate": 4.73,
        "in_state_tuition": 50420,
        "out_of_state_tuition": 50420,
        "city": City.objects(name="cambridge", state=choices.STATE_MASSACHUSETTS).first(),
        "website": "http://harvard.edu",
        "sat_median": 1520,
        "act_median": 34,
        "percent_black": 8.03,
        "percent_white": 40.54,
        "percent_asian": 19.22,
        "percent_hispanic": 11.33,
        "percent_male": 51.13,
        "percent_female": 48.87,
        "median_debt": 591,
        "avg_cost": 15561,
        "predominant_degree": "Bachelor's",
        "highest_degree": "Doctorate",
        # TODO check this
        "completion_overall": 0.492,
        "completion_rate_black": 99.04,
        "completion_rate_asian": 97.73,
        "completion_rate_hispanic": 98.68,
        "completion_rate_white": 97.60,
        "earnings": 58200,
        "retention_rate": 99.11,
        # will need to update this once all the Major models are in
        "majors_offered": Major.objects().all(),
    },
    {
        "name": "rice_university",
        "student_population": 3962,
        "acceptance_rate": 11.13,
        "in_state_tuition": 47350,
        "out_of_state_tuition": 47350,
        "city": City.objects(name="houston", state=choices.STATE_TEXAS).first(),
        "website": "http://rice.edu",
        "sat_median": 1513,
        "act_median": 34,
        "percent_black": 7.14,
        "percent_white": 33.24,
        "percent_asian": 25.69,
        "percent_hispanic": 15.52,
        "percent_male": 52.30,
        "percent_female": 47.70,
        "median_debt": 537,
        "avg_cost": 20879,
        "predominant_degree": "Bachelor's",
        "highest_degree": "Doctorate",
        # TODO check this
        "completion_overall": 0.390,
        "completion_rate_black": 85.94,
        "completion_rate_asian": 98.08,
        "completion_rate_hispanic": 92.31,
        "completion_rate_white": 94.99,
        "earnings": 65400,
        "retention_rate": 97.41,
        # will need to update this once all the Major models are in
        "majors_offered": Major.objects().all(),
    }
]

# example insertion
# could also init with u = University(name="x", field2=y, ...)
for uni in example_universities:
    u = University(**uni)
    u.save()

# example query
for uni in example_universities:
    uni_from_db = University.objects(name=uni["name"]).first()
    assert uni_from_db.name == uni["name"]

Connector.disconnect_database()
