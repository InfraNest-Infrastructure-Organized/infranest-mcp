<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/InfraNest-Infrastructure-Organized/infranest-mcp/main/.github/assets/infranest-logo-dark.svg">
    <img alt="InfraNest" src="https://raw.githubusercontent.com/InfraNest-Infrastructure-Organized/infranest-mcp/main/.github/assets/infranest-logo-light.svg" width="300">
  </picture>
</p>

<h1 align="center">infranest-mcp</h1>

<p align="center">
  <strong>Ask your AI assistant about your infrastructure.</strong><br>
  What is down, where a hostname points, what expires soon, who changed what. Hosted, nothing to install.
</p>

<p align="center">
  <a href="https://github.com/InfraNest-Infrastructure-Organized/infranest-mcp/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/InfraNest-Infrastructure-Organized/infranest-mcp/actions/workflows/ci.yml/badge.svg"></a>
  <img alt="MCP: streamable HTTP" src="https://img.shields.io/badge/MCP-streamable%20HTTP-6E56CF">
  <img alt="Access: reads, on-call actions only when allowed" src="https://img.shields.io/badge/access-reads%20%2B%20on--call%20actions%20when%20allowed-brightgreen">
  <img alt="Licence: Apache-2.0" src="https://img.shields.io/badge/licence-Apache--2.0-blue">
</p>

---

