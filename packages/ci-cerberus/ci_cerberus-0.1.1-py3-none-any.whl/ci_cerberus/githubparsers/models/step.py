from dataclasses import dataclass
from typing import Optional


@dataclass
class Step:
    id: str
    name: str
    uses: str
    with_arguments: Optional[dict] = None
