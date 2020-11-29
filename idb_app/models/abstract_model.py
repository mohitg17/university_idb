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

    @classmethod
    def get_image_class(cls):
        raise NotImplementedError

    # does it really make sense to bind together the data model with the details of how its viewed into one class...
    # TODO consider moving these functionality into a View class or something
    def get_template(self):
        raise NotImplementedError
