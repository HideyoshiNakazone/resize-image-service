from storage_service.service.virus_checker.virus_checker_service import (
    VirusCheckerService,
)

from virustotal_python import Virustotal

from io import BytesIO


class VirusTotalService(VirusCheckerService):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def check_virus(self, file_data: BytesIO) -> bool:
        files = {"file": ("image_file", file_data)}

        with Virustotal(self.api_key) as vtotal:
            resp = vtotal.request("files", files=files, method="POST")

            file_attributes = self._get_analysis(resp.json()["data"]["id"])

            return self._is_valid_file(file_attributes["data"]["attributes"]["stats"])

    def _get_analysis(self, file_id: str) -> dict:
        with Virustotal(self.api_key) as vtotal:
            resp = vtotal.request(f"analyses/{file_id}")

            return resp.json()

    @staticmethod
    def _is_valid_file(file_stats: dict) -> bool:
        if "malicious" in file_stats and file_stats["malicious"] > 0:
            return False

        if "suspicious" in file_stats and file_stats["suspicious"] > 0:
            return False

        return True
