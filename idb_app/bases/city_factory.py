from idb_app.bases import BaseFactory, CityBase


class CityFactory(BaseFactory):
    @classmethod
    def factory_method(cls):
        return CityBase()
