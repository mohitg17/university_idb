from idb_app.models import University, City, Major
from idb_app.mongo import Connector
from idb_app.models import choices
from mongoengine import NotUniqueError
import requests


def create_majors():
    majors = [
        "agriculture",
        "resources",
        "architecture",
        "ethnic_cultural_gender",
        "communication",
        "communications_technology",
        "computer",
        "personal_culinary",
        "education",
        "engineering",
        "engineering_technology",
        "language",
        "family_consumer_science",
        "legal",
        "english",
        "humanities",
        "library",
        "biological",
        "mathematics",
        "military",
        "multidiscipline",
        "parks_recreation_fitness",
        "philosophy_religious",
        "theology_religious_vocation",
        "physical_science",
        "science_technology",
        "psychology",
        "security_law_enforcement",
        "public_administration_social_service",
        "social_science",
        "construction",
        "mechanic_repair_technology",
        "precision_production",
        "transportation",
        "visual_performing",
        "health",
        "business_marketing",
        "history",
    ]
    for major in majors:
        major_data = {
            "name": major,
            "median_starting_salary": 10,
            "median_midcareer_salary": 10,
            "num_certificate_programs": 10,
            "num_associate_programs": 10,
            "num_bachelor_programs": 10,
        }
        mjr = Major(**major_data)
        mjr.save()


def create_city(data):
    if City.objects(name=data["school_city"]):
        return City.objects(name=data["school_city"]).first()
    else:
        city_params = {
            "name": data["school_city"],
            "state": data["school_state"],
            "area": 1000000,
            "population": 1000000,
            "population_density": 10000,
            "community_type": data["school_locale"],
            "median_age": 20,
            "median_gross_rent": 1000,
        }

        dummy_city = City(**city_params)
        dummy_city.save()
        return dummy_city


def rename_fields(data):
    tmp = {}
    for key in data:
        new_key = key.replace(".", "_")
        tmp[new_key] = data[key]
    return tmp


def compress_majors(data):
    majors_offered = []
    compressed = {}
    for key in data:
        if "latest_academics_program_bachelors" in key:
            if data[key] and data[key] > 0:
                majors_offered.append(Major.objects(name=key.split("_")[-1]).first())
        else:
            compressed[key] = data[key]
    compressed["majors_offered"] = majors_offered
    return compressed


def fix_major_references(uni, data):
    majors_offered = []
    for key in data:
        if "latest.academics.program.bachelors" in key:
            if data[key] and data[key] > 0:
                majors_offered.append(Major.objects(name=key.split(".")[-1]).first())
    uni.majors_offered = majors_offered
    uni.save()


def translate(cleaned):
    degrees = {
        0: choices.UNCLASSIFIED,
        1: choices.DEGREE_CERTIFICATE,
        2: choices.DEGREE_ASSOCIATE,
        3: choices.DEGREE_BACHELORS,
        4: choices.DEGREE_GRADUATE,
    }

    locale = {
        -2: "Unclassified",
        -3: "Unclassified",
        11: "City",
        12: "City",
        13: "City",
        21: "Suburb",
        22: "Suburb",
        23: "Suburb",
        31: "Town",
        32: "Town",
        33: "Town",
        41: "Rural",
        42: "Rural",
        43: "Rural",
    }

    states = {
        "AL": "Alabama",
        "AK": "Alaska",
        "AZ": "Arizona",
        "AR": "Arkansas",
        "CA": "California",
        "CO": "Colorado",
        "CT": "Connecticut",
        "DE": "Delaware",
        "FL": "Florida",
        "GA": "Georgia",
        "HI": "Hawaii",
        "ID": "Idaho",
        "IL": "Illinois",
        "IN": "Indiana",
        "IA": "Iowa",
        "KS": "Kansas",
        "KY": "Kentucky",
        "LA": "Louisiana",
        "ME": "Maine",
        "MD": "Maryland",
        "MA": "Massachusetts",
        "MI": "Michigan",
        "MN": "Minnesota",
        "MS": "Mississippi",
        "MO": "Missouri",
        "MT": "Montana",
        "NE": "Nebraska",
        "NV": "Nevada",
        "NH": "New Hampshire",
        "NJ": "New Jersey",
        "NM": "New Mexico",
        "NY": "New York",
        "NC": "North Carolina",
        "ND": "North Dakota",
        "OH": "Ohio",
        "OK": "Oklahoma",
        "OR": "Oregon",
        "PA": "Pennsylvania",
        "RI": "Rhode Island",
        "SC": "South Carolina",
        "SD": "South Dakota",
        "TN": "Tennessee",
        "TX": "Texas",
        "UT": "Utah",
        "VT": "Vermont",
        "VA": "Virginia",
        "WA": "Washington",
        "WV": "West Virginia",
        "WI": "Wisconsin",
        "WY": "Wyoming",
    }

    cleaned["school_degrees_awarded_highest"] = degrees[
        cleaned["school_degrees_awarded_highest"]
    ]
    cleaned["school_degrees_awarded_predominant"] = degrees[
        cleaned["school_degrees_awarded_predominant"]
    ]
    cleaned["school_school_url"] = (
        f"https://{cleaned['school_school_url'].split('.', 1)[1]}"
        if cleaned["school_school_url"]
        else "None"
    )
    cleaned["school_locale"] = locale[cleaned["school_locale"]]
    cleaned["school_state"] = (
        states[cleaned["school_state"].upper()]
        if cleaned["school_state"].upper() in states
        else "Texas"
    )
    return cleaned


