LOCATION = "MHH/ZTL"
SITE_PREFIX = "ZTL"
SOURCE_PATH = "/home/lucaschr/TemporalStorage/MHH-ZTL/"
PATH_MR = "MR"
PATH_CT = "CT"
LOG_FILENAMES = []
LOG_SUFFIX = ".log"
KEYWORDS = ["rodent", "tomography"]  # Default keywords always added to any dataset beside other keywords
DATASET_NAME_PATTERN = "{}/{}/{}/{}"
FILENAME_IGNORE_PATTERN = ["_ref", "_dar"]
DICOM_TAGS = ["ImageType", "StudyDate", "Modality", "Manufacturer", "InstitutionName", "SeriesDescription", "ManufacturerModelName", "PatientName", "PatientID", "PatientSpeciesDescription", "ResponsibleOrganization", "ScanningSequence", "SequenceVariant", "ScanOptions", "MRAcquisitionType", "SequenceName", "SliceThickness", "RepetitionTime", "EchoTime", "MagneticFieldStrength", "SpacingBetweenSlices", "NumberOfPhaseEncodingSteps", "ProtocolName", "AcquisitionMatrix", "FlipAngle", "PatientPosition", "ImagePositionPatient", "ImageOrientationPatient", "ImagesInAcquisition", "PhotometricInterpretation", "Rows", "Columns", "PixelSpacing", "BitsAllocated", "BitsStored"]