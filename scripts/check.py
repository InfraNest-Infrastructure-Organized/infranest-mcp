#!/usr/bin/env python3
"""Checks that the files here describe the server they point at, and agree with each other.

The registry entry, the Gemini CLI extension and the README all name the same URL and version, and nothing
but this script ties them together. With --live it also compares the README's tool table with the tools the
hosted server describes in its server card, so a tool added or renamed there is noticed here within a week.
"""

import base64
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

URL = "https://api.infranest.io/mcp"
CARD = "https://api.infranest.io/.well-known/mcp/server-card.json"
NAME = "io.infranest/infranest"
REPOSITORY = "https://github.com/InfraNest-Infrastructure-Organized/infranest-mcp"

problems = []


def check(ok, message):
    if not ok:
        problems.append(message)


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def fetch_json(url):
    request = urllib.request.Request(url, headers={"User-Agent": "infranest-mcp-ci"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return json.load(response)


server = load("server.json")
extension = load("gemini-extension.json")
readme = open("README.md", encoding="utf-8").read()

# The registry entry, against the schema it names.
import jsonschema  # noqa: E402  (installed by the workflow; the rest needs only the standard library)

schema = fetch_json(server["$schema"])
for error in jsonschema.validators.validator_for(schema)(schema).iter_errors(server):
    problems.append(f"server.json: {error.json_path}: {error.message}")

check(server["name"] == NAME, f"server.json: the name is {server['name']!r}; it is {NAME!r}, fixed by DNS")
check(len(server["description"]) <= 100, "server.json: the registry refuses a description over 100 characters")
check(server["remotes"] == [{"type": "streamable-http", "url": URL}], f"server.json: the one remote is {URL}")
check(server["repository"]["url"] == REPOSITORY, f"server.json: the repository is {REPOSITORY}")

# The Gemini CLI extension says the same.
check(extension["version"] == server["version"], "gemini-extension.json and server.json have different versions")
check(extension["description"] == server["description"], "gemini-extension.json and server.json describe it differently")
check(extension["mcpServers"]["infranest"]["httpUrl"] == URL, f"gemini-extension.json: httpUrl is not {URL}")
try:
    open(extension["contextFileName"]).close()
except OSError:
    problems.append(f"gemini-extension.json: contextFileName {extension['contextFileName']} does not exist")

# The README's URL and both install buttons.
check(f"```\n{URL}\n```" in readme, f"README: the URL block does not show {URL}")

cursor = re.search(r"cursor\.com/en/install-mcp\?name=infranest&config=([A-Za-z0-9+/=]+)", readme)
check(cursor and json.loads(base64.b64decode(cursor.group(1))) == {"url": URL}, "README: the Cursor button does not install " + URL)

vscode = re.search(r"vscode\.dev/redirect/mcp/install\?name=infranest&config=([^)\s]+)", readme)
check(
    vscode and json.loads(urllib.parse.unquote(vscode.group(1))) == {"type": "http", "url": URL},
    "README: the VS Code button does not install " + URL,
)

documented = set(re.findall(r"`([a-z_]+)`", "\n".join(l for l in readme.splitlines() if l.startswith("| `"))))
print(f"{len(documented)} tools in the README, version {server['version']}")

# The live server, on the weekly run and by hand.
if "--live" in sys.argv:
    try:
        card = fetch_json(CARD)
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
        # Before the card is deployed there is nothing to compare with. Say so rather than fail every run.
        print(f"::warning::{CARD} answers 404, so the tool table was not compared with the server")
    else:
        served = {tool["name"] for tool in card["tools"]}
        check(card["serverInfo"]["version"] == server["version"],
              f"the server is version {card['serverInfo']['version']}, server.json says {server['version']}")
        for name in sorted(served - documented):
            problems.append(f"README: the server has a tool {name} that the table does not list")
        for name in sorted(documented - served):
            problems.append(f"README: the table lists {name}, which the server does not have")
        print(f"{len(served)} tools on the server")

for problem in problems:
    print(f"::error::{problem}")
sys.exit(1 if problems else 0)
