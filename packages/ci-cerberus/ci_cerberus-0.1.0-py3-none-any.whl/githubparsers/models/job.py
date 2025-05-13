from dataclasses import dataclass

from githubparsers.models.step import Step


@dataclass
class Job:
    key: str
    name: str
    runs_on: str
    steps: list[Step]
