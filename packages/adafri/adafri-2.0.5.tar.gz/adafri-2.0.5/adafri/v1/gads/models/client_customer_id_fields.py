from dataclasses import dataclass
from  ....utils.utils import BaseFieldsClass
from google.cloud.firestore_v1.document import Timestamp
from google.api_core.datetime_helpers import DatetimeWithNanoseconds
@dataclass
class ClientCustomerIdFields(BaseFieldsClass):
    accountId = "accountId"
    customerId = "customerId"
    name = "name"
    enabled = "enabled"
    owner = "owner"
    creationDate = "creationDate"
    creationDateString = "creationDateString"
    createdAt = "createdAt"
    isDefault = "isDefault"
    def __init__(self, **kwargs):
        self.class_fields_props = ClientCustomerIdFieldsProps
        super().__init__(**kwargs)

ClientCustomerIdFieldsProps = {
    ClientCustomerIdFields.accountId: {
        "internal": True,
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    ClientCustomerIdFields.name: {
        "internal": True,
        "type": str,
        "required": True,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    ClientCustomerIdFields.customerId: {
        "internal": True,
        "type": str,
        "required": True,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    ClientCustomerIdFields.owner: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": True,
        "editable": False,
        "interactive": True,
        "pickable": False,
        "default_value": None
    },
    ClientCustomerIdFields.enabled: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": True
    },
    ClientCustomerIdFields.isDefault: {
        "internal": True,
        "type": bool,
        "required": False,
        "mutable": True,
        "editable": True,
        "interactive": True,
        "pickable": True,
        "default_value": False
    },
    ClientCustomerIdFields.createdAt: {
        "internal": False,
        "type": [int, str, Timestamp, DatetimeWithNanoseconds],
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    ClientCustomerIdFields.creationDate: {
        "internal": True,
        "type": int,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
    ClientCustomerIdFields.creationDateString: {
        "internal": True,
        "type": str,
        "required": False,
        "mutable": False,
        "editable": False,
        "interactive": True,
        "pickable": True,
        "default_value": None
    },
}


CLIENT_CUSTOMER_ID_PICKABLE_FIELDS = ClientCustomerIdFields(fields_props=ClientCustomerIdFieldsProps).filtered_keys('pickable', True)
