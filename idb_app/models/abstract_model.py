from typing import List

from idb_app.filtering.filtering_controls import RadioButtonSet, TextInput


# defines the common interface for all models
class AbstractModel:
    @classmethod
    def get_name_field(cls) -> str:
        raise NotImplementedError

    @classmethod
    def get_filtering_text(cls) -> List[TextInput]:
        raise NotImplementedError

    @classmethod
    def get_sort_buttons(cls) -> RadioButtonSet:
        raise NotImplementedError

    @classmethod
    def get_filtering_buttons(cls) -> List[RadioButtonSet]:
        raise NotImplementedError

    # defines the attributes that are passed to .only() for the base model query
    @classmethod
    def get_base_attributes(cls) -> List[str]:
        raise NotImplementedError

    # allows you to do enforce global constraints on which objects are viewable -- see major for an example
    @classmethod
    def base_queryset(cls):
        return cls.objects()

    # packages model info in a way that can be used by the base page front end
    # TODO pull out some of the repetition across model/city/uni implementations of this into base class
    @classmethod
    def create_models(cls, query_set):
        raise NotImplementedError

    @classmethod
    def get_image_class(cls):
        raise NotImplementedError
