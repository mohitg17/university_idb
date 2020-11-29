from idb_app.bases import AbstractBase
from idb_app.models import City
from flask import url_for

class CityBase(AbstractBase):
    title = "Cities"
    model_type = type = "city"
    filter_buttons = City.get_filtering_buttons()
    filter_text = City.get_filtering_text()
    sort_buttons = City.get_sort_buttons()
    
    def build_instances(self, query_set):
        instances = []
        for city in query_set:
            instance = {
                "model_type": "city",
                "page_url": url_for("instance", model_name="city", object_id=city.id),
                "image_url": url_for(
                    "static", filename=(city.name + "_" + city.state + ".png")
                ),
                "name": str(city),
                "id": city.id,
                "attribute_1": {"name": "Population",
                                "value": city.population if not city.population == 0 else "Unavailable"},
                "attribute_2": {"name": "Community Type", "value": city.community_type},
                "attribute_3": {
                    "name": "Area (square miles)",
                    "value": city.area if not city.area == 0 else "Unavailable",
                },
            }
            instances.append(instance)
        return instances