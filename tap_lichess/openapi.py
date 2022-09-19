"""A base stream class for OpenApi-defined APIs."""

from  openapi3 import OpenAPI
from openapi3.paths import Operation
from memoization import cached
from typing import Any

from singer_sdk.plugin_base import PluginBase as TapBaseClass
from singer_sdk.streams import RESTStream
from singer.schema import Schema

class OpenApi3Stream(RESTStream):
    """A RESTStream that can be configured using an OpenApi 3 schema."""

    def __init__(
        self,
        tap: TapBaseClass,
        name: str | None = None,
        schema: dict[str, Any] | Schema | None = None,
        api_schema: dict[str, Any] = None,
        content_type: str = "application/json",
    ) -> None:
        super().__init__(name=name, schema=schema, tap=tap)
        if api_schema:
          self.api_schema = api_schema
        self.content_type = content_type

    @property
    @cached
    def api(self) -> OpenAPI:
      return OpenAPI(self.api_schema, validate=True)

    @property
    @cached
    def url_base(self) -> str:
        return self.api.servers[0].url

    @property
    def schema(self) -> dict:
      raw_schema = self.get_method_definition().responses['200'].content[self.content_type].schema
      # __get_state__ will resolve openapi references but include every possible property.
      # Passing this through Schema.from_dict will sanitize that output
      return Schema.from_dict(raw_schema.__getstate__()).to_dict()['items']

    def get_method_definition(self) -> Operation:
      return self.api.paths[self.path].__getattribute__(self.rest_method.lower())