def query(fields: list, arguments: dict) -> dict:
    base_url = "https://api.data.gov/ed/collegescorecard/v1/"
    api_key = "KmhhX8cOFnuAhYhQoXdv85o9kdd4fFchmFKmdvGC"
    resp = requests.get(
        f"{base_url}schools?api_key={api_key}&fields={','.join(fields)}",
        params=arguments,
    )
    assert resp.status_code == 200
    return resp.json()


if __name__ == "__main__":
    # requires that you have a .env file with a mongo DB user/password
    Connector.load_database_creds()
    Connector.connect_prod_database()

    for i in range(1, 21):
        raw_data = query(
            [
                "school.name",
                "school.city",
                "school.state",
                "school.locale",
                "school.school_url",
                "latest.student.size",
                "latest.admissions.admission_rate.overall",
                "latest.cost.tuition.in_state",
                "latest.cost.tuition.out_of_state",
                "latest.cost.attendance.academic_year",
                "latest.aid.median_debt.completers.overall",
                "school.degrees_awarded.highest",
                "school.degrees_awarded.predominant",
                "latest.earnings.10_yrs_after_entry.median",
                "latest.admissions.sat_scores.average.overall",
                "latest.admissions.act_scores.midpoint.cumulative",
                "latest.academics.program.bachelors.agriculture",
                "latest.academics.program.bachelors.resources",
                "latest.academics.program.bachelors.architecture",
                "latest.academics.program.bachelors.ethnic_cultural_gender",
                "latest.academics.program.bachelors.communication",
                "latest.academics.program.bachelors.communications_technology",
                "latest.academics.program.bachelors.computer",
                "latest.academics.program.bachelors.personal_culinary",
                "latest.academics.program.bachelors.education",
                "latest.academics.program.bachelors.engineering",
                "latest.academics.program.bachelors.engineering_technology",
                "latest.academics.program.bachelors.language",
                "latest.academics.program.bachelors.family_consumer_science",
                "latest.academics.program.bachelors.legal",
                "latest.academics.program.bachelors.english",
                "latest.academics.program.bachelors.humanities",
                "latest.academics.program.bachelors.library",
                "latest.academics.program.bachelors.biological",
                "latest.academics.program.bachelors.mathematics",
                "latest.academics.program.bachelors.military",
                "latest.academics.program.bachelors.multidiscipline",
                "latest.academics.program.bachelors.parks_recreation_fitness",
                "latest.academics.program.bachelors.philosophy_religious",
                "latest.academics.program.bachelors.theology_religious_vocation",
                "latest.academics.program.bachelors.physical_science",
                "latest.academics.program.bachelors.science_technology",
                "latest.academics.program.bachelors.psychology",
                "latest.academics.program.bachelors.security_law_enforcement",
                "latest.academics.program.bachelors.public_administration_social_service",
                "latest.academics.program.bachelors.social_science",
                "latest.academics.program.bachelors.construction",
                "latest.academics.program.bachelors.mechanic_repair_technology",
                "latest.academics.program.bachelors.precision_production",
                "latest.academics.program.bachelors.transportation",
                "latest.academics.program.bachelors.visual_performing",
                "latest.academics.program.bachelors.health",
                "latest.academics.program.bachelors.business_marketing",
                "latest.academics.program.bachelors.history",
                "latest.student.demographics.race_ethnicity.white",
                "latest.student.demographics.race_ethnicity.black",
                "latest.student.demographics.race_ethnicity.hispanic",
                "latest.student.demographics.race_ethnicity.asian",
                "latest.student.demographics.men",
                "latest.student.demographics.women",
                "latest.completion.4_yr_completion.overall",
                "latest.completion.completion_rate_4yr_150_white",
                "latest.completion.completion_rate_4yr_150_black",
                "latest.completion.completion_rate_4yr_150_hispanic",
                "latest.completion.completion_rate_4yr_150_asian",
                "latest.student.retention_rate.four_year.full_time",
            ],
            {"per_page": 100, "page": i, "school.degrees_awarded.predominant": 3}
            # {"id":228778}
        )

        print(raw_data["metadata"])

        for j in range(len(raw_data["results"])):
            # uni = University.objects(school_name=raw_data['results'][j]['school.name'], school_city=City.objects(name=raw_data['results'][j]['school.city']).first()).first()
            # fix_major_references(uni, raw_data['results'][j])
            uni_data = rename_fields(raw_data["results"][j])
            uni_data = compress_majors(uni_data)
            uni_data = translate(uni_data)
            uni_data["school_city"] = create_city(uni_data)

            uni = University(**uni_data)
            try:
                uni.save()
            except NotUniqueError:
                print("not unique")

    Connector.disconnect_database()
