
import pydicom


def json_to_dcm(tags_dict) -> pydicom.Dataset:
    dataset = pydicom.Dataset()
    for key, value in tags_dict.items():
        if key.endswith("Sequence"):
            if isinstance(value, dict):
                values = [json_to_dcm(value)]
            elif isinstance(value, list):
                values = [json_to_dcm(v) for v in value]
            else:
                print("Wrong tags.")
                continue
            dataset.__setattr__(key, values)
        else:
            dataset.__setattr__(key, value)
    return dataset


if __name__ == "__main__":
    tags_dict = {
        "ValueType": "CONTAINER",
        "ContributingEquipmentSequence": {
            "CodeValue": 126000,
            "CodingSchemeDesignator": "DCM",
            "CodeMeaning": "Imaging Measurement Report",
        },
        "ContentSequence": [
            {
                "RelationshipType": "HAS CONCEPT MOD",
                "ValueType": "CODE",
            },
            {
                "RelationshipType": "CONTAINS",
                "ValueType": "CONTAINER",
            },
        ],
    }
    ds = json_to_dcm(tags_dict)
