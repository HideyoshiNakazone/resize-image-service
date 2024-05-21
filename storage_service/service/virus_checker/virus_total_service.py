from storage_service.service.virus_checker.virus_checker_service import (
    VirusCheckerService,
)

from virustotal_python import Virustotal

from io import BytesIO


class VirusTotalService(VirusCheckerService):
    virus_checker: Virustotal

    def __init__(self, virus_checker: Virustotal):
        self.virus_checker = virus_checker

    def check_virus(self, file_data: BytesIO) -> bool:
        file_id = self._upload_file(file_data)
        file_attributes = self._get_analysis(file_id)

        return self._is_valid_file(file_attributes)

    def _upload_file(self, file_data: BytesIO) -> str:
        files = {"file": ("image_file", file_data)}

        resp = self.virus_checker.request("files", files=files, method="POST")

        return resp.data["id"]

    def _get_analysis(self, file_id: str) -> dict:
        resp = self.virus_checker.request(f"analyses/{file_id}")

        return resp.json()["data"]["attributes"]["stats"]

    @staticmethod
    def _is_valid_file(file_stats: dict) -> bool:
        match file_stats:
            case {"malicious": 0, "suspicious": 0, "harmless": 0}:
                return True
            case _:
                return False
