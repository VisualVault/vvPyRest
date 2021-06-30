import unittest
from .utilities import get_vault_object, generate_random_uuid, get_parameters_json
from vvrest.services.document_service import DocumentService


class DocumentServiceTest(unittest.TestCase):
    vault = None

    @classmethod
    def setUpClass(cls):
        if not cls.vault:
            cls.vault = get_vault_object()

        test_parameters = get_parameters_json()
        cls.folder_path = test_parameters['folder_path']
        cls.query_string = test_parameters['query_string']
        cls.document_id = test_parameters['document_id']
        cls.revision_id = test_parameters['document_revision_id']
        cls.index_field_id = test_parameters['index_field_id']
        cls.index_field_name = test_parameters['index_field_name']
        cls.folder_id = test_parameters['folder_id']

    def test_get_documents(self):
        """
        tests DocumentService.get_documents
        """
        document_service = DocumentService(self.vault)
        resp = document_service.get_documents(self.query_string)
        self.assertEqual(resp['meta']['status'], 200)
        documents = resp['data']
        self.assertGreater(len(documents), 0)
        for document in documents:
            self.assertEqual(document['folderPath'], self.folder_path)

    def test_get_document(self):
        """
        tests DocumentService.get_document
        """
        document_service = DocumentService(self.vault)
        resp = document_service.get_document(self.document_id)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['documentId'], self.document_id)

    def test_get_document_revisions(self):
        """
        tests DocumentService.get_document_revisions
        """
        document_service = DocumentService(self.vault)
        resp = document_service.get_document_revisions(self.document_id)
        self.assertEqual(resp['meta']['status'], 200)
        documents = resp['data']
        self.assertGreater(len(documents), 0)
        for document in documents:
            self.assertEqual(document['documentId'], self.document_id)

    def test_get_document_revision(self):
        """
        tests DocumentService.get_document_revision
        """
        document_service = DocumentService(self.vault)
        resp = document_service.get_document_revision(self.document_id, self.revision_id)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['id'], self.revision_id)
        self.assertEqual(resp['data']['documentId'], self.document_id)

    def test_get_document_index_fields(self):
        """
        tests DocumentService.get_document_index_fields
        """
        document_service = DocumentService(self.vault)
        resp = document_service.get_document_index_fields(self.document_id)
        self.assertEqual(resp['meta']['status'], 200)
        index_fields = resp['data']
        self.assertGreater(len(index_fields), 0)
        for index_field in index_fields:
            self.assertEqual(index_field['dataType'], 'DocumentIndexField')

    def test_get_document_index_field(self):
        """
        tests DocumentService.get_document_index_field
        """
        document_service = DocumentService(self.vault)
        resp = document_service.get_document_index_field(self.document_id, self.index_field_id)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['fieldId'], self.index_field_id)

    def test_get_document_revision_index_fields(self):
        """
        tests DocumentService.get_document_revision_index_fields
        """
        document_service = DocumentService(self.vault)
        resp = document_service.get_document_revision_index_fields(self.document_id, self.revision_id)
        self.assertEqual(resp['meta']['status'], 200)
        index_fields = resp['data']
        self.assertGreater(len(index_fields), 0)
        for index_field in index_fields:
            self.assertEqual(index_field['fieldId'], self.index_field_id)

    def test_get_document_revision_index_field(self):
        """
        tests DocumentService.get_document_revision_index_field
        """
        document_service = DocumentService(self.vault)
        resp = document_service.get_document_revision_index_field(self.document_id, self.revision_id, self.index_field_id)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['fieldId'], self.index_field_id)

    def test_update_document_index_fields(self):
        """
        tests DocumentService.update_document_index_fields
        """
        document_service = DocumentService(self.vault)
        expected_value = generate_random_uuid()
        fields_dict = str({self.index_field_name: expected_value})
        resp = document_service.update_document_index_fields(self.document_id, fields_dict)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(len(resp['data']), 1)
        self.assertEqual(resp['data'][0]['fieldId'], self.index_field_id)  # TODO: report issue with UUID label
        # self.assertEqual(resp['data'][0]['value'], expected_value)  # TODO: uncomment when API resolves bug
        new_value = document_service.get_document_index_field(self.document_id, self.index_field_id)['data']['value']
        self.assertEqual(new_value, expected_value)

    def test_update_document_index_field(self):
        """
        tests DocumentService.update_document_index_field
        """
        document_service = DocumentService(self.vault)
        expected_value = generate_random_uuid()
        resp = document_service.update_document_index_field(self.document_id, self.index_field_id, expected_value)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['fieldId'], self.index_field_id)
        self.assertEqual(resp['data']['value'], expected_value)
        new_value = document_service.get_document_index_field(self.document_id, self.index_field_id)['data']['value']
        self.assertEqual(new_value, expected_value)

    def test_new_document_and_delete_document(self):
        """
        tests DocumentService.new_document and DocumentService.delete_document
        """
        document_service = DocumentService(self.vault)

        # new document
        resp = document_service.new_document(self.folder_id, 1, '_test_doc', '_test_doc description', '0', '_test.txt')
        self.assertEqual(resp['meta']['status'], 200)
        document_id = resp['data']['documentId']
        revision_id = resp['data']['id']

        # validate document exists in VV
        resp = document_service.get_document(document_id)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['documentId'], document_id)
        self.assertEqual(resp['data']['archive'], 0)  # document not in recycle bin

        # delete document
        resp = document_service.delete_document(revision_id)
        self.assertEqual(resp['meta']['status'], 200)

        # validate document does not exist in VV
        resp = document_service.get_document(document_id)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['archive'], 2)  # document in recycle bin

    def test_update_document_check_in_status(self):
        """
        tests DocumentService.update_document_check_in_status
        """
        document_service = DocumentService(self.vault)

        # validate document checked in
        resp = document_service.get_document(self.document_id)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['documentId'], self.document_id)
        self.assertEqual(resp['data']['checkInStatus'], 0)

        # check out document in VV
        resp = document_service.update_document_check_in_status(self.document_id, 1)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['documentId'], self.document_id)
        self.assertEqual(resp['data']['checkInStatus'], 1)

        # check in document in VV
        resp = document_service.update_document_check_in_status(self.document_id, 0)
        self.assertEqual(resp['meta']['status'], 200)
        self.assertEqual(resp['data']['documentId'], self.document_id)
        self.assertEqual(resp['data']['checkInStatus'], 0)
