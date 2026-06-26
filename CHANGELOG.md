# Changelog

All notable changes to the ChatBotKit Python SDK are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
