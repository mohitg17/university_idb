from idb_app.bases import BaseFactory, MajorBase


class MajorFactory(BaseFactory):
    @classmethod
    def factory_method(cls):
        return MajorBase()
