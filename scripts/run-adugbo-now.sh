#!/bin/bash
# One-time AdugboInsure run (triggered manually for 5-hour delay)

echo "[$(date)] Starting scheduled AdugboInsure automation..."

bash /home/claw/.openclaw/workspace/scripts/adugboinsure-funding-radar.sh
bash /home/claw/.openclaw/workspace/scripts/adugboinsure-grant-search.sh

echo "[$(date)] Scheduled AdugboInsure automation complete"
