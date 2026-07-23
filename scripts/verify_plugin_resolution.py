#!/usr/bin/env python3
"""Verify Codex plugin-list JSON resolves the expected installed version."""

import argparse
import json
import sys
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--plugin-id", required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--allow-available", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    payload: dict[str, Any] = json.load(sys.stdin)
    collections = ["installed"]
    if args.allow_available:
        collections.append("available")

    plugins = [
        plugin
        for collection in collections
        for plugin in payload.get(collection, [])
        if plugin.get("pluginId") == args.plugin_id
    ]
    if not plugins:
        print(f"{args.plugin_id} was not found in Codex plugin output", file=sys.stderr)
        return 1

    plugin = plugins[0]
    actual_version = plugin.get("version")
    if actual_version != args.expected_version:
        print(
            f"{args.plugin_id} resolved to {actual_version!r}, "
            f"expected {args.expected_version!r}",
            file=sys.stderr,
        )
        return 1

    if not args.allow_available and (
        not plugin.get("installed") or not plugin.get("enabled")
    ):
        print(f"{args.plugin_id} is not installed and enabled", file=sys.stderr)
        return 1

    print(
        f"{args.plugin_id} is installed and enabled at version {actual_version}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

