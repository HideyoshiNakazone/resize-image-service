from storage_service.config.config_virus_checker import (
    get_virus_checker_api_key,
)
from storage_service.service.virus_checker.virus_checker_service import (
    VirusCheckerService,
)
from storage_service.service.virus_checker.virus_total_service import (
    VirusTotalService,
)
from storage_service.utils.enums.virus_checker_type import VirusCheckerType

from dotenv import load_dotenv

import os
from functools import cache


@cache
def dependency_virus_checker_service() -> VirusCheckerService:
    load_dotenv()

    virus_checker_config = get_virus_checker_api_key()

    if not virus_checker_config["api_key"]:
        raise RuntimeError("Virus Checker API Key not found")

    virus_checker_type_var = os.environ.get("VIRUS_CHECKER_TYPE")
    if VirusCheckerType(virus_checker_type_var) == VirusCheckerType.TOTAL_VIRUS:
        return VirusTotalService(**get_virus_checker_api_key())

    raise RuntimeError("Invalid Virus Checker Type")
