from dataclasses import dataclass
from ...base.firebase_collection import FirebaseCollectionBase, getTimestamp
from typing import Any
from ....utils import ApiResponse, StatusCode, ResponseStatus, Error
from  ....utils.utils import DictUtils, BaseFieldsClass, BaseClass, init_class_kwargs,get_object_model_class
from .client_customer_id_fields import ClientCustomerIdFields, ClientCustomerIdFieldsProps, CLIENT_CUSTOMER_ID_PICKABLE_FIELDS
from adafri.v1.account import Account
from datetime import datetime
from adafri.utils import DateUtils, interger
from google.cloud.firestore_v1.document import DocumentReference
import os

COLLECTION_NAME = os.environ.get('GADS_CLIENT_CUSTOMER_ID_COLLECTION', 'clients-customer-id');
@dataclass(init=False)
class ClientCustomerId(FirebaseCollectionBase):
    id: str
    accountId: str
    owner: str
    customerId: str
    isDefault: bool
    name: str
    enabled: bool
    createdAt: Any
    creationDate: int
    creationDateString: str
    def __init__(self, customer=None, collection_name=COLLECTION_NAME, **kwargs):
        (cls_object, keys, data_args) = init_class_kwargs(self, customer, CLIENT_CUSTOMER_ID_PICKABLE_FIELDS, ClientCustomerIdFieldsProps, collection_name, ['customerId'], **kwargs)
        super().__init__(**data_args);
        for key in keys:
            setattr(self, key, cls_object[key]) 
    def to_dict(self, field=None):
        createdAt = None
        if getattr(self, 'createdAt', None) is not None: 
            createdAt = DateUtils.convert_firestore_timestamp_to_str(self.createdAt)
        return DictUtils.remove_none_values({
            "accountId": self.accountId,
            "customerId": self.customerId,
            "name": self.name,
            "enabled": self.enabled,
            "isDefault": self.isDefault,
            "createdAt": createdAt,
            "creationDate": self.creationDate,
            "creationDateString": self.creationDateString
        })
    
    @staticmethod
    def generate_model(_key_="default_value"):
        campaign = {};
        props = ClientCustomerIdFieldsProps
        for k in DictUtils.get_keys(props):
            campaign[k] = props[k][_key_];
        return campaign;
    # def query(self, query_params: list, first=False, limit=None):
    #     result = [];
    #     query_result = self.custom_query(query_params, first=first, limit=limit, collection_name=self.collection_name)
    #     # print('query result', query_result)
    #     if bool(query_result):
    #         if first:
    #             return ClientCustomerId.from_dict(customer=query_result, db=self.db, collection_name=self.collection_name)
    #         else:
    #             for doc in query_result:
    #                 result.append(ClientCustomerId.from_dict(customer=doc, db=self.db, collection_name=self.collection_name))
    #             return result
    #     if first:
    #             return None
    #     return [];
    def get(self):
        if getattr(self, 'customerId', None) is None:
            return None;
        query = self.query(self, 'customer', [{"key": "customerId", "comp": "==", "value": self.customer_id}], True)
        if query is None:
            return None;
        result: ClientCustomerId = query
        return result;
    @staticmethod
    def from_dict(customer: Any = None, db=None, collection_name=COLLECTION_NAME) -> 'ClientCustomerId':
        cls_object, keys = get_object_model_class(customer, ClientCustomerId, ClientCustomerIdFieldsProps);
        return ClientCustomerId(cls_object, db=db, collection_name=collection_name)
    
    def getDefault(self)->'list[ClientCustomerId]':
        query = self.query(self, 'customer', [{"key": "isDefault", "comp": "==", "value": True}])
        if query is None:
            return [];
        result: list[ClientCustomerId] = query
        return result;
    def create(self, accountId, **kwargs):
        data_dict = DictUtils.pick_fields(kwargs, ClientCustomerIdFields(fields_props=ClientCustomerIdFieldsProps).filtered_keys('mutable', True));
        customer_model = ClientCustomerId().from_dict(DictUtils.merge_dict(data_dict, ClientCustomerId().generate_model()));
        if bool(customer_model.to_json()) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Empty request","INVALID_REQUEST", 1))
        
        if bool(customer_model.customerId) is False or len(customer_model.customerId) != 10 or interger(customer_model.customerId) is None:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Invalid or missing customerId","INVALID_REQUEST", 1));
        
        account = None
        if accountId is not None:
            account = Account(accountId).get();
        if account is None:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Account not found","INVALID_REQUEST", 1));
    
        customer_model.accountId = account.id;
        customer_model.owner = account.owner
        customerId = customer_model.customerId

        docs = ClientCustomerId().query(self, "customer", query_params=[{"key": "accountId", "comp": "==", "value": customer_model.accountId}, {"key": "customerId", "comp": "==", "value": customerId}]);
        found_customer = [];
        if len(docs) > 0:
            for doc in docs:
                found_customer.append(ClientCustomerId.from_dict(doc.to_dict()).to_json());
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Account with name {customer_model.email} already exist","INVALID_REQUEST", 1));
    
        try:
            doc: DocumentReference = ClientCustomerId().collection().document()
            customer_model.id = doc.id;
            if bool(customer_model.isDefault) is False:
                customer_model.isDefault = False
            creationDate = datetime.now()
            creationDateN = int(creationDate.timestamp()) * 1000
            creationDateString = creationDate.isoformat();
            creationDateString = creationDate.strftime("%d %B %Y à %H:%M:%S UTC");
            customer_model.creationDate = creationDateN;
            customer_model.creationDateString = creationDateString;
            doc.set({**customer_model.to_json(), "createdAt": getTimestamp()}, merge=True)
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, DictUtils.remove_none_values(DictUtils.filter_by_fields(customer_model.to_json(), CLIENT_CUSTOMER_ID_PICKABLE_FIELDS)), None);
        except Exception as e:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(str(e),"INVALID_REQUEST", 1));
