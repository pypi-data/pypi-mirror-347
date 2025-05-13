from dataclasses import dataclass


@dataclass
class Cvss:
    source: str
    type: str
    base_score: float
    severity: str
    vector: str
