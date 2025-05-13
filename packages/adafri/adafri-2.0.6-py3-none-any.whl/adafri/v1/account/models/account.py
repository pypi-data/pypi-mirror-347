from ...base.firebase_collection import FirebaseCollectionBase, getTimestamp
from ....utils import (DictUtils, get_object_model_class, init_class_kwargs, BaseClass, get_request_fields, RequestFields)
from ....utils.response import ApiResponse, Error, ResponseStatus, StatusCode
from .account_fields import AccountStatus, AccountFields, AccountLinkFields, AccountLinkFieldProps, AccountFieldProps, STANDARD_FIELDS, ACCOUNT_PICKABLE_FIELDS, LINK_STANDARD_FIELDS, ACCOUNT_COLLECTION, ACCOUNT_LINK_COLLECTION
from typing import Any
from dataclasses import dataclass
import pydash
from adafri.v1.user import User
from google.cloud.firestore_v1.document import DocumentReference
from datetime import datetime
from time import time
def filter_account_request_fields(fields, default_fields = ACCOUNT_PICKABLE_FIELDS):
    request_fields = get_request_fields(fields, default_fields, [default_fields[0]])
    if request_fields is None or bool(request_fields) is False:
        request_fields = [default_fields[0]]
    return request_fields

@dataclass(init=False)
class Account(FirebaseCollectionBase):
    id: str
    aacid: str
    account_value: int
    creationDate: int
    creationDateString: str
    name: str
    owner: str
    owner_email: str
    status: str
    totalClics: int
    totalCosts: int
    totalImpressions: int
    usedPackTest: bool
    __baseFields: AccountFieldProps

    def __init__(self,_account=None, **kwargs):
        account = _account
        if type(_account) is str:
            account = {"id": _account}
        (cls_object, keys, data_args) = init_class_kwargs(self, account, STANDARD_FIELDS, AccountFieldProps, ACCOUNT_COLLECTION, ['id'], **kwargs)
        super().__init__(**data_args);
        for key in keys:
            setattr(self, key, cls_object[key]) 


    @staticmethod
    def generate_model(_key_="default_value"):
        user = {};
        props = AccountFieldProps
        for k in DictUtils.get_keys(props):
            user[k] = props[k][_key_];
        return user;

    @staticmethod
    def from_dict(account: Any, db=None, collection_name=None) -> 'Account':
        cls_object, keys = get_object_model_class(account, Account, AccountFieldProps);
        if AccountFields.aacid in cls_object and bool(cls_object[AccountFields.aacid]) is False:
            if AccountFields.id in cls_object and bool(cls_object[AccountFields.id]):
                cls_object[AccountFields.aacid] = cls_object[AccountFields.id]
        _account = Account(cls_object, db=db, collection_name=collection_name)
        return _account
    
    def to_dict(self):
        return {
            "id": self.id,
            "aacid": self.aacid,
            "account_value": self.account_value,
            "creationDate": self.creationDate,
            "creationDateString": self.creationDateString,
            "name": self.name,
            "owner": self.owner,
            "owner_email": self.owner_email,
            "status": self.status,
        }
    
    def get(self, fields=None):
        _id = getattr(self, 'aacid', None);
        if bool(_id) is False:
            if self.id is None:
                return None;
            _id = self.id;
        if bool(id) is None:
            return None;
        request_fields = filter_account_request_fields(fields)
        doc = self.document_reference().get();
        if doc.exists is False:
            return None;
        data = {"id": doc.id, **doc.to_dict()}
        return Account.from_dict(account=Account.from_dict(account=data).to_dict(),  db=self.db, collection_name=self.collection_name);


    def getUserAccountsLinked(self, uid, fields=None):
        accounts_link = []
        request_fields = filter_account_request_fields(fields)
        # print('account query', account)
        links_ids = []
        accounts_links_ = AccountLink(account_link=None).query(AccountLink, "account_link", query_params=[{"key": "target", "comp": "==", "value": uid}])
        for account in accounts_links_:
            links_ids.append(account.linked_account.account.id)
        accounts_batch = self.queryBatch(Account, "account", links_ids)
        for account in accounts_batch:
            accounts_link.append(account)
            # print(account.linked_account.account.id)
        return accounts_link
    def getUserAccounts(self, uid, includeLinks = True, fields=None):
        accounts = []
        accounts_link = []
        accounts_ = self.query(Account, "account", query_params=[{"key": "owner", "comp": "==", "value": uid}])
        request_fields = filter_account_request_fields(fields)
        # print('account query', account)
        for account in accounts_:
            accounts.append(account)
        if includeLinks is True:
            accounts_link.extend(self.getUserAccountsLinked(uid))
            # print(account.linked_account.account.id)
        return accounts, accounts_link
        # accounts_link.append(account.to_json(['id']))
    def getByUserId(self,id):
        accounts = [];
        docs = self.collection().where('owner','==',id).get();
        for doc in docs:
            data = doc.to_dict();
            data['id'] = doc.id;
            data['aacid'] = doc.id;
            print(data)
            accounts.append(Account.from_dict(data))
        return accounts;
    # def query(self, query_params: list, first=False, limit=None):
    #     result = [];
    #     query_result = self.custom_query(query_params, first=first, limit=limit)
    #     if bool(query_result):
    #         if first:
    #             return Account.from_dict(account=query_result, db=self.db, collection_name=self.collection_name)
    #         else:
    #             for doc in query_result:
    #                 result.append(Account.from_dict(account=doc, db=self.db, collection_name=self.collection_name))
    #             return result
    #     if first:
    #             return None
    #     return [];

    def getAccount(self):
            id = self.id
            if bool(id) is False:
                if bool(self.aacid) is False:
                    return None;
                id = self.aacid
            account = self.get(self.id);
            if account is None:
                return None;
            return account.to_dict();
    def create(self, **kwargs):
        data_dict = DictUtils.pick_fields(kwargs, AccountFields(fields_props=AccountFieldProps).filtered_keys('mutable', True));
        account_model = Account().from_dict(DictUtils.merge_dict(data_dict, Account.generate_model()));
        if bool(account_model.to_json()) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Empty request","INVALID_REQUEST", 1))
        
        user = None
        if 'uid' in kwargs:
            user = User(kwargs['uid']).get();
        if user is None:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("User not found","INVALID_REQUEST", 1));
    
        account_model.owner = user.id;
        account_model.owner_email = user.email;
        name = account_model.name

        if bool(name) is False:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error("Password required","INVALID_REQUEST", 1));
        docs = Account().query(self, "account", query_params=[{"key": "owner", "comp": "==", "value": account_model.owner}, {"key": "name", "comp": "==", "value": name}]);
        found_users = [];
        if len(docs) > 0:
            for doc in docs:
                found_users.append(Account.from_dict(doc.to_dict()).to_json());
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Account with name {account_model.email} already exist","INVALID_REQUEST", 1));
    
    
        try:
            doc: DocumentReference = Account().collection().document()
            account_model.aacid = doc.id;
            account_model.id = doc.id;
            account_model.status = AccountStatus.ACTIVE;
            creationDate = datetime.now()
            creationDateN = int(creationDate.timestamp()) * 1000
            creationDateString = creationDate.isoformat();
            creationDateString = creationDate.strftime("%d %B %Y à %H:%M:%S UTC");
            account_model.creationDate = creationDateN;
            account_model.creationDateString = creationDateString;
            doc.set({**account_model.to_json(), "createdAt": getTimestamp()}, merge=True)
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, DictUtils.filter_by_fields(account_model.to_json(), ['id', 'aacid', 'name']), None);
        except Exception as e:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(str(e),"INVALID_REQUEST", 1));

    def update(self, data):
        try:
            last_value = self.to_json();
            filtered_value = pydash.pick(data, AccountFields.filtered_keys('editable', True));
            new_value = DictUtils.merge_dict(filtered_value, self.to_json());
            changed_fields = DictUtils.get_changed_field(last_value, new_value);
            data_update = DictUtils.dict_from_keys(filtered_value, changed_fields);
            if bool(data_update) is False:
                return None;
            if 'account_value' in data_update:
                data_update['account_value'] = float(str(data_update['account_value']))
            self.document_reference().set(data_update, merge=True)
            return DictUtils.dict_from_keys(self.getAccount(), changed_fields);
        except Exception as e:
            print(e)
            return None;

    def update_account_value(self, params):
        if 'value' not in params:
            return None;
        if 'operation' not in params:
            return None;
        account_value = params['value'];
        operation = params['operation'];
    
        try:
            value = float(str(account_value))
            current_value = float(str(DictUtils.pick(self.to_json(), "account_value", float, 0)))
            new_value = None;
            if str(operation).lower() == 'add':
                new_value = value + current_value;
            elif str(operation).lower() == 'remove':
                new_value = current_value - value;
            if new_value is None or new_value < 0:
                return None;
        
            data_update = {'account_value': new_value, 'last_value': current_value}
            print('new', data_update)
            self.document_reference(self.id).set(data_update, merge=True)
            return DictUtils.dict_from_keys(self.getAccount(), ['account_value']);
        except Exception as e:
            print('exception', e)
            return None;

    def remove(self, only_mark_as_removed=True):
        try:
            if self.id is None:
                return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Cannot identify Account with id {self.id}","INVALID_REQUEST", 1));
            if only_mark_as_removed:
                self.document_reference().set({"is_removed": True})
            else:
                self.document_reference().delete();
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, {"message": f"Account {self.id} deleted"}, None);
        except:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"An error occurated while removing authorization code with id {self.id}","INVALID_REQUEST", 1));


