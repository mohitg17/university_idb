import unittest
from idb_app.mongo import Connector
from idb_app.models import University, City, Major
from bson.objectid import ObjectId
from flask import url_for


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Connector.load_database_creds()
        Connector.connect_prod_database()

    @classmethod
    def tearDownClass(cls):
        Connector.disconnect_database()

    def test_major(self):
        major = Major.objects(name="education").first()
        instance = {
            "name": major.name.replace("_", " ").title(),
            "attribute_1": {
                "name": "Median Starting Salary",
                "value": major.median_starting_salary,
            },
            "attribute_2": {
                "name": "Median Midcareer Salary",
                "value": major.median_midcareer_salary,
            },
            "attribute_3": {
                "name": "Number of Bachelor's Programs",
                "value": major.num_bachelor_programs,
            },
        }
        expected = {
            "name": "Education",
            "attribute_1": {"name": "Median Starting Salary", "value": 10},
            "attribute_2": {"name": "Median Midcareer Salary", "value": 10},
            "attribute_3": {"name": "Number of Bachelor's Programs", "value": 10},
        }
        self.assertEqual(instance, expected)

    def test_city(self):
        city = City.objects(name="Austin").first()
        instance = {
            "name": str(city),
            "attribute_1": {"name": "Population", "value": city.population},
            "attribute_2": {"name": "Community Type", "value": city.community_type},
            "attribute_3": {
                "name": "Median Gross Rent",
                "value": city.median_gross_rent,
            },
        }
        expected = {
            "name": "Austin, Texas",
            "attribute_1": {"name": "Population", "value": 950715},
            "attribute_2": {"name": "Community Type", "value": "City"},
            "attribute_3": {"name": "Median Gross Rent", "value": 1000},
        }
        self.assertEqual(instance, expected)

    def test_uni(self):
        university = University.objects(school_name="Harvard University").first()
        instance = {
            "name": university.school_name.replace("_", " ").title(),
            "id": university.id,
            "attribute_1": {"name": "State", "value": university.school_state},
            "attribute_2": {
                "name": "Student Population",
                "value": university.latest_student_size,
            },
            "attribute_3": {
                "name": "Cost of Attendance",
                "value": university.latest_cost_attendance_academic_year,
            },
        }
        expected = {
            "name": "Harvard University",
            "id": ObjectId("5f965e1b81739c6287e0ccf8"),
            "attribute_1": {"name": "State", "value": "Massachusetts"},
            "attribute_2": {"name": "Student Population", "value": 7582},
            "attribute_3": {"name": "Cost of Attendance", "value": 71135},
        }
        self.assertEqual(instance, expected)

    def test_uni_modify(self):
        university = University.objects(school_name="Marian University").first()
        actual = []
        for property in university:
            if university[property] == 0:
                university[property] = "NA"
            if isinstance(university[property], float):
                university[property] = round(float(university[property] * 100), 4)
                actual.append(university[property])

        expected = [
            65.04,
            5.65,
            78.76,
            2.12,
            7.41,
            30.56,
            69.44,
            62.63,
            26.19,
            33.33,
            40.0,
            65.34,
            4377.7411,
            -8842.0638
        ]
        self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
