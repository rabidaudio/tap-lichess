"""Stream type classes for tap-lichess."""

import requests
import json
from typing import Any, List, Iterable, Optional

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

    def get_child_context(self, record: dict, context: Optional[dict]) -> dict:
        return { "username": record["id"] }


class UserChildStream(LichessStream):
    """Base class for child streams by user."""

    parent_stream_type = UsersStream
    ignore_parent_replication_key = True
    state_partitioning_keys = ["username"]


class GamesStream(UserChildStream):
    """
    Stream of chess games.
    
    This one is also a bit weird, it returns games in nd-json (jsonl)
    format. It's unpaged, instead streaming all games in one request.
    """
    name = "games"
    path = "/api/games/user/{username}"
    primary_keys = ["id"]
    replication_key = "createdAt"
    content_type = "application/x-ndjson"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # override the request session to enable stream mode
        self.requests_session.stream = True

    def get_new_paginator(self) -> BaseAPIPaginator:
        return SinglePagePaginator()

    def get_url_params(self, context: dict | None, next_page_token: None) -> dict[str, Any]:
        params = {
            "sort": "dateAsc",
            "pgnInJson": "true",
            "clocks": "true",
            "evals": "true",
            "opening": "true",
            "literate": "true",
        }
        start_at = self.get_starting_timestamp(context)
        if start_at:
            params["since"] = int(start_at.timestamp())
        return params

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        for line in response.iter_lines():
            yield json.loads(line)
