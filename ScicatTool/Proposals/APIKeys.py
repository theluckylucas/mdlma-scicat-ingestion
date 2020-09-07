from ..REST.CommonKeys import *


PROPOSAL_ID = "proposalId"
PI_EMAIL = "pi_email"
PI_FIRSTNAME = "pi_firstname"
PI_LASTNAME = "pi_lastname"
EMAIL = "email"
FIRSTNAME = "firstname"
LASTNAME = "lastname"
TITLE = "title"
ABSTRACT = "abstract"
START_TIME = "startTime"
END_TIME = "endTime"
MEASURED_PERIOD_LIST = "MeasurementPeriodList"


PROPERTIES = {
    PROPOSAL_ID:    "Globally unique identifier of a proposal, eg. PID-prefix/internal-proposal-number. PID prefix is auto prepended",
    PI_EMAIL:       "Email of principal investigator",
    PI_FIRSTNAME:   "First name of principal investigator",
    PI_LASTNAME:    "Last name of principal investigator",
    EMAIL:          "Email of main proposer",
    FIRSTNAME:      "First name of main proposer",
    LASTNAME:       "Last name of main proposer",
    TITLE:          "string",
    ABSTRACT:       "string",
    START_TIME:     "string($date-time)",
    END_TIME:       "string($date-time)",
    MEASURED_PERIOD_LIST:   "Embedded information used inside proposals to define which type of experiment as to be pursued where (at which intrument) and when.",
    OWNER_GROUP:    COMMON_PROPERTIES[OWNER_GROUP],
    ACCESS_GROUPS:  COMMON_PROPERTIES[ACCESS_GROUPS],
}


# PROPOSAL_ID, CREATED_AT, CREATED_BY, UPDATED_AT, UPDATED_BY will be automatically assigned by Scicat API / database
REQUIRED_PROPERTIES_PROPOSAL = [PROPOSAL_ID, EMAIL, OWNER_GROUP]