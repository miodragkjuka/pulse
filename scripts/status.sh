#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://pulse.local/status}"

response=$(curl -sf "$URL")

echo "$response" | jq .

down_count=$(echo "$response" | jq '[.sites[] | select(.up == false)] | length')

if [ "$down_count" -gt 0 ]; then
  echo "WARNING: $down_count site(s) down" >&2
  exit 1
fi

echo "All sites up"