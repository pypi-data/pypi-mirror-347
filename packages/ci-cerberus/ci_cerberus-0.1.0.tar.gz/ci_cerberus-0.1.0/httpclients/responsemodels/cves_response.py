import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List

from models.cve import Cve
from models.cvss import Cvss

logger = logging.getLogger(__name__)


@dataclass
class CvesResponse:
    """
    DTO for response from NVD CVEs endpoint.

    Contains a list of CVEs, number of results returned & time data was retrieved.
    """

    total_results: int
    timestamp: str
    cves: List[Cve] = field(default_factory=list)

    @staticmethod
    def parse_json(data: Dict[str, Any]) -> "CvesResponse":
        """Helper method to parse CVE from raw JSON into CvesResponse"""
        logger.debug("DEBUG: parsing CVE response")
        cves = []

        for item in data.get("vulnerabilities", []):
            cve_data = item.get("cve", {})
            cve_id = cve_data.get("id")

            descriptions = {}
            for description in cve_data.get("descriptions", []):
                descriptions[description.get("lang")] = description["value"]

            description_english = descriptions.get(
                "en", "Couldn't find an English description for this CVE"
            )

            cvss_scores = []
            for metric in cve_data.get("metrics", {}).get("cvssMetricV31", []):
                cvss_data = metric.get("cvssData", {})
                cvss = Cvss(
                    source=metric.get("source"),
                    type=metric.get("type"),
                    base_score=cvss_data.get("baseScore"),
                    severity=cvss_data.get("baseSeverity"),
                    vector=cvss_data.get("vectorString"),
                )
                cvss_scores.append(cvss)

            weaknesses = []
            for weakness in cve_data.get("weaknesses", []):
                for description in weakness.get("description", []):
                    if description.get("lang") == "en":
                        weaknesses.append(description["value"])

            cpes = []
            for config in cve_data.get("configurations", []):
                for node in config.get("nodes", []):
                    for match in node.get("cpeMatch", []):
                        if match.get("vulnerable"):
                            cpes.append(match.get("criteria"))

            references = []
            for reference in cve_data.get("references", []):
                reference_url = reference.get("url")
                references.append(reference_url)

            cves.append(
                Cve(
                    cve_id=cve_id,
                    description=description_english,
                    cvss_scores=cvss_scores,
                    weaknesses=weaknesses,
                    cpes=cpes,
                    references=references,
                )
            )

        return CvesResponse(
            total_results=data.get("totalResults"),
            timestamp=data.get("timestamp"),
            cves=cves,
        )
