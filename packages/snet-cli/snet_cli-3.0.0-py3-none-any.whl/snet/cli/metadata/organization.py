import base64
from enum import Enum
from json import JSONEncoder
import json

from snet.cli.utils.utils import is_valid_url


class DefaultEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class AssetType(Enum):
    HERO_IMAGE = "hero_image"


class PaymentStorageClient(object):

    def __init__(self, connection_timeout=None, request_timeout="", endpoints=None):
        if endpoints is None:
            endpoints = []
        self.connection_timeout = connection_timeout
        self.request_timeout = request_timeout
        self.endpoints = endpoints

    def add_payment_storage_client_details(self, connection_time_out, request_timeout, endpoints):
        self.connection_timeout = connection_time_out
        self.request_timeout = request_timeout
        self.endpoints = endpoints

    @classmethod
    def from_json(cls, json_data: dict, check_url=True):
        if check_url:
            endpoints = json_data["endpoints"]
            if endpoints:
                for endpoint in endpoints:
                    if not is_valid_url(endpoint):
                        raise Exception("Invalid endpoint passed in json file")
        return cls(**json_data)

class Payment(object):

    def __init__(self, payment_address="", payment_expiration_threshold="", payment_channel_storage_type="",
                 payment_channel_storage_client=PaymentStorageClient()):
        self.payment_address = payment_address
        self.payment_expiration_threshold = payment_expiration_threshold
        self.payment_channel_storage_type = payment_channel_storage_type
        self.payment_channel_storage_client = payment_channel_storage_client

    @classmethod
    def from_json(cls, json_data: dict, check_url=True):
        payment_channel_storage_client = PaymentStorageClient.from_json(
            json_data['payment_channel_storage_client'], check_url)
        return cls(json_data['payment_address'], json_data['payment_expiration_threshold'],
                   json_data['payment_channel_storage_type'], payment_channel_storage_client)

    def update_connection_timeout(self, connection_timeout):
        self.payment_channel_storage_client.connection_timeout = connection_timeout

    def update_request_timeout(self, request_timeout):
        self.payment_channel_storage_client.request_timeout = request_timeout

    def update_endpoints(self, endpoints):
        self.payment_channel_storage_client.endpoints = endpoints


class Group(object):

    def __init__(self, group_name="", group_id="", payment=Payment()):
        self.group_name = group_name
        self.group_id = group_id
        self.payment = payment

    @classmethod
    def from_json(cls, json_data: dict, check_url=True):
        payment = Payment()
        if 'payment' in json_data:
            payment = Payment.from_json(json_data['payment'], check_url)
        return cls(json_data['group_name'], json_data['group_id'], payment)

    def add_group_details(self, group_name, group_id, payment):
        self.group_name = group_name
        self.group_id = group_id
        self.payment = payment

    def update_payment_expiration_threshold(self, payment_expiration_threshold):
        self.payment.payment_expiration_threshold = payment_expiration_threshold

    def update_payment_channel_storage_type(self, payment_channel_storage_type):
        self.update_payment_channel_storage_type = payment_channel_storage_type

    def update_payment_address(self, payment_address):
        self.payment.payment_address = payment_address

    def update_connection_timeout(self, connection_timeout):
        self.payment.update_connection_timeout(connection_timeout)

    def update_request_timeout(self, request_timeout):
        self.payment.update_request_timeout(request_timeout)

    def update_endpoints(self, endpoints):
        self.payment.update_endpoints(endpoints)

    def get_group_id(self, group_name=None):
        return base64.b64decode(self.get_group_id_base64(group_name))

    def get_payment_address(self):
        return self.payment.payment_address


