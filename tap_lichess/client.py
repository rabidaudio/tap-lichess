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
