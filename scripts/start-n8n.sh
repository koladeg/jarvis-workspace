#!/usr/bin/env bash
set -euo pipefail

export PATH="/home/claw/.npm-global/bin:/usr/local/bin:/usr/bin:/bin"
export N8N_HOST="127.0.0.1"
export N8N_PORT="5678"
export N8N_PROTOCOL="http"
export N8N_SECURE_COOKIE="false"
export N8N_LISTEN_ADDRESS="127.0.0.1"
export N8N_USER_FOLDER="/home/claw/.n8n"
export N8N_LOG_LEVEL="info"

mkdir -p /home/claw/.n8n /home/claw/.openclaw/workspace/logs

exec /home/claw/.npm-global/bin/n8n start >> /home/claw/.openclaw/workspace/logs/n8n.log 2>&1
