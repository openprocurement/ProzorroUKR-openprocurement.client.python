# -*- coding: utf-8 -*-
from zope.deprecation import deprecation

from openprocurement_client.clients import APIResourceClient
from openprocurement_client.constants import (
    CHANGES,
    CONTRACTS,
    DOCUMENTS,
    MILESTONES,
)


class ContractingClient(APIResourceClient):
    """ Contracting client """
    resource = CONTRACTS

    def create_contract(self, contract):
        return self.create_resource_item(contract)

    def get_contract(self, contract_id):
        return self.get_resource_item(contract_id)

    def get_contracts(self, params=None, feed=CHANGES):
        return self.get_resource_items(params=params, feed=feed)

    def create_change(self, contract_id, access_token, change_data):
        return self.create_resource_item_subitem(contract_id, change_data, CHANGES, access_token=access_token)

    @deprecation.deprecate("use create_resource_item_subitem")
    def _create_contract_resource_item(self, contract_id, access_token, item_obj, items_name):
        return self.create_resource_item_subitem(contract_id, item_obj, items_name, access_token)

    def retrieve_contract_credentials(self, contract_id, access_token):
        # In order to get rights for future contract editing, tender token
        # is passed as access token here.
        # Response will contain the new access token for further
        # contract modification.
        return self.patch_credentials(contract_id, access_token)

    def patch_contract(self, contract_id, access_token, data):
        return self.patch_resource_item(contract_id, data, access_token)

    def patch_change(self, contract_id, change_id, access_token, data):
        return self.patch_resource_item_subitem(contract_id, data, CHANGES, change_id, access_token=access_token)

    def patch_milestone(self, contract_id, milestone_id, access_token, data):
        return self.patch_resource_item_subitem(
            contract_id, data, MILESTONES, milestone_id, access_token=access_token
        )

    def post_document(self, contract_id, access_token, data):
        return self.create_resource_item_subitem(
            contract_id, data, DOCUMENTS, access_token=access_token
        )
