#!/usr/bin/env bash
# tools/gc/download_gc.sh - 下载 GoatCounter 自托管二进制
# 用法: ./tools/gc/download_gc.sh [版本]
set -euo pipefail
VERSION="${1:-v2.7.0}"
BIN_NAME="goatcounter-${VERSION}-linux-amd64"
BIN_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_PATH="${BIN_DIR}/gc"
TARBALL="${BIN_DIR}/${BIN_NAME}.gz"
echo "[download] fetching ${VERSION}"
curl -fSL --max-time 180 "https://github.com/arp242/goatcounter/releases/download/${VERSION}/${BIN_NAME}.gz" -o "$TARBALL"
gunzip -f "$TARBALL"
mv "${BIN_DIR}/${BIN_NAME}" "$BIN_PATH"
chmod 755 "$BIN_PATH"
echo "[download] installed: $BIN_PATH"
"$BIN_PATH" version
