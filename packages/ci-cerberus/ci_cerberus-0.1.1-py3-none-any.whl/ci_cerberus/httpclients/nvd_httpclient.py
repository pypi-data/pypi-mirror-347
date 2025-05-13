import logging

from .base_httpclient import BaseHttpClient
from .responsemodels.cves_response import CvesResponse

logger = logging.getLogger(__name__)


class NvdHttpClient(BaseHttpClient):
    """Derived HttpClient to handle interacting with NIST NVD (National Vulnerability Database)"""

    def __init__(self, base_url: str):
        logger.debug("initialising NvdHttpClient")
        super().__init__(base_url)
        self.cves_url = "rest/json/cves/2.0"

    def find_cves_by_keywords(self, keywords: str) -> CvesResponse:
        logger.debug("called find_cves_by_keywords")
        keywords = keywords
        cves_response = self.get(self.cves_url, params={"keywordSearch": keywords})
        logger.debug(f"got response from NVD API\n{cves_response}")
        return CvesResponse.parse_json(cves_response)