class OrganizationMetadata(object):
    """
        {
            "org_name": "organization_name",
            "org_id": "org_id1",
            org_type: "organization"/"individual",
            "contacts": [
                {
                    "contact_type": "support",
                    "email_id":"abcd@abcdef.com",
                    "phone":"1234567890",
                },
                {
                    "contact_type": "dummy",
                    "email_id":"dummy@abcdef.com",
                    "phone":"1234567890",
                },
            ],
            "description": "We do this and that ... Describe your organization here ",
            "assets": {
                "hero_image": "QmNW2jjz11enwbRrF1mJ2LdaQPeZVEtmKU8Uq7kpEkmXCc/hero_gene-annotation.png"
            },
            "groups": [
                {
                    "group_name": "default_group2",
                    "group_id": "99ybRIg2wAx55mqVsA6sB4S7WxPQHNKqa4BPu/bhj+U=",
                    "payment": {
                        "payment_address": "0x671276c61943A35D5F230d076bDFd91B0c47bF09",
                        "payment_expiration_threshold": 40320,
                        "payment_channel_storage_type": "etcd",
                        "payment_channel_storage_client": {
                            "connection_timeout": "5s",
                            "request_timeout": "3s",
                            "endpoints": [
                                "http://127.0.0.1:2379"
                            ]
                        }
                    }
                },
                {
                    "group_name": "default_group2",
                    "group_id": "99ybRIg2wAx55mqVsA6sB4S7WxPQHNKqa4BPu/bhj+U=",
                    "payment": {
                        "payment_address": "0x671276c61943A35D5F230d076bDFd91B0c47bF09",
                        "payment_expiration_threshold": 40320,
                        "payment_channel_storage_type": "etcd",
                        "payment_channel_storage_client": {
                            "connection_timeout": "5s",
                            "request_timeout": "3s",
                            "endpoints": [
                                "http://127.0.0.1:2379"
                            ]
                        }
                    }
                }
            ]
        }
    """

    def __init__(self, org_name="", org_id="", org_type="",contacts=[], description={},
                 assets={}, groups=[]):
        self.org_name = org_name
        self.org_id = org_id
        self.org_type = org_type
        self.description = description
        self.assets = assets
        self.contacts = contacts
        self.groups = groups

    def add_group(self, group):
        self.groups.append(group)

    def get_json_pretty(self):
        return json.dumps(self, indent=4, cls=DefaultEncoder)

    def save_pretty(self, file_name):
        with open(file_name, 'w') as f:
            f.write(self.get_json_pretty())

    @classmethod
    def from_json(cls, json_data: dict, check_url=True):
        groups = []
        if 'groups' in json_data:
            groups = list(map(lambda j_d: Group.from_json(j_d, check_url), json_data["groups"]))
            if "contacts" not in json_data:
                json_data["contacts"] = []
            if "description" not in json_data:
                json_data["description"] = {}
            if "assets" not in json_data:
                json_data["assets"] = {}
            if "org_type" not in json_data:
                json_data["org_type"] = ""
        return cls(
            org_name=json_data['org_name'],
            org_id=json_data['org_id'],
            org_type=json_data['org_type'],
            contacts=json_data['contacts'],
            description=json_data['description'],
            groups=groups,
            assets=json_data['assets']
        )

    @classmethod
    def from_file(cls, filepath):
        try:
            with open(filepath, 'r') as f:
                return OrganizationMetadata.from_json(json.load(f))
        except Exception as e:
            print(
                "Organization metadata json file not found ,Please check --metadata-file path ")
            raise e

    def is_removing_existing_group_from_org(self, current_group_name, existing_registry_metadata_group_names):
        if len(existing_registry_metadata_group_names - current_group_name) == 0:
            pass
        else:
            removed_groups = existing_registry_metadata_group_names - current_group_name
            raise Exception("Cannot remove existing group from organization as it might be attached"
                            " to services, groups you are removing are  %s" % removed_groups)

    def check_remove_groups(self, existing_registry_metadata):
        unique_group_names = set([group.group_name for group in self.groups])
        existing_registry_metadata_group_names = set()

        if existing_registry_metadata:
            for group in existing_registry_metadata.groups:
                existing_registry_metadata_group_names.add(group.group_name)

        self.is_removing_existing_group_from_org(unique_group_names, existing_registry_metadata_group_names)

    def get_payment_address_for_group(self, group_name):
        for group in self.groups:
            if group.group_name == group_name:
                return group.get_payment_address()

    def get_group_id_by_group_name(self, group_name):
        for group in self.groups:
            if group.group_name == group_name:
                return group.group_id

    def get_group_by_group_id(self, group_id):
        for group in self.groups:
            if group.group_id == group_id:
                return group

    def add_asset(self, asset_ipfs_hash, asset_type):
        if asset_type == AssetType.HERO_IMAGE.value:
            self.assets[asset_type] = asset_ipfs_hash
        else:
            raise Exception("Invalid asset type %s" % asset_type)

    def remove_all_assets(self):
        self.assets = {}

    def remove_assets(self, asset_type):
        if asset_type == AssetType.HERO_IMAGE.value:
            self.assets[asset_type] = ""
        else:
            raise Exception("Invalid asset type %s" % asset_type)

    def add_description(self, description):
        self.description["description"] = description

    def add_short_description(self, short_description):
        self.description["short_description"] = short_description

    def add_url(self, url):
        self.description["url"] = url

    def remove_description(self):
        self.description = {}

    def add_contact(self, contact_type, phone, email):
        if phone is None:
            phone = ""
        if email is None:
            email = ""

        contact = {
            "contact_type": contact_type,
            "email_id": email,
            "phone": phone
        }
        self.contacts.append(contact)

    def remove_contact_by_type(self, contact_type):
        self.contacts = [contact for contact in self.contacts if contact["contact_type"] != contact_type]

    def remove_all_contacts(self):
        self.contacts = []
