# BASELINE-001 ADR: Keep plugin setup user-scoped and pin the marketplace ref

- **Status:** Accepted
- **Decision:** Do not add `requirements.toml`. Install the companion
  marketplace with `codex plugin marketplace add ... --ref v0.1.0`, install
  `governed-sdlc` from that marketplace, and verify that its manifest reports
  version `0.1.0`.
- **Context:** Codex CLI 0.144.4 supports native marketplace and plugin
  installation, but does not expose a project dependency manifest that
  installs or pins plugins. `requirements.toml` is a managed-policy surface and
  its plugin schema does not declare a plugin version.
- **Consequences:** Setup is explicit and honest, but each user or workspace
  must install the plugin. The companion repository must publish both plugin
  version `0.1.0` and Git tag `v0.1.0` before bootstrap succeeds.
