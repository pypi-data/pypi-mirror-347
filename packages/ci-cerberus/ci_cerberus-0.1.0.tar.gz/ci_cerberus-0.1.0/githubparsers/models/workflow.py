from dataclasses import dataclass

from githubparsers.models.job import Job


@dataclass
class Workflow:
    id: str
    name: str
    jobs: list[Job]
