import time

from .APIKeys import *
from .Consts import PID_FACTOR
from ..Utils.Errors import ValidationError


class ProposalBuilder():    
    def __init__(self):
        super().__init__()
        self.proposal = {PROPOSAL_ID: "P{:09.0f}".format(time.time() * PID_FACTOR)}
    
    def args(self, args):
        return self.owner_group(args.ownergroup).\
            access_groups(args.accessgroups)

    def proposal_id(self, proposal_id : str):
        self.proposal[PROPOSAL_ID] = "P{}".format(proposal_id)
        return self

    def access_groups(self, access_groups : list):
        self.proposal[ACCESS_GROUPS] = access_groups
        return self

    def owner_group(self, owner_group : str):
        self.proposal[OWNER_GROUP] = owner_group
        return self

    def email(self, email : str):
        self.proposal[EMAIL] = email
        return self

    def firstname(self, firstname : str):
        self.proposal[FIRSTNAME] = firstname
        return self

    def lastname(self, lastname : str):
        self.proposal[LASTNAME] = lastname
        return self

    def pi_email(self, email : str):
        self.proposal[PI_EMAIL] = email
        return self

    def pi_firstname(self, firstname : str):
        self.proposal[PI_FIRSTNAME] = firstname
        return self

    def pi_lastname(self, lastname : str):
        self.proposal[PI_LASTNAME] = lastname
        return self

    def title(self, title : str):
        self.proposal[TITLE] = title
        return self

    def abstract(self, abstract : str):
        self.proposal[ABSTRACT] = abstract
        return self

    def start_time(self, time : str):
        self.proposal[START_TIME] = time
        return self

    def end_time(self, time : str):
        self.proposal[END_TIME] = time
        return self

    def measured_period_list(self, measured_period_list):
        self.proposal[MEASURED_PERIOD_LIST] = measured_period_list
        return self

    def _invalid(self):
        invalids=set()
        
        # Illegal keys
        for key in self.proposal.keys():
            if key not in PROPERTIES:
                invalids.add(key)
        
        # Required keys
        for key in REQUIRED_PROPERTIES_PROPOSAL:
            if key not in self.proposal.keys():
                invalids.add(key)
                
        return invalids
            
    def build(self):
        invalids = self._invalid()
        if invalids:
            raise ValidationError(invalids)
        return self.proposal
