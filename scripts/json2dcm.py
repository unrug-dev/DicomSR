"""
Usage:
python json2dcm.py path/to/file.json


Example:
json_content = {
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
dicom = _json_to_dataset(json_content)
"""

import pydicom
import sys
import json



def _json_to_base_dicom(tags_dict: dict) -> pydicom.Dataset:
    """ Initialize an base DICOM with a file meta dataset"""
    file_meta = pydicom.FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = tags_dict["SOPClassUID"]
    file_meta.MediaStorageSOPInstanceUID = tags_dict["SOPInstanceUID"]
    file_meta.ImplementationClassUID = tags_dict.pop("ImplementationClassUID")
    file_meta.ImplementationVersionName = tags_dict.pop("ImplementationVersionName")
    file_meta.SourceApplicationEntityTitle = tags_dict.pop(
        "SourceApplicationEntityTitle"
    )
    file_meta.TransferSyntaxUID = "ExplicitVRLittleEndian"
    file_meta.FileMetaInformationGroupLength = len(file_meta)
    dicom = FileDataset(BytesIO(), {}, file_meta=file_meta, preamble=b"\0" * 128)
    validate_file_meta(file_meta=dicom.file_meta, enforce_standard=True)    
    return dicom


def _json_to_dataset(
    tags_dict,
    dataset: Optional[pydicom.Dataset] = None,
) -> pydicom.Dataset:
    if dataset is None:
        dataset = pydicom.Dataset()
    for key, value in tags_dict.items():
        if key.endswith("Sequence"):
            if isinstance(value, dict):
                value = [json_to_dataset(value)]
            elif isinstance(value, list):
                value = [json_to_dataset(v) for v in value]
            else:
                print("Wrong tags.")
                continue
        dataset.__setattr__(key, value)
    return dataset


def json_to_dicom(tags_dict) -> pydicom.Dataset:
    dicom = _json_to_base_dicom(tags_dict)
    dicom = _json_to_dataset(tags_dict, dicom)
    validate_file_meta(file_meta=dicom.file_meta, enforce_standard=True)
    return dicom
    

if __name__ == "__main__":
    with open(sys.argv[0]) as f:
        json_dcm = json.load(f)
    dicom = json_to_dicom(json_dcm)
    dicom.save_as(sys.argv[1] + ".dcm")
