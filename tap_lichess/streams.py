"""Stream type classes for tap-lichess."""

import requests
from typing import Any, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from singer_sdk.pagination import BaseAPIPaginator, SinglePagePaginator

from tap_lichess.client import LichessStream

class ListPaginator(BaseAPIPaginator[List[Any]]):
    """Given a static list and a step size, generate pages from that list."""

    def __init__(self, items: List[Any], step: int = 1) -> None:
        super().__init__(start_value=items[0:step])
        self.items = items
        self.step = step
        self.index = 0 

    def get_next(self, response: requests.Response) -> List[Any] | None:
        self.index += self.step
        chunk = self.items[self.index : self.index + self.step]
        if len(chunk) == 0:
            return None
        return chunk

class UsersStream(LichessStream):
    """
    Read user profile info.
    
    This one is a little strange, you post up to 300 usernames
    in CSV form and get a JSON array back.
    """
    name = "users"
    path = "/api/users"
    primary_keys = ["id"]
    replication_key = None
    rest_method = "POST"
    step_size = 300

    def get_new_paginator(self) -> BaseAPIPaginator:
        return ListPaginator(self.config['usernames'], self.step_size)

    def prepare_request(
        self, context: dict | None, next_page_token: List[Any]
    ) -> requests.PreparedRequest:
        http_method = self.rest_method
        url: str = self.get_url(context)
        params: dict = self.get_url_params(context, next_page_token)
        headers = self.http_headers
        # if there isn't a next page, load the first page
        body: str = ",".join(next_page_token)

        return self.build_prepared_request(
            method=http_method,
            url=url,
            params=params,
            headers=headers,
            data=body,
        )

    @property
    def http_headers(self) -> dict:
        return {
            **super().http_headers,
            "Content-Type": "text/plain",
        }

class UserChildStream(LichessStream):
    """Base class for child streams by user."""

    parent_stream_type = UsersStream
    ignore_parent_replication_key = True
    state_partitioning_keys = ["username"]

    # def post_process(self, row: dict, context: Optional[dict] = None) -> Optional[dict]:
    #     """As needed, append or transform raw data to match expected structure."""
    #     # add the username from context as it isn't in the response body
    #     assert context is not None
    #     row["username"] = context["username"]
    #     return super().post_process(row, context)

class GameStream(LichessStream):
    """Stream of chess games."""
    name = "games"
    path = "/games/user/{username}"
    primary_keys = ["id"]
    # replication_key = 
    
    # "Accept": "application/nd-json",

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        import pdb; pdb.set_trace()