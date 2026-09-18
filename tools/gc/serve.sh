#!/usr/bin/env bash
# tools/gc/serve.sh - 启动 GoatCounter 自托管实例
set -euo pipefail
GC_BIN="${GOATCOUNTER_GC:-./tools/gc/gc}"
if [[ ! -x "$GC_BIN" ]]; then echo "ERROR: gc not found" >&2; exit 1; fi
if [[ -z "${GOATCOUNTER_DB:-}" ]]; then echo "ERROR: GOATCOUNTER_DB must be set" >&2; exit 1; fi
exec "$GC_BIN" serve --db "sqlite+${GOATCOUNTER_DB}" --listen "${GOATCOUNTER_LISTEN:-:8080}" ${GOATCOUNTER_TLS:+--tls "$GOATCOUNTER_TLS"} ${GOATCOUNTER_AUTOMIGRATE:+--automigrate}
