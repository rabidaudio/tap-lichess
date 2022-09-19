"""Lichess tap class."""

from typing import List

from singer_sdk import Stream, Tap
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_lichess.streams import GamesStream, UsersStream

STREAM_TYPES = [
    UsersStream,
    GamesStream,
]


class TapLichess(Tap):
    """Lichess tap class."""

    name = "tap-lichess"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "auth_token",
            th.StringType,
            description="The token to authenticate against the API service. "
            "Not required.",
        ),
        th.Property(
            "usernames",
            th.ArrayType(th.StringType),
            required=True,
            description="Lichess account ids to fetch data for",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]


if __name__ == "__main__":
    TapLichess.cli()
