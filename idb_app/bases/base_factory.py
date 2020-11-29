from idb_app.bases import UniversityBase, CityBase, MajorBase
from flask import request

class BaseFactory:

    @classmethod
    def get_model_from_string(cls, s: str):
        s_normalized = s.lower()
        model_class = {
            "major": MajorBase(),
            "university": UniversityBase(),
            "city": CityBase(),
        }.get(s_normalized)
        if model_class is None:
            raise ValueError(f"{s} is not a known model class")
        return model_class

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
    def create_base(cls, model_name, model_class):
        model_objects = BaseFactory.get_model_objects(model_class)
        base_class = BaseFactory.get_model_from_string(model_name)
        return base_class.create_base(model_objects)