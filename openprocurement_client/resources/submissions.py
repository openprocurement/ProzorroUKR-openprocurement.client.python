import logging

from openprocurement_client.clients import APIResourceClient
from openprocurement_client.constants import (SUBMISSIONS, DOCUMENTS)

LOGGER = logging.getLogger(__name__)


class SubmissionsClient(APIResourceClient):
    """Client for submissions"""

    resource = SUBMISSIONS

    def get_submission(self, submission_id):
        return self.get_resource_item(submission_id)

    def create_submission(self, submission):
        return self.create_resource_item(submission)

    def patch_submission(self, submission_id, patch_data={}, access_token=None):
        return self.patch_resource_item(submission_id, patch_data, access_token=access_token)

    def upload_submission_document(self, file, submission_id, use_ds_client=True,
                              doc_registration=True, access_token=None):
        return self.upload_document(file, submission_id,
                                    use_ds_client=use_ds_client,
                                    doc_registration=doc_registration,
                                    access_token=access_token)

    def post_registered_submission_document(self, submission_id, document_data, access_token=None):
        return self.create_resource_item_subitem(
            submission_id, document_data, DOCUMENTS, access_token=access_token
        )

    def patch_submission_document(self, submission_id, document_data, document_id,
                       access_token=None, depth_path=None):
        return self.patch_resource_item_subitem(
            submission_id, document_data, DOCUMENTS, document_id,
            access_token, depth_path
        )

    def put_submission_document(self, submission_id, subitem_obj, document_id, access_token=None):
        headers = None
        if access_token:
            headers = {'X-Access-Token': access_token}
        if isinstance(submission_id, dict):
            headers = {'X-Access-Token': self._get_access_token(submission_id)}
            resource_item_id = submission_id['data']['id']
        url = '{}/{}/{}/{}'.format(self.prefix_path, submission_id,
                                       DOCUMENTS, document_id)
        return self._create_resource_item(url, subitem_obj, headers=headers, method='PUT')


    def get_submission_document(self, submission_id, document_id, access_token=None):
        return self.get_resource_item_subitem(
            submission_id, document_id, depth_path='{}'.format(DOCUMENTS), access_token=access_token)