[InfraNest](https://infranest.io) is one place for your servers, uptime monitors, incidents, DNS, domains and
certificates, across the cloud and DNS providers you already use. This is its hosted
[Model Context Protocol](https://modelcontextprotocol.io) server. Ask in plain language: what is down right now,
which monitors failed last night, where a hostname points, which domains and certificates expire soon, which
servers are running out of disk, and who changed what in the audit log.

```
https://api.infranest.io/mcp
```

[![Install in VS Code](https://img.shields.io/badge/VS_Code-Install_InfraNest-0098FF?logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=infranest&config=%7B%22type%22%3A%22http%22%2C%22url%22%3A%22https%3A%2F%2Fapi.infranest.io%2Fmcp%22%7D)
[![Add to Cursor](https://cursor.com/deeplink/mcp-install-dark.svg)](https://cursor.com/en/install-mcp?name=infranest&config=eyJ1cmwiOiJodHRwczovL2FwaS5pbmZyYW5lc3QuaW8vbWNwIn0=)

**It reads, and changes only what you allow.** Every tool reads, except a small on-call set — acknowledge an
incident, leave the team a note, silence a monitor, check a monitor again, start or end a maintenance window —
which needs write access to Monitoring: an API token with Monitoring write, or **Also let it act** ticked when you
connect. Each of those changes is undone by another, is recorded in your audit log, and your assistant asks before
making it. Nothing else can be created, changed or deleted, and it never returns secrets such as domain transfer
codes, private keys or tokens. Works on every InfraNest plan, including Free.

## Connect

**Assistants that support sign-in (OAuth)** — Claude, ChatGPT, VS Code, Cursor and others: add a custom
connector with the URL above, or use a button above. You sign in with your InfraNest account and choose the one
organization it may use; it sees only what your role there allows. Remove it any time under
**My account → Authorized apps**.

**Assistants that take a header instead** — create an API token in InfraNest (**My account → Developer**) and
send it as a bearer token:

```json
{
  "mcpServers": {
    "infranest": {
      "url": "https://api.infranest.io/mcp",
      "headers": { "Authorization": "Bearer <your InfraNest API token>" }
    }
  }
}
```

**Gemini CLI** — this repository is a Gemini CLI extension:

```sh
gemini extensions install https://github.com/InfraNest-Infrastructure-Organized/infranest-mcp
```

Gemini CLI opens the InfraNest sign-in the first time a tool is used.

No account yet? Sign up free at [infranest.io](https://infranest.io). A
[sandbox](https://developers.infranest.io/sandbox) with sample data lets you try every tool safely.

Step-by-step setup for each assistant: [developers.infranest.io/ai-assistants](https://developers.infranest.io/ai-assistants).

## Tools

| Tool | What it answers |
|---|---|
| `list_organizations` | Which organizations you can read |
| `status_overview` | Is everything up right now — monitors, servers, open incidents, running maintenance |
| `status_across_organizations` | Is anything down in any of your organizations, one line each |
| `search`, `fetch` | Find anything by name, then read the one you mean in full |
| `list_servers`, `get_server` | Your cloud servers, filtered by state, provider or tag |
| `server_attention` | What needs attention on a server |
| `server_metrics`, `server_metric_history` | Servers with their latest CPU, memory and disk figures, and one server's over time |
| `list_monitors`, `get_monitor` | Your uptime monitors |
| `monitor_stats`, `monitor_results` | Uptime and response times of a monitor, and its recent check results |
| `list_incidents`, `incident_timeline` | Incidents and what happened during each |
| `list_deploys`, `deploy_changes` | Deploys to a monitor or server, and what each changed |
| `list_dns_zones`, `list_dns_records` | DNS zones and their records |
| `search_dns`, `check_dns_name` | Where a hostname points across all zones, and everything about one name, live DNS included |
| `dns_zone_changes`, `dns_outside_changes` | Recent changes to a zone, in InfraNest and made directly at the DNS provider |
| `list_domains`, `domain_findings` | Domains with expiry and renewal state, and what is wrong with any of them, in one call |
| `list_certificates` | Certificates, with expiry |
| `list_status_pages` | Your public status pages |
| `list_dynamic_ips` | Dynamic IPs and the records they keep up to date |
| `list_maintenance_windows` | Planned maintenance |
| `search_audit_log` | Who changed what, and when |
| `uptime_report` | Monthly uptime report |
| `read_api` | Any other read in the [public API](https://developers.infranest.io/reference) |

**On-call actions**, only with write access to Monitoring:

| Tool | What it does | Undone by |
|---|---|---|
| `acknowledge_incident`, `unacknowledge_incident` | Marks an incident as yours, stopping repeat alerts and telling the team | each other |
| `add_incident_note` | Leaves the team a note on an incident | — |
| `silence_monitor`, `unsilence_monitor` | Stops a monitor's alerts for a while; it keeps checking | each other |
| `run_monitor_check` | Checks a monitor again now instead of waiting for its schedule | — |
| `start_maintenance`, `end_maintenance` | Opens a maintenance window, so nobody is paged for planned work, and ends it. It is internal unless given a public notice, the text your status pages show | each other |

## Prompts

Ready-made questions in your assistant's prompt menu:

| Prompt | What you get |
|---|---|
| Health check (`health_check`) | What is down now and what needs attention this month: incidents, servers, domains, certificates, DNS |
| Investigate an incident (`investigate_incident`) | Why something is down: the incident, what it affects, what changed just before it, what to do next |
| What changed recently (`what_changed`) | Everything that changed in a period: settings, deploys, DNS edits in InfraNest and at the provider |
| Monthly uptime report (`monthly_report`) | A report fit to send a customer: uptime against target, each incident with its cause, planned maintenance |

## What is in this repository

The server itself is hosted by InfraNest; its source is not here. This repository holds what MCP clients and
directories read about it:

| File | Read by |
|---|---|
| [`server.json`](server.json) | The official [MCP Registry](https://registry.modelcontextprotocol.io), as `io.infranest/infranest` |
| [`gemini-extension.json`](gemini-extension.json), [`GEMINI.md`](GEMINI.md) | Gemini CLI and its extension gallery |
| This README | You, and the MCP directories that list the server |

CI checks the files against the registry's schema and against each other on every change, and every week
checks the tool table above against the tools the live server describes.

## Links

- [Use InfraNest from an AI assistant](https://developers.infranest.io/ai-assistants), on the developer site, and
  the same in the [help center](https://infranest.io/docs/ai-assistants/)
- [Developer documentation](https://developers.infranest.io) and the [API reference](https://developers.infranest.io/reference)
- [infranest-openapi](https://github.com/InfraNest-Infrastructure-Organized/infranest-openapi): the API description
- [infranest-examples](https://github.com/InfraNest-Infrastructure-Organized/infranest-examples): ready-to-run scripts for the API
- [Service status](https://status.infranest.io)
- [Privacy policy](https://infranest.io/privacy) · [Terms of Service](https://infranest.io/terms)

Found a problem? Open an [issue](https://github.com/InfraNest-Infrastructure-Organized/infranest-mcp/issues), or
write to support@infranest.io. For a security issue in InfraNest, see
[infranest.io/security](https://infranest.io/security).

## Licence

The files in this repository are under the [Apache License 2.0](LICENSE). Your use of InfraNest is governed by its
[Terms of Service](https://infranest.io/terms).
