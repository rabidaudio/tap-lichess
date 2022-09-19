"""A base stream class for OpenApi-defined APIs."""

from typing import Any, Dict, Optional, Union

from memoization import cached
from openapi3 import OpenAPI
from openapi3.paths import Operation
from singer.schema import Schema
from singer_sdk.plugin_base import PluginBase as TapBaseClass
from singer_sdk.streams import RESTStream


class OpenApi3Stream(RESTStream):
    """A RESTStream that can be configured using an OpenApi 3 schema."""

    content_type = "application/json"

    def __init__(
        self,
        tap: TapBaseClass,
        name: Optional[str] = None,
        schema: Optional[Union[Dict[str, Any], Schema]] = None,
        api_schema: Dict[str, Any] = None,
    ) -> None:
        super().__init__(name=name, schema=schema, tap=tap)
        if api_schema:
            self.api_schema = api_schema

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
        raw_schema = (
            self.get_method_definition()
            .responses["200"]
            .content[self.content_type]
            .schema
        )
        # __get_state__ will resolve openapi references but include every
        # possible property.
        # Passing this through Schema.from_dict will sanitize that output.
        schema = Schema.from_dict(raw_schema.__getstate__()).to_dict()
        if "items" in schema:
            return schema["items"]
        return schema

    def get_method_definition(self) -> Operation:
        return self.api.paths[self.path].__getattribute__(self.rest_method.lower())
