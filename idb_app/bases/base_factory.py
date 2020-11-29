from idb_app.bases import UniversityBase, CityBase, MajorBase
from abc import ABC, abstractmethod
from flask import request

class BaseFactory(ABC):

    @classmethod
    def get_filter_parameters(cls, raw_params, model):
        params = {}
        for k, v in raw_params.items():
            if "filter__" in k and v:
                params[k.replace("filter__", "")] = v.strip()
            elif k == "searchin" and v:
                params[f"{model.get_name_field()}__icontains"] = v.strip()
        return params
    
    @classmethod
    def get_model_objects(cls, model_class):
        order = request.args.get("order")
        if order is None:
            order = "+"
        order_by = f"{order}{request.args.get('order_by')}"
        if len(order_by) == 1:
            order_by = ""
        filter_params = BaseFactory.get_filter_parameters(request.args, model_class)
        model_objects = (
            model_class.base_queryset()
            .filter(**filter_params)
            .order_by(order_by)
            .only(*model_class.get_base_attributes())
        )
        return model_objects

    @classmethod
    def build_base(cls, model_class):
        base = cls.factory_method()
        model_objects = BaseFactory.get_model_objects(model_class)
        return base.create_base(model_objects)

    @abstractmethod
    def factory_method(self):
        raise NotImplementedError