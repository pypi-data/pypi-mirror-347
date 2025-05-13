from dataclasses import dataclass
from typing import List

from .cvss import Cvss


@dataclass
class Cve:
    cve_id: str
    description: str
    cvss_scores: List[Cvss]
    weaknesses: List[str]
    cpes: List[str]
    references: List[str]
