# Untappd MCP Server (untappd-mcp)

Untappd MCP Server is a Python MCP server for Untappd connectivity. It is not affiliated in any way with Untappd.

## Usage

To use the Untappd MCP Server, you must have an API Client ID and Client Secret. Consult https://untappd.com/api/ for information on how to onboard to the Untappd API. Note that currently (as of August 2026), Untappd is not onboarding non-commercial APIs.

Add your Client ID and Client Secret and Redirect URL (needed for Authentication, see below) to `.env` as:

```
CLIENT_ID=CLIENT_ID_HERE
CLIENT_SECRET=CLIENT_SECRET_HERE
REDIRECT_URL=REDIRECT_URL_HERE
```

### Authentication

Some of the tools this server supports require authentication with the Untappd API. This is also recommended if you want to run this MCP to support multiple users and avoid frequent usage threshold constraints (the default API usage is 100 calls per hour OR per authenticated user per hour).

To support authentication, it's best to ask users to authenticate following the instructions below, using the callback URL you've created when obtaining your API key. A simple example token capture HTML page is included in `examples/token.html`. Note that Access Tokens never expire. To support authentication, the simplest procedure is as follows:

- Visit `https://untappd.com/oauth/authenticate/?client_id={YOUR_CLIENT_ID}&response_type=token&redirect_url={YOUR_REDIRECT_URL}` (Note that your CLIENT_SECRET should NEVER be exposed - ID and REDIRECT are fine to expose though)
- When running locally (stdio mode), you can use an environment variable for this. Simply add to your mcp.json or similar config, something like:
  `"env": { "ACCESS_TOKEN": "ACCESS_TOKEN_HERE" }`
- When running remotely (streamable_http mode), the client should provide the token via the Authorization Bearer token.

## Running the Server

`uv run mcp dev src/untappd_mcp/server.py`

Note that when testing locally using the Inspector via this command, any tool that requires Authentication will fail. Tools where Authentication is optional will fall back on your client_id/client_secret.

You can solve this by putting `ACCESS_TOKEN=YOUR_ACCESS_TOKEN` into .env **_but be extremely careful not to deploy with this change or you risk every user using your access token rather than their own_**.

### Integration

This is built on the MCP Python SDK and it is recommended you follow the instructions at [Connect To A Real Host](https://py.sdk.modelcontextprotocol.io/get-started/real-host/) to integrate with Claude, Cursor, VS Code, etc.

## Tools

Currently the Untappd MCP supports the following tools:

- Beer Search (beer_search) - searches for beers with the requested `name` parameter. Optionally you can provide an `offset` (for "search more" functionality).
- Brewery Search (brewery_search) - searches for breweries with the requested `name` parameter. Optionally you can provide an `offset` (for "search more" functionality).

## Affiliation

untappd-mcp is not affiliated in any way with Untappd and is an independent hobby project.

## Contributions

PRs are always welcome. Please first raise an issue before raising a PR to implement the solution.

## License

[MIT](https://choosealicense.com/licenses/mit/)
