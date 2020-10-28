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
        self.assertEqual(self.uni.school_name, "Harvard University")
        self.uni = University.objects(school_name="Harvard University", school_state="Massachusetts").first()
        self.assertEqual(self.uni.school_name, "Harvard University")

    def test_city_query(self):
        self.city = City.objects(name="Austin").first()
        self.assertEqual(self.city.name, "Austin")
        self.city = City.objects(name="Austin", state="Texas").first()
        self.assertEqual(self.city.name, "Austin")

    def test_major_query(self):
        self.major = Major.objects(name="education").first()
        self.assertEqual(self.major.name, "education")

    def test_uni_image_query(self):
        self.image = UniversityImage.objects(university=ObjectId('5f965e1b81739c6287e0ccf8')).first()
        self.assertEqual(self.image.id, ObjectId('5f972c43c2f60552d0590828'))

    def test_city_ref(self):
        self.uni = University.objects(school_name="Harvard University").first()
        self.assertEqual(self.uni.school_city, City.objects(name="Cambridge").first())

    def test_major_ref(self):
        self.uni = University.objects(school_name="Harvard University").first()
        self.assertEqual(self.uni.majors_offered[0], Major.objects(id=self.uni.majors_offered[0].id).first())

if __name__ == '__main__':
    unittest.main()