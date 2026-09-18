#!/usr/bin/env bash
# tools/gc/init_site.sh - 首次初始化 GoatCounter 自托管站点
set -euo pipefail
GC_BIN="${GOATCOUNTER_GC:-./tools/gc/gc}"
if [[ ! -x "$GC_BIN" ]]; then echo "ERROR: gc binary not found" >&2; exit 1; fi
if [[ -z "${GOATCOUNTER_DB:-}" ]]; then echo "ERROR: GOATCOUNTER_DB must be set" >&2; exit 1; fi
DB_DIR="$(dirname "$(readlink -f "$GOATCOUNTER_DB")")"
mkdir -p "$DB_DIR"
echo "[init] db=$GOATCOUNTER_DB"
$GC_BIN db create site --db "sqlite+${GOATCOUNTER_DB}" -createdb -vhost "protreptic.goatcounter.local" -user.email "admin@example.invalid" -user.password "$(openssl rand -base64 16)" 2>&1 || true
$GC_BIN db create apitoken --db "sqlite+${GOATCOUNTER_DB}" -name "Protreptic Stats" -user 1 -perm count 2>&1 || true
echo "[init] done. Dashboard: $GC_BIN serve --db "sqlite+${GOATCOUNTER_DB}" --listen :8080"
