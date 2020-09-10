LOCATION = "DESY/PETRA3/P05"  # Default location added to any P05 raw dataset
P05_PREFIX = "P05"

PATH_GPFS_P05 = "/asap3/petra3/gpfs/p05/{}/data/{}"
JSON_META_EXP = "beamtime-metadata-{}.json"
TEXT_META_EXP = "beamtime-metadata-{}.txt"
LOG_SUFFIX = "scan.log"

PROCESSED = "processed"
RAW = "raw"

FLAT_CORRECTED = "flat_corrected"
RECO = "reco"
SINO = "sino"
RECO_PHASE = "reco_phase"
SINO_PHASE = "sino_phase"
PHASE_MAP = "phase_map"
POSTPROCESSING = [FLAT_CORRECTED, RECO, SINO, RECO_PHASE, SINO_PHASE, PHASE_MAP]

RAW_BIN = "rawBin"
BINNING = "binning"

KEYWORDS = ["synchrotron", "beamline"]  # Default keywords always added to any P05 dataset