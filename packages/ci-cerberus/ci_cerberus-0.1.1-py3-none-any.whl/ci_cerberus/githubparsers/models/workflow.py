from dataclasses import dataclass

from .job import Job


@dataclass
class Workflow:
    id: str
    name: str
    jobs: list[Job]
