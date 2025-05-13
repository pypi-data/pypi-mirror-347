from dataclasses import dataclass
from typing import Any
from  ....utils.utils import BaseFieldsClass
from google.cloud.firestore_v1.document import Timestamp
from google.api_core.datetime_helpers import DatetimeWithNanoseconds


@dataclass
class BaseCampaignFields(BaseFieldsClass):
    id = "id"
    id_campagne = "id_campagne"
    name = "name"
    objective = "objective"
    adChannel = "adChannel"
    status = "status"
    startDate = "startDate"
    endDate = "endDate"
    startDateFormattedGoogle = "startDateFormattedGoogle"
    endDateFormattedGoogle = "endDateFormattedGoogle"
    areaTargetedOption = "areaTargetedOption"
    areaExcludedOption = "areaExcludedOption"
    budget = "budget"
    budgetId = "budgetId"
    dailyBudget = "dailyBudget"
    bid = "bid"
    urlPromote = "urlPromote"
    strategie = "strategie"
    deliveryMethod = "deliveryMethod"
    trackingTemplate = "trackingTemplate"
    finalUrlSuffix = "finalUrlSuffix"
    urlCustomParameters = "urlCustomParameters"
    clientCustomerId = "clientCustomerId"
    servingStatus = "servingStatus"
    owner = "owner"
    createdAt = "createdAt"
    createdBy = "createdBy"
    endedAt = "endedAt"
    isPayed = "isPayed"
    isEnded = "isEnded"
    type = "type"
    accountId = "accountId"
    is_removed = "is_removed"
    targetedLocations = "targetedLocations"
    excludedLocations = "excludedLocations"
    ages = "ages"
    genders = "genders"
    devicesTargeted = "devicesTargeted"
    devicesExcluded = "devicesExcluded"
    adsSchedules = "adsSchedules"
    budgetEnded = "budgetEnded"
    publish = "publish"
    publishing = "publishing"
    ad_group_id = "ad_group_id"
    ad_group_id_firebase = "ad_group_id_firebase"
    publicationDate = "publicationDate"
    provider = "provider"
    isComplete = "isComplete"

    def __init__(self, **kwargs):
        self.class_fields_props = BaseCampaignFieldsProps
        super().__init__(**kwargs)



BaseCampaignFieldsProps = {
    BaseCampaignFields.id: {
        "internal": False,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.name: {
        "internal": True,
        "type": str,
        "required": True,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.status: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": "ENABLED"
    },
    BaseCampaignFields.startDate: {
         "internal": True,
        "type": str,
        "required": True,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.endDate: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.startDateFormattedGoogle: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": False,
        "default_value": None
    },
    BaseCampaignFields.endDateFormattedGoogle: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": False,
        "default_value": None
    },
    BaseCampaignFields.strategie: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": "CPM"
    },
    BaseCampaignFields.bid: {
        "internal": True,
        "type": float,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": False,
        "default_value": 0.1
    },
    BaseCampaignFields.budget: {
        "internal": True,
        "type": [int,float],
        "required": True,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": 4
    },
    BaseCampaignFields.dailyBudget: {
        "internal": True,
        "type": [int,float],
        "required": True,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": 4
    },
    BaseCampaignFields.budgetId: {
        "internal": True,
        "type": int,
        "required": False,
        "mutable": False,
        "editable": True,
        "interactive": True,
        "pickable": False,
        "default_value": 0
    },
    BaseCampaignFields.urlPromote: {
        "internal": True,
        "type": str,
        "required": True,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.objective: {
        "internal": True,
        "type": dict,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": {"obj_id": "6"}
    },
    BaseCampaignFields.adChannel: {
        "type": dict,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": {"obj_id": 'display'}
    },
    BaseCampaignFields.provider: {
        "internal": True,
        "type": str,
        "required": True,
        "mutable": False,
        "editable": True,
        "interactive": True,
        "pickable": False,
        "default_value": None
    },
    BaseCampaignFields.type: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.owner: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.accountId: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.id_campagne: {
        "internal": True,
        "type": int,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": 0
    },
    BaseCampaignFields.ad_group_id: {
        "internal": True,
        "type": int,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": 0
    },
    BaseCampaignFields.ad_group_id_firebase: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.isEnded: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": False,
        "default_value": False
    },
    BaseCampaignFields.isPayed: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": False,
        "default_value": False
    },
    BaseCampaignFields.is_removed: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": False,
        "default_value": False
    },
    BaseCampaignFields.finalUrlSuffix: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.trackingTemplate: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.urlCustomParameters: {
        "type": list,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": ""
    },
    BaseCampaignFields.publish: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": False,
        "editable": True,
        "interactive": True,
        "pickable": False,
        "default_value": False
    },
    BaseCampaignFields.publishing: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": False,
        "editable": True,
        "interactive": True,
        "pickable": False,
        "default_value": False
    },
    BaseCampaignFields.isComplete: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": False,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": False
    },
    BaseCampaignFields.budgetEnded: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": False,
        "editable": True,
        "interactive": True,
        "pickable": False,
        "default_value": False
    },
    BaseCampaignFields.publicationDate: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": False,
        "default_value": ""
    },
    BaseCampaignFields.areaTargetedOption: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.areaExcludedOption: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.ages: {
        "internal": True,
        "type": list,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": []
    },
    BaseCampaignFields.genders: {
        "internal": True,
        "type": list,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": []
    },
    BaseCampaignFields.servingStatus: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": True,
        "interactive": True,
        "pickable": False,
        "default_value": None
    },
    BaseCampaignFields.clientCustomerId: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.createdBy: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": False,
        "default_value": None
    },
    BaseCampaignFields.createdAt: {
        "type": [int, str, Timestamp, DatetimeWithNanoseconds],
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    BaseCampaignFields.adsSchedules: {
        "internal": True,
        "type": list,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": []
    },
    BaseCampaignFields.deliveryMethod: {
         "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": False,
        "default_value": None
    },
    BaseCampaignFields.targetedLocations: {
        "internal": True,
        "type": list,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": []
    },
    BaseCampaignFields.excludedLocations: {
        "internal": True,
        "type": list,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": []
    },
    BaseCampaignFields.devicesTargeted: {
        "internal": True,
        "type": list,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": []
    },
    BaseCampaignFields.devicesExcluded: {
        "internal": True,
        "type": list,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": []
    }
}


STANDARD_FIELDS = BaseCampaignFields(fields_props=BaseCampaignFieldsProps).filtered_keys('pickable', True)
BASE_CAMPAIGN_PICKABLE_FIELDS = BaseCampaignFields(fields_props=BaseCampaignFieldsProps).filtered_keys('pickable', True) + ['objective.primary']
