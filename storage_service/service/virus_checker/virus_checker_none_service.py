from storage_service.service.virus_checker.virus_checker_service import (
    VirusCheckerService,
)

from io import BytesIO


class VirusCheckerNoneService(VirusCheckerService):
    def check_virus(self, file_data: BytesIO) -> bool:
        # No virus checker is used, so we assume the file is safe
        return True
