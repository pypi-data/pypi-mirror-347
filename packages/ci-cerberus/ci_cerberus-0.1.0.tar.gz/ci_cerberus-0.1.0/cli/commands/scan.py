import logging

from githubparsers import workflowparser
from httpclients.nvd_httpclient import NvdHttpClient


def register_command(subparsers):
    parser = subparsers.add_parser(
        "scan", help="Scan workflow files for vulnerabilities"
    )
    parser.set_defaults(func=handle_scan)


def handle_scan(action_name: str):
    logger = logging.getLogger(__name__)

    nvd_client = NvdHttpClient("https://services.nvd.nist.gov/")
    cves = nvd_client.find_cves_by_keywords(action_name)

    logger.info(cves)
    parser = workflowparser.WorkflowParser()
    actions = parser.get_workflows()
    logger.info(actions)
