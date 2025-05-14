import logging

from httpclients.base_httpclient import BaseHttpClient
from httpclients.responsemodels.cves_response import CvesResponse

logger = logging.getLogger(__name__)


class NvdHttpClient(BaseHttpClient):
    """Derived HttpClient to handle interacting with NIST NVD (National Vulnerability Database)"""

    def __init__(self, base_url: str):
        logger.debug("initialising NvdHttpClient")
        super().__init__(base_url)
        self.cves_url = "rest/json/cves/2.0"
        self._cves_cache = {}

    def find_cves_by_keywords(self, keywords: str) -> CvesResponse:
        logger.debug("called find_cves_by_keywords")
        if keywords in self._cves_cache:
            logger.debug(f"returning cached response for keywords: {keywords}")
            return self._cves_cache[keywords]

        keywords = keywords
        logger.debug(f"calling NVD API with {keywords}")
        cves_response_json = self.get(self.cves_url, params={"keywordSearch": keywords})
        logger.debug(f"got response from NVD API\n{cves_response_json}")
        cves_response = CvesResponse.parse_json(cves_response_json)
        self._cves_cache[keywords] = cves_response
        return cves_response
