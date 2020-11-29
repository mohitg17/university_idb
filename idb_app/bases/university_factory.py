from idb_app.bases import BaseFactory, UniversityBase

class UniversityFactory(BaseFactory):

    @classmethod
    def factory_method(cls):
        return UniversityBase()