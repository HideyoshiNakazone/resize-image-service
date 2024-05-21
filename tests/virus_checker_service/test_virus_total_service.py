from io import BytesIO
from unittest import TestCase
from unittest.mock import Mock

from storage_service.service.virus_checker.virus_total_service import VirusTotalService


class TestVirusTotalService(TestCase):
    def test_check_virus_invalid(self):
        mock_virus_checker = Mock()
        mock_virus_checker.request.side_effect = [
            Mock(data={"id": "file_id"}),
            Mock(json=Mock(return_value={"data": {"attributes": {"stats": {"malicious": 1, "suspicious": 1, "harmless": 1}}}})),
        ]

        virus_total_service = VirusTotalService(mock_virus_checker)

        result = virus_total_service.check_virus(BytesIO(b"file_data"))

        self.assertFalse(result)

    def test_check_virus_valid(self):
        mock_virus_checker = Mock()
        mock_virus_checker.request.side_effect = [
            Mock(data={"id": "file_id"}),
            Mock(json=Mock(return_value={"data": {"attributes": {"stats": {"malicious": 0, "suspicious": 0, "harmless": 0}}}})),
        ]

        virus_total_service = VirusTotalService(mock_virus_checker)

        result = virus_total_service.check_virus(BytesIO(b"file_data"))

        self.assertTrue(result)
