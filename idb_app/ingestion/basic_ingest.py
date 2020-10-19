from idb_app.models import City, Major, University


def insert_majors():
    majors = [
        {
            "name": "education",
            "median_starting_salary": 34900,
            "median_midcareer_salary": 52000,
            "num_certificate_programs": 376,
            "num_associate_programs": 696,
            "num_bachelor_programs": 1169,
        },
        {
            "name": "history",
            "median_starting_salary": 39200,
            "median_midcareer_salary": 71000,
            "num_certificate_programs": 21,
            "num_associate_programs": 185,
            "num_bachelor_programs": 1233,
        },
        {
            "name": "engineering",
            "median_starting_salary": 58957,
            "median_midcareer_salary": 99257,
            "num_certificate_programs": 95,
            "num_associate_programs": 464,
            "num_bachelor_programs": 619,
        },
    ]

    for major in majors:
        m = Major(**major)
        m.save()



