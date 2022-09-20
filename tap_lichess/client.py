"""REST client handling, including LichessStream base class."""

import json
from pathlib import Path
from typing import Optional

from memoization import cached
from singer_sdk import RESTStream
from singer_sdk.authenticators import BearerTokenAuthenticator


class LichessStream(RESTStream):
    """Lichess stream class."""

    url_base = "https://lichess.org/api"
    content_type = "application/json"

    @property
    def api_schema(self) -> dict:
        with open(Path(__file__).parent / Path("openapi.json")) as f:
            return json.load(f)

    @property
    @cached
    def authenticator(self) -> Optional[BearerTokenAuthenticator]:
        """Return a new authenticator object."""
        if "auth_token" in self.config:
            return BearerTokenAuthenticator(self, self.config["auth_token"])
        return None

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed."""
        return {
            "User-Agent": "https://github.com/rabidaudio/tap-lichess",
            "Accept": self.content_type,
        }
