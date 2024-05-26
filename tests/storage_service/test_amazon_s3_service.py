from unittest import TestCase
from unittest.mock import Mock

from storage_service.service.storage import AmazonS3Service
from storage_service.utils.enums.file_type import FileType


class TestAmazonS3Service(TestCase):
    def setUp(self):
        self.s3_client_mock = Mock()
        self.virus_checker_service_mock = Mock()

    def test_get_temp_upload_link(self):
        self.s3_client_mock.generate_presigned_url.return_value = "https://test.com"

        storage_service = AmazonS3Service(
            s3_client=self.s3_client_mock,
            bucket_name="test_bucket",
            virus_checker_service=self.virus_checker_service_mock
        )

        response = storage_service.get_temp_upload_link("test_file", FileType.JPEG)

        self.assertEqual(response.signed_url, "https://test.com")
        self.assertEqual(response.expires_in, 3600)

        self.s3_client_mock.generate_presigned_url.assert_called_once_with(
            "put_object",
            Params={
                "Bucket": "test_bucket",
                "Key": "test_file",
                "ContentType": "image/jpeg",
            },
            ExpiresIn=3600,
        )

    def test_get_temp_read_link(self):
        self.s3_client_mock.generate_presigned_url.return_value = "https://test.com"
        self.s3_client_mock.list_objects.return_value = {
            "Contents": [
                {
                    "Key": "test_file"
                }
            ]
        }

        storage_service = AmazonS3Service(
            s3_client=self.s3_client_mock,
            bucket_name="test_bucket",
            virus_checker_service=self.virus_checker_service_mock
        )

        response = storage_service.get_temp_read_link("test_file")

        self.assertEqual(response.signed_url, "https://test.com")
        self.assertEqual(response.expires_in, 3600)

        self.s3_client_mock.generate_presigned_url.assert_called_once_with(
            "get_object",
            Params={
                "Bucket": "test_bucket",
                "Key": "test_file"
            },
            ExpiresIn=3600,
        )

    def test_delete_file(self):
        storage_service = AmazonS3Service(
            s3_client=self.s3_client_mock,
            bucket_name="test_bucket",
            virus_checker_service=self.virus_checker_service_mock
        )

        storage_service.delete_file("test_file")

        self.s3_client_mock.delete_object.assert_called_once_with(
            Bucket="test_bucket",
            Key="test_file"
        )

    def test_process_file_if_file_invalid(self):
        mock_body = Mock()
        mock_body.read.return_value = b"test_file"
        self.s3_client_mock.get_object.return_value = {
            "Body": mock_body
        }
        self.virus_checker_service_mock.check_virus.return_value = True

        storage_service = AmazonS3Service(
            s3_client=self.s3_client_mock,
            bucket_name="test_bucket",
            virus_checker_service=self.virus_checker_service_mock
        )

        with self.assertRaises(RuntimeError):
            storage_service.process_file("test_file", FileType.JPEG)

    def test_process_file_if_file_is_virus(self):
        mock_body = Mock()
        mock_body.read.return_value = b"test_file"
        self.s3_client_mock.get_object.return_value = {
            "Body": mock_body
        }

        mock_file_type = Mock()
        mock_file_type.get_validator.return_value = lambda x: x
        mock_file_type.get_content_type.return_value = "image/fake"

        self.virus_checker_service_mock.check_virus.return_value = False

        storage_service = AmazonS3Service(
            s3_client=self.s3_client_mock,
            bucket_name="test_bucket",
            virus_checker_service=self.virus_checker_service_mock
        )

        with self.assertRaises(ValueError):
            storage_service.process_file("test_file", mock_file_type)

    def test_process_file(self):
        mock_body = Mock()
        mock_body.read.return_value = b"test_file"
        self.s3_client_mock.get_object.return_value = {
            "Body": mock_body
        }
        self.virus_checker_service_mock.check_virus.return_value = True

        mock_file_type = Mock()
        mock_file_type.get_validator.return_value = lambda x: x
        mock_file_type.get_content_type.return_value = "image/fake"

        storage_service = AmazonS3Service(
            s3_client=self.s3_client_mock,
            bucket_name="test_bucket",
            virus_checker_service=self.virus_checker_service_mock
        )

        storage_service.process_file("test_file", mock_file_type)

        self.s3_client_mock.upload_fileobj.assert_called()
