import json
from importlib import resources

import httpx
from fastmcp import FastMCP
from fastmcp.server.openapi import RouteMap, RouteType

from dotenv import load_dotenv
import os

# by default looks for a .env in the cwd or the same folder as this script
load_dotenv()


def truncate_after_special_char(s: str) -> str:
    for i, ch in enumerate(s):
        if not ch.isalnum():
            return s[:i]
    return s  # if no non-alnum found


# Create a client for your API
api_client = httpx.AsyncClient(base_url=os.getenv("CLOSELINK_API_BASE_URL"),
                               headers={"apiKey": os.getenv("CLOSELINK_API_KEY")})

# Load your OpenAPI spec as object
with resources.open_text("src", "cl-openapi.json", encoding="utf-8") as f:
    spec = json.load(f)

# Replace all operationIds with the summary in camel case
for path, path_item in spec["paths"].items():
    for method, operation in path_item.items():
        summary_in_title_case = ''.join(x for x in operation["summary"].title() if not x.isspace())
        sanitized = truncate_after_special_char(summary_in_title_case)
        operation["operationId"] = sanitized

# Custom mapping rules
custom_maps = [
    # Force all endpoints to be Tools (for now)
    RouteMap(methods=["GET"],
             pattern=r".*",
             route_type=RouteType.TOOL)
]

# Create an MCP server from your OpenAPI spec
mcp = FastMCP.from_openapi(openapi_spec=spec, client=api_client, name="Closelink", route_maps=custom_maps)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
