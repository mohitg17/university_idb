from idb_app.models import University, City, Major
from idb_app.mongo import Connector
import pandas as pd

Connector.load_database_creds()
Connector.connect_prod_database()


def get_cip_reference(definition):
    if "Instructional content is defined" in definition:
        cip_reference = definition.split(" ")[-1].strip(".")
    else:
        cip_reference = definition.split(" ")[-3]
    return cip_reference


cip_data = pd.read_csv("CIPCode2010.csv")
majors = Major.objects(cip_code__exists=True, cip_family__exists=False)

for major in majors:
    print(major.name)
    data = cip_data.loc[cip_data["CIPTitle"] == major.name]
    try:
        cip_family = int(data.iloc[0]["CIPFamily"])
        definition = str(data.iloc[0]["CIPDefinition"])
    except IndexError:
        cip_family = 0
        definition = "unavailable"
    if (
        "Instructional content is defined" in definition
        or "Instructional content for this group of programs" in definition
    ):
        cip_reference = get_cip_reference(definition)
        try:
            definition = cip_data.loc[cip_data["CIPCode"] == float(cip_reference)].iloc[
                0
            ]["CIPDefinition"]
        except ValueError:
            definition = "unavailable"
        if (
            "Instructional content is defined" in definition
            or "Instructional content for this group of programs" in definition
        ):
            try:
                definition = cip_data.loc[
                    cip_data["CIPCode"] == float(cip_reference)
                ].iloc[1]["CIPDefinition"]
            except IndexError:
                pass
            if (
                "Instructional content is defined" in definition
                or "Instructional content for this group of programs" in definition
            ):
                definition = "unavailable"
    print(cip_family)
    print(definition)
    major["description"] = definition
    major["cip_family"] = cip_family
    major.save()
