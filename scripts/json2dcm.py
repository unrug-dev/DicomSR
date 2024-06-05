"""
Usage:
python json2dcm.py path/to/file.json


Example:
json_dicom = {
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
dicom = json_to_dcm(json_dicom)
"""

import pydicom
import sys
import json


def json_to_dcm(tags_dict) -> pydicom.Dataset:
    dataset = pydicom.Dataset()
    for key, value in tags_dict.items():
        if key.endswith("Sequence"):
            if isinstance(value, dict):
                value = [json_to_dcm(value)]
            elif isinstance(value, list):
                value = [json_to_dcm(v) for v in value]
            else:
                print("Wrong tags.")
                continue
        dataset.__setattr__(key, value)
    return dataset


if __name__ == "__main__":
    with open(sys.argv[0]) as f:
        json_dcm = json.load(f)
    dcm = json_to_dcm(json_dcm)
    dcm.save_as(sys.argv[1] + ".dcm")
