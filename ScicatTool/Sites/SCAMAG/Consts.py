LOCATION = "MHH/Syntellix"
SITE_PREFIX = "MHH-Syntellix"
SOURCE_PATH = "/nfs/fs/hzg/mdlma/data/MHH-SCAMAG/"
LOG_FILENAMES = []
LOG_SUFFIX = ".log"
KEYWORDS = ["carpus", "wrist", "tomography", "longitudinal", "in-vivo"]  # Default keywords always added to any dataset beside other keywords
DATASET_NAME_PATTERN = "{}/{}/{}/{}/{}/{}"
FILENAME_IGNORE_PATTERN = ["_ref", "_dar"]
DICOM_TAGS = ['ImageType', 'ManufacturerModelName', 'Manufacturer', 'StudyID', 'NumberOfAverages', 'SamplesPerPixel', 'ScanningSequence', 'WindowCenter', 'WindowWidth', 'WindowCenterWidthExplanation', 'SliceThickness', 'SmallestImagePixelValue', 'LargestImagePixelValue', 'InPlanePhaseEncodingDirection', 'ScanOptions', 'RequestedProcedureCodeSequence', 'Modality', 'ProcedureCodeSequence', 'SAR', 'SpacingBetweenSlices', 'HighBit', 'EchoTrainLength', 'PhotometricInterpretation', 'MRAcquisitionType', 'MagneticFieldStrength', 'BitsStored', 'SoftwareVersions', 'SequenceVariant', 'PercentPhaseFieldOfView', 'TransmitCoilName', 'NumberOfPhaseEncodingSteps', 'EchoNumbers', 'EchoTime', 'PixelSpacing', 'PercentSampling', 'FlipAngle', 'Rows', 'Columns', 'PatientID', 'BitsAllocated', 'SeriesNumber', 'VariableFlipAngleFlag', 'PixelBandwidth', 'RepetitionTime', 'PatientSex', 'DistanceSourceToDetector', 'FilterType', 'RescaleType', 'GeneratorPower', 'EstimatedDoseSaving']
PROPOSAL_ABSTRACT = "Data of the hand (carpus) from MHH (Department of Plastic, Aesthetic, Hand and Reconstructive Surgery) with 6 in-vivo measurements (before implant, 3 MR follow-ups, 1 multi-modal follow-up CT/MR): Pre-surgery, 6w follow-up MR, 3m follow-up MR/CT, 6m follow-up MR, 12m follow-up MR"
PROPOSAL_TITLE = "MHH/Syntellix SCAMAG"
PROPOSAL_ID = "2019-SCAMAG"
PROPOSAL_START = "2019-08-02"
PROPOSAL_END = "2020-11-02"
PAT1_SAMPLE_ID = "S1"
PAT1_DATE_MAPPING = {
    "STD00001": "2019-02-08",
    "surgery": "2019-02-11",
    "STD00002": "2019-03-22",
    "STD00003": "2019-05-10",
    "STD00004": "2019-05-13",
    "STD00005": "2019-08-09",
    "STD00006": "2020-02-11"
}
PAT1_DAY_MAPPING = {
    "STD00001": "BL",
    "STD00002": "6w",
    "STD00003": "3m",
    "STD00004": "3m",
    "STD00005": "6m",
    "STD00006": "12m"
}