@dataclass(init=False)
class UserRole(BaseClass):
    admin: bool
    readOnly: bool
    def __init__(self, role=None, **kwargs):
        (cls_object, keys, data_args) = init_class_kwargs(self, role, ['admin', "readOnly"], None, None, [], **kwargs)
        for key in keys:
            setattr(self, key, cls_object[key]) 
    def to_dict(self, field=None):
        return {
            "admin": self.admin,
            "readOnly": self.readOnly
        }
    @staticmethod
    def from_dict(obj: Any) -> 'UserRole':
        cls_object, keys = get_object_model_class(obj, UserRole, None);
        return UserRole(cls_object)
@dataclass(init=False)
class LinkedAccount(BaseClass):
    account: Account
    role: UserRole
    def __init__(self, account_linked=None, **kwargs):
        
        (cls_object, keys, data_args) = init_class_kwargs(self, account_linked, ["account", "role"], None, None, [], **kwargs)
        for key in keys:
            setattr(self, key, cls_object[key])
            if key == 'account':
                # print('cls_object[key]', Account.from_dict(cls_object[key]))
                setattr(self, key, Account.from_dict(cls_object[key]))
            else:
                setattr(self, key, UserRole.from_dict(cls_object[key]))
    def to_dict(self):
        return {
            "account": self.account.to_json(["id"]),
            "role": self.role.to_json()
        }

    @staticmethod
    def from_dict(obj: Any) -> 'LinkedAccount':
        cls_object, keys = get_object_model_class(obj, LinkedAccount, None);
        _account = DictUtils.pick(obj, "account", bool)
        _role = DictUtils.pick(obj, "role", bool)
        return LinkedAccount(cls_object)



