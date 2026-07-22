# Changelog

All notable changes to the ChatBotKit Python SDK are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.5.0] - 2026-07-22

### Added

- Agent cancellation. `agent.execute(...)` and `agent.complete(...)` now accept
  an `abort_signal` (`asyncio.Event`); setting it stops the loop from the outside
  (timeout, shutdown, user stop) and exits with code `1` at the next event
  boundary. The built-in `abort` tool's `hard=True` option now cancels the
  in-flight iteration immediately instead of being a no-op, bringing the Python
  agent to parity with the Node and Go SDKs.

### Changed

- The agent system instruction now includes the "Be Responsive" guideline
  (prioritise new user input mid-run), matching the Node and Go SDKs.

## [0.4.0] - 2026-06-27

### Added

- Secret token minting and request proxying. `client.secret.mint(...)` /
  `client.contact.secret.mint(...)` mint a usable token from a secret
  (`oauth`/`jwt` secrets only; owner-only) and return `{ token, expiresAt }`.
  `client.secret.proxy(...)` / `client.contact.secret.proxy(...)` proxy a request
  through a secret — the credential is injected server-side (it never leaves the
  platform) and the upstream `httpx.Response` is returned as-is, success or error.
- `AuthorizationRequiredError` (exported from `chatbotkit`; a subclass of
  `APIError`) carrying the `url` the user must visit to authorize. It is raised
  when a secret or connection has not been authenticated yet
  (`409 authorization_required`) — by `mint`, by any normal route, and by `proxy`
  (which otherwise passes every genuine upstream response through untouched).
  `APIError` now also carries `status_code` and the parsed `data` body.

## [0.3.0] - 2026-06-26

### Added

- `state` lifecycle field on the skillset and ability resources, backed by the
  new `ResourceState` enum (`enabled` / `disabled`). A skillset or ability can
  now be toggled off without deleting it. Available on the create, update, fetch,
  and list types.

## [0.2.0] - 2026-06-22

### Added

- `skill_server` integration client (`client.integration.skill_server`) with
  `list`, `fetch`, `create`, `update`, and `delete`. The Skill Server
  integration exposes a skillset's abilities as a text-first HTTP API.
- `site` client under `space` (`client.space.site`) with `list`, `fetch`,
  `create`, `update`, and `delete`, keyed by the parent space ID. A space site
  binds a `<label>.chatbotkit.space` subdomain to static content served from a
  space's storage.

### Changed

- Re-generated types from the latest API spec, including the `alias` field now
  present across integration create/update requests.

## [0.1.0] - 2026-06-11

### Added

- Initial release of the async Python SDK for ChatBotKit.
