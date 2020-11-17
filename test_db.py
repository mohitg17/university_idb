import unittest
from idb_app.mongo import Connector
from idb_app.models import University, City, Major, UniversityImage
from bson.objectid import ObjectId


class TestDB(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        Connector.load_database_creds()
        Connector.connect_prod_database()

    @classmethod
    def tearDownClass(cls):
        Connector.disconnect_database()
    
    def test_uni_query(self):
        self.uni = University.objects(school_name="Harvard University").first()
        self.assertEqual(self.uni.id, ObjectId("5f965e1b81739c6287e0ccf8"))
        self.uni = University.objects(
            school_name="Harvard University", school_state="Massachusetts"
        ).first()
        self.assertEqual(self.uni.id, ObjectId("5f965e1b81739c6287e0ccf8"))
        self.uni = University.objects(
            school_name="Harvard University",
            school_state="Massachusetts",
            school_city=City.objects(name="Cambridge").first().id,
        ).first()
        self.assertEqual(self.uni.id, ObjectId("5f965e1b81739c6287e0ccf8"))
        self.nothing = University.objects(school_name="UT Austin").first()
        self.assertEqual(self.nothing, None)

    def test_city_query(self):
        self.city = City.objects(name="Austin").first()
        self.assertEqual(self.city.id, ObjectId("5f964eb5e2830ac6278784b3"))
        self.city = City.objects(name="Austin", state="Texas").first()
        self.assertEqual(self.city.id, ObjectId("5f964eb5e2830ac6278784b3"))
        self.nothing = City.objects(name="austin").first()
        self.assertEqual(self.nothing, None)

    def test_major_query(self):
        self.major = Major.objects(name="education").first()
        self.assertEqual(self.major.id, ObjectId("5f963df0608c791e121cacc7"))
        self.nothing = Major.objects(name="edu").first()
        self.assertEqual(self.nothing, None)

    def test_uni_image_query(self):
        self.image = UniversityImage.objects(
            university=ObjectId("5f965e1b81739c6287e0ccf8")
        ).first()
        self.assertEqual(self.image.id, ObjectId("5f972c43c2f60552d0590828"))

    def test_city_ref(self):
        self.uni = University.objects(school_name="Harvard University").first()
        self.assertEqual(self.uni.school_city, City.objects(name="Cambridge").first())

    def test_major_ref(self):
        self.uni = University.objects(school_name="Harvard University").first()
        self.assertEqual(
            self.uni.majors_offered[0],
            Major.objects(id=self.uni.majors_offered[0].id).first(),
        )

    def test_uni_image(self):
        self.image = UniversityImage.objects(
            university=ObjectId("5f965e1b81739c6287e0ccf8")
        ).first()
        self.assertEqual(self.image.id, ObjectId("5f972c43c2f60552d0590828"))

    def test_update_city(self):
        self.city = City.objects(name="Austin").first()
        correct_population = self.city.population
        self.assertEqual(self.city.population, correct_population)
        self.city.population = 5000
        self.city.save()
        self.city = City.objects(name="Austin").first()
        self.assertEqual(self.city.population, 5000)
        self.city.population = correct_population
        self.city.save()

    def test_update_uni(self):
        self.uni = University.objects(school_name="Harvard University").first()
        correct_student_size = self.uni.latest_student_size
        self.assertEqual(self.uni.latest_student_size, correct_student_size)
        self.uni.latest_student_size = 5000
        self.uni.save()
        self.uni = University.objects(school_name="Harvard University").first()
        self.assertEqual(self.uni.latest_student_size, 5000)
        self.uni.latest_student_size = correct_student_size
        self.uni.save()

    def test_update_major(self):
        self.major = Major.objects(name="Computer Science.").first()
        correct_earnings = self.major.earnings_weighted_sum
        self.assertEqual(self.major.earnings_weighted_sum, correct_earnings)
        self.major.earnings_weighted_sum = 5000
        self.major.save()
        self.major = Major.objects(name="Computer Science.").first()
        self.assertEqual(self.major.earnings_weighted_sum, 5000)
        self.major.earnings_weighted_sum = correct_earnings
        self.major.save()

    def test_create_major(self):
        major_params = {'name': 'Dummy', 'cip_code': '003830', 
        'earnings_weighted_sum': 817263800, 'earnings_count': 11503, 'program_count_estimate': 588}
        major = Major(**major_params)
        major.save()
        major = Major.objects(name="Dummy").first()
        self.assertIsNotNone(major)
        major.delete()

    def test_create_city(self):
        city_params = {'name': 'Dummy', 'state': 'Texas', 'area': 297.9, 'population': 950715, 
        'population_density': 3191, 'community_type': 'City', 'median_age': 33, 
        'median_gross_rent': 1000, 'latitude': 30.267153, 'longitude': -97.7430608}
        city = City(**city_params)
        city.save()
        city = City.objects(name="Dummy").first()
        self.assertIsNotNone(city)
        city.delete()

    def test_create_university(self):
        uni_params = {'school_name': 'Dummy University', 
        'school_city': City.objects(name="Cambridge").first(), 
        'school_state': 'Massachusetts', 
        'school_school_url': 'https://harvard.edu', 
        'school_degrees_awarded_predominant': "Bachelor's", 
        'school_degrees_awarded_highest': 'Graduate'}
        uni = University(**uni_params)
        uni.save()
        uni = University.objects(school_name="Dummy University").first()
        self.assertIsNotNone(uni)
        uni.delete()

if __name__ == "__main__":
    unittest.main()
