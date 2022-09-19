"""REST client handling, including LichessStream base class."""

import json
from pathlib import Path
from typing import Optional

from memoization import cached

from singer_sdk.authenticators import BearerTokenAuthenticator

from tap_lichess.openapi import OpenApi3Stream

class LichessStream(OpenApi3Stream):
    """Lichess stream class."""

    content_type = "application/json"

    @property
    def api_schema(self) -> dict:
        with open(Path(__file__).parent / Path("openapi.json")) as f:
            return json.load(f)

    @property
    @cached
    def authenticator(self) -> Optional[BearerTokenAuthenticator]:
        """Return a new authenticator object."""
        if self.config['auth_token']:
            return BearerTokenAuthenticator(self, self.config['auth_token'])
        return None

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        return {
            "User-Agent": "https://github.com/rabidaudio/tap-lichess",
            "Accept": self.content_type,
        }

    # def get_next_page_token(
    #     self, response: requests.Response, previous_token: Optional[Any]
    # ) -> Optional[Any]:
    #     """Return a token for identifying next page or None if no more pages."""
    #     # TODO: If pagination is required, return a token which can be used to get the
    #     #       next page. If this is the final page, return "None" to end the
    #     #       pagination loop.
    #     if self.next_page_token_jsonpath:
    #         all_matches = extract_jsonpath(
    #             self.next_page_token_jsonpath, response.json()
    #         )
    #         first_match = next(iter(all_matches), None)
    #         next_page_token = first_match
    #     else:
    #         next_page_token = response.headers.get("X-Next-Page", None)

    #     return next_page_token

    # def get_url_params(
    #     self, context: Optional[dict], next_page_token: Optional[Any]
    # ) -> Dict[str, Any]:
    #     """Return a dictionary of values to be used in URL parameterization."""
    #     params: dict = {}
    #     if next_page_token:
    #         params["page"] = next_page_token
    #     if self.replication_key:
    #         params["sort"] = "asc"
    #         params["order_by"] = self.replication_key
    #     return params

    # def prepare_request_payload(
    #     self, context: Optional[dict], next_page_token: Optional[Any]
    # ) -> Optional[dict]:
    #     """Prepare the data payload for the REST API request.

    #     By default, no payload will be sent (return None).
    #     """
    #     # TODO: Delete this method if no payload is required. (Most REST APIs.)
    #     return None

    # def post_process(self, row: dict, context: Optional[dict]) -> dict:
    #     """As needed, append or transform raw data to match expected structure."""
    #     # datetimes from timestamps
    #     import pdb; pdb.set_trace()
    #     return row
