# -*- coding: utf-8 -*-
from zope.deprecation import deprecation
from simplejson import loads

from openprocurement_client.compatibility_utils import munchify_factory
from openprocurement_client.exceptions import InvalidResponse
from openprocurement_client.clients import APIResourceClient
from openprocurement_client.constants import (
   AGREEMENTS,
   CHANGES,
   DOCUMENTS,
   CONTRACTS,
   MILESTONES
)

munchify = munchify_factory()


class AgreementClient(APIResourceClient):
    """ Client for agreements """
    resource = AGREEMENTS

    def get_agreement(self, agreement_id):
        return self.get_resource_item(agreement_id)

    def get_agreements(self, params=None, feed=CHANGES):
        return self.get_resource_items(params=params, feed=feed)

    def create_change(self, agreement_id, change_data, access_token=None):
        return self.create_resource_item_subitem(
            agreement_id, change_data, CHANGES, access_token=access_token)

    def patch_agreement(self, agreement_id, data, access_token=None):
        return self.patch_resource_item(agreement_id, data, access_token=access_token)

    def patch_change(self, agreement_id, data, change_id, access_token=None):
        return self.patch_resource_item_subitem(
            agreement_id, data, CHANGES, change_id, access_token=access_token)

    def patch_document(self, agreement_id, data, document_id, access_token=None):
        return self.patch_resource_item_subitem(
            agreement_id, data, DOCUMENTS, document_id, access_token=access_token)

    def find_agreements_by_classification_id(self, classification_id, additional_classifications=()):
        url = "{}_by_classification/{}".format(self.prefix_path, classification_id)
        params = {}
        if additional_classifications:
            params["additional_classifications"] = ",".join(additional_classifications)
        response = self.request('GET', url, params_dict=params)
        if response.status_code == 200:
            resource_items_list = munchify(loads(response.text))
            return resource_items_list.data

        raise InvalidResponse(response)

    def find_recursive_agreements_by_classification_id(self, classification_id, additional_classifications=()):
        if "-" in classification_id:
            classification_id = classification_id[:classification_id.find("-")]
        needed_level = 2
        while classification_id[needed_level] != '0':
            agreements = self.find_agreements_by_classification_id(classification_id, additional_classifications)
            if agreements:
                return agreements

            pos = classification_id[1:].find('0')
            classification_id = classification_id[:pos] + '0' + classification_id[pos+1:]


    def upload_document_in_milestone(self, file, agreement_id, contract_id, milestone_id, use_ds_client=True,
                                     doc_registration=True, access_token=None):
        depth_path = '{}/{}/{}/{}'.format(CONTRACTS, contract_id, MILESTONES, milestone_id)
        self.upload_document
        return self.upload_document(file, agreement_id,
                                    use_ds_client=use_ds_client,
                                    doc_registration=doc_registration,
                                    depth_path=depth_path,
                                    access_token=access_token)

    def ban_contract(self, agreement_id, contract_id, data, access_token=None):
        depth_path = '{}/{}'.format(CONTRACTS, contract_id)
        return self.create_resource_item_subitem(
            agreement_id, data, MILESTONES,
            depth_path=depth_path, access_token=access_token)


    def disqualify_contract(self, agreement_id, contract_id, milestone_id, data, access_token=None):
        depth_path = '{}/{}'.format(CONTRACTS, contract_id)
        return self.patch_resource_item_subitem(
            agreement_id, data, MILESTONES, milestone_id,
            depth_path=depth_path,
            access_token=access_token)



