from abc import ABC, abstractmethod
from io import BytesIO


class VirusCheckerService(ABC):
    @abstractmethod
    def check_virus(self, file_data: BytesIO) -> bool:
        pass
