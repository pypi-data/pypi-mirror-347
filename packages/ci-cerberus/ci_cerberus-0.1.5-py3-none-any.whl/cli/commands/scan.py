import logging

from githubparsers import workflowparser
from httpclients.nvd_httpclient import NvdHttpClient
from importlib.metadata import version
from typing import Tuple

from models.cve import Cve


def register_command(subparsers):
    parser = subparsers.add_parser(
        "scan", help="Scan workflow files for vulnerabilities"
    )
    parser.set_defaults(command=handle_scan)


def handle_scan(action_name: str):
    logger = logging.getLogger(__name__)

    logger.info(f"🐕 starting ci-cerberus! (v{version('ci-cerberus')})\n")
    logger.debug("(debug mode enabled)")

    parser = workflowparser.WorkflowParser()
    workflows = parser.get_workflows()
    steps_data = _get_steps(workflows)

    nvd_client = NvdHttpClient("https://services.nvd.nist.gov/")

    steps_with_cves: dict[(str, str), list[Cve]] = {}

    for step_obj, workflow_file_name in steps_data:
        cves_response = nvd_client.find_cves_by_keywords(step_obj.uses)
        if cves_response.cves:
            steps_with_cves[(step_obj.uses, workflow_file_name)] = cves_response.cves

    _log_cve_details(steps_with_cves, logger)


def _log_cve_details(
    steps_with_cves: dict[(str, str), list[Cve]], logger: logging.Logger
):
    logger.info(f"🔍 found {len(steps_with_cves)} steps with potential CVEs")
    for (step, workflow_file_name), cves in steps_with_cves.items():
        logger.info(f"  ⛓️‍💥 {step} (`{workflow_file_name}`)")
        for cve in cves:
            logger.info(
                f"      CVE: {cve.cve_id} (https://nvd.nist.gov/vuln/detail/{cve.cve_id})"
            )
            logger.info(f"      CVSSs: ")
            for cvss in cve.cvss_scores:
                logger.info(f"        - Source:{cvss.source}")
                logger.info(f"          - Base Score:{cvss.base_score}")
                logger.info(f"          - Version:{cvss.type}")
                logger.info(f"          - Severity:{cvss.severity}")
            logger.info(f"      CWEs: ")
            for weakness in cve.weaknesses:
                logger.info(
                    f"              - https://cwe.mitre.org/data/definitions/{weakness.split('CWE-')[1]}.html"
                )
            logger.info(
                f"      Description: {cve.description} (https://nvd.nist.gov/vuln/detail/{cve.cve_id})"
            )
            logger.info("\n")


def _get_steps(
    workflows: list[workflowparser.Workflow],
) -> list[Tuple[workflowparser.Step, str]]:
    steps_data = []
    for workflow in workflows:
        for job in workflow.jobs:
            for step in job.steps:
                steps_data.append((step, workflow.file_name))
    return steps_data