@dataclass(init=False)
class AccountLink(FirebaseCollectionBase):
    id: str
    linkDate: int
    linkDateString: str
    owner: str
    owner_email: str
    target: str
    target_email: str
    status: str
    linked_account: LinkedAccount

    def __init__(self, account_link=None, **kwargs):
        (cls_object, keys, data_args) = init_class_kwargs(self, account_link, LINK_STANDARD_FIELDS, AccountLinkFieldProps, ACCOUNT_LINK_COLLECTION, ['id'], **kwargs)
        super().__init__(**data_args);
        for key in keys:
            # print('key', key)
            if key=='linked_account':
                _linked =  DictUtils.pick(cls_object, "linked_account", dict)
                setattr(self, key, LinkedAccount.from_dict(_linked))
            else:
                setattr(self, key, cls_object[key])

    def to_dict(self):
        return self.to_json(['id', "linked_account"])


    @staticmethod
    def generate_model(_key_="default_value"):
        link = {};
        props = AccountLinkFieldProps
        for k in DictUtils.get_keys(props):
            link[k] = props[k][_key_];
        return link;

    @staticmethod
    def from_dict(account_link: Any, db=None, collection_name=None) -> 'AccountLink':
        cls_object, keys = get_object_model_class(account_link, AccountLink, AccountLinkFieldProps);
        _account = AccountLink(cls_object, db=db, collection_name=collection_name)
        return _account
    
    
    def get(self):
        id = self.id;
        if bool(id) is None:
            return None;
    
        doc = self.document_reference().get();
        if doc.exists is False:
            return None;
        data = {"id": doc.id, **doc.to_dict()()}
        return AccountLink.from_dict(data, db=self.db, collection_name=self.collection_name);

    # def query(self, query_params: list, first=False, limit=None):
    #     result = [];
    #     query_result = self.custom_query(query_params, first=first, limit=limit)
    #     if bool(query_result):
    #         if first:
    #             return AccountLink.from_dict(account=query_result, db=self.db, collection_name=self.collection_name)
    #         else:
    #             for doc in query_result:
    #                 result.append(AccountLink.from_dict(account=doc, db=self.db, collection_name=self.collection_name))
    #             return result
    #     if first:
    #             return None
    #     return [];

    def getAccount(self):
            account = self.get(self.id);
            if account is None:
                return None;
            return account.to_json();

    def update(self, data):
        
        try:
            last_value = self.to_json();
            filtered_value = pydash.pick(data, AccountFields.filtered_keys('editable', True));
            new_value = DictUtils.merge_dict(filtered_value, self.to_json());
            changed_fields = DictUtils.get_changed_field(last_value, new_value);
            data_update = DictUtils.dict_from_keys(filtered_value, changed_fields);
            if bool(data_update) is False:
                return None;
            self.document_reference().set(data_update, merge=True)
            return DictUtils.dict_from_keys(self.get().to_json(), changed_fields);
        except Exception as e:
            print(e)
            return None;

    def remove(self, only_mark_as_removed=True):
        try:
            if self.id is None:
                return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"Cannot identify Account with id {self.id}","INVALID_REQUEST", 1));
            if only_mark_as_removed:
                self.document_reference().set({"is_removed": True})
            else:
                self.document_reference().delete();
            return ApiResponse(ResponseStatus.OK, StatusCode.status_200, {"message": f"Account {self.id} deleted"}, None);
        except:
            return ApiResponse(ResponseStatus.ERROR, StatusCode.status_400, None, Error(f"An error occurated while removing authorization code with id {self.id}","INVALID_REQUEST", 1));