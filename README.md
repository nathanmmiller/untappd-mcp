# Untappd MCP Server (untappd-mcp)

Untappd MCP Server is a Python MCP server for Untappd connectivity. It is not affiliated in any way with Untappd.

## Usage

To use the Untappd MCP Server, you must have an API Client ID and Client Secret. Consult https://untappd.com/api/ for information on how to onboard to the Untappd API. Note that currently (as of August 2026), Untappd is not onboarding non-commercial APIs.

Add your Client ID and Client Secret to `.env` as:

```
CLIENT_ID=CLIENT_ID_HERE
CLIENT_SECRET=CLIENT_SECRET_HERE
```

## Running the Server

`uv run mcp dev src/untappd_mcp/server.py`

### Integration

This is built on the MCP Python SDK and it is recommended you follow the instructions at [Connect To A Real Host](https://py.sdk.modelcontextprotocol.io/get-started/real-host/) to integrate with Claude, Cursor, VS Code, etc.

## Tools

Currently the Untappd MCP supports the following tools:

- Beer Search (search_for_beer) - searches for beers with the requested `name` parameter. Optionally you can provide a `limit` (default is 25), an `offset` (for "search more" functionality), and a `sort` ("name" - sorts by name instead of by checkin count).

## Affiliation

untappd-mcp is not affiliated in any way with Untappd and is an independent hobby project.

## Contributions

PRs are always welcome. Please first raise an issue before raising a PR to implement the solution.

## License

[MIT](https://choosealicense.com/licenses/mit/)
