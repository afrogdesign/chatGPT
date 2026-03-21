#!/bin/zsh
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PLIST_SRC="$ROOT_DIR/launchd/com.afrog.xbot.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.afrog.xbot.plist"

mkdir -p "$HOME/Library/LaunchAgents"
sed "s#__ROOT_DIR__#$ROOT_DIR#g" "$PLIST_SRC" > "$PLIST_DST"
launchctl unload "$PLIST_DST" >/dev/null 2>&1 || true
launchctl load "$PLIST_DST"

echo "installed: $PLIST_DST"
echo "check with: launchctl list | grep com.afrog.xbot"
