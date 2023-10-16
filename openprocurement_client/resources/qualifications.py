import logging

from openprocurement_client.clients import APIResourceClient
from openprocurement_client.constants import (QUALIFICATIONS, DOCUMENTS)

LOGGER = logging.getLogger(__name__)


class QualificationClient(APIResourceClient):
    """Client for qualification"""

    resource = QUALIFICATIONS

    def get_qualification(self, qualification_id):
        return self.get_resource_item(qualification_id)

    def patch_qualification(self, qualification_id, patch_data={}, access_token=None):
        return self.patch_resource_item(qualification_id, patch_data, access_token=access_token)

    def upload_qualification_document(self, file, qualification_id, use_ds_client=True,
                              doc_registration=True, access_token=None):
        return self.upload_document(file, qualification_id,
                                    use_ds_client=use_ds_client,
                                    doc_registration=doc_registration,
                                    access_token=access_token)

    def post_qualification_document(self, qualification_id, document_data, access_token=None):
        return self.create_resource_item_subitem(
            qualification_id, document_data, DOCUMENTS, access_token=access_token
        )

    def patch_qualification_document(self, qualification_id, document_data, document_id,
                       access_token=None, depth_path=None):
        return self.patch_resource_item_subitem(
            qualification_id, document_data, DOCUMENTS, document_id,
            access_token, depth_path
        )

    def put_qualification_document(self, qualification_id, subitem_obj, document_id, access_token=None):
        headers = None
        if access_token:
            headers = {'X-Access-Token': access_token}
        if isinstance(qualification_id, dict):
            headers = {'X-Access-Token': self._get_access_token(qualification_id)}
            resource_item_id = qualification_id['data']['id']
        url = '{}/{}/{}/{}'.format(self.prefix_path, qualification_id,
                                       DOCUMENTS, document_id)
        return self._create_resource_item(url, subitem_obj, headers=headers, method='PUT')