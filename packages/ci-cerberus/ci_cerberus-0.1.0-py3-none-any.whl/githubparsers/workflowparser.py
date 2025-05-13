import logging
import os.path
from typing import Iterator, List, Optional

import yaml

from githubparsers.models.job import Job
from githubparsers.models.step import Step
from githubparsers.models.workflow import Workflow

logger = logging.getLogger(__name__)


class WorkflowParser:
    def __init__(self, github_directory: str = ".github/workflows"):
        self.github_directory = os.path.normpath(github_directory)

    def get_workflows(self) -> Optional[List[Workflow]]:
        files = self._find_workflow_files()
        if not files:
            return None

        workflows = []
        for file in files:
            workflow = self._parse_yaml(file)
            if not workflow:
                logger.error(f"unable to parse workflow from {file}")
            workflows.append(workflow)

        return workflows

    def _find_workflow_files(self) -> List[str] | None:
        absolute_path = os.path.abspath(self.github_directory)
        logger.debug(f"looking for workflow files in {absolute_path}")

        try:
            file_names = os.listdir(self.github_directory)
            if not file_names:
                logger.warning(f"couldn't find any files in {absolute_path}")
                return None

            logger.debug(f"found {len(file_names)} workflows in {absolute_path}")

            files = []
            for file in file_names:
                logger.info(f"    {file}")
                files.append(os.path.join(self.github_directory, file))

            return files
        except FileNotFoundError:
            logger.error(f"No directory found at {absolute_path}")
            return None

    def _parse_yaml(self, file_path: str) -> Workflow:
        with open(file_path, "r") as file:
            logger.info(f"parsing workflow file {file.name}")
            workflow_yaml = yaml.load(file.read(), Loader=yaml.SafeLoader)
            return self._parse_workflow(workflow_yaml)

    def _parse_workflow(self, workflow_yaml) -> Optional[Workflow]:
        jobs = list(self._parse_jobs(workflow_yaml.get("jobs")))
        if not jobs:
            logger.debug(f"couldn't find any jobs in {workflow_yaml}")

        return Workflow(
            id=workflow_yaml.get("id"),
            name=workflow_yaml.get("name"),
            jobs=jobs,
        )

    def _parse_jobs(self, jobs_yaml) -> Iterator[Job]:
        for key, job in jobs_yaml.items():
            steps = list(self._parse_steps(job.get("steps")))

            if not steps:
                logger.debug("couldn't find any steps in job - skipping")

            yield Job(
                key=key,
                name=job.get("name"),
                runs_on=job.get("runs-on"),
                steps=steps,
            )

    @staticmethod
    def _parse_steps(steps_yaml) -> Iterator[Step]:
        logger.info(yaml.dump(steps_yaml))
        for step in steps_yaml:
            uses = step.get("uses")

            yield Step(
                id=step.get("id"),
                name=step.get("name"),
                uses=uses,
                with_arguments=step.get("with"),
            )
