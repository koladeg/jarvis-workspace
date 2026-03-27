#!/bin/bash
# reminder-daemon.sh
# Reliable reminder daemon: cron wakes this every 5 minutes, Python handles JSON + schedule matching.

set -euo pipefail

WORKSPACE="${WORKSPACE:-/home/claw/.openclaw/workspace}"
CONFIG_FILE="${WORKSPACE}/config/reminders.json"
STATE_DIR="${WORKSPACE}/.reminder-state"
LOG_FILE="${WORKSPACE}/logs/reminder-daemon.log"
LOCK_DIR="${STATE_DIR}/.lock"
CRED_FILE="${WORKSPACE}/.credentials/telegram_bot_config.txt"

mkdir -p "${STATE_DIR}" "$(dirname "${LOG_FILE}")"

log() {
  local level="$1"; shift
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" >> "${LOG_FILE}"
}

acquire_lock() {
  mkdir "${LOCK_DIR}" 2>/dev/null
}

release_lock() {
  rm -rf "${LOCK_DIR}" 2>/dev/null || true
}

trap release_lock EXIT

if ! acquire_lock; then
  log WARN "Could not acquire lock, skipping run"
  exit 0
fi

if [ ! -f "${CONFIG_FILE}" ]; then
  log ERROR "Config file not found: ${CONFIG_FILE}"
  exit 1
fi

if [ ! -f "${CRED_FILE}" ]; then
  log ERROR "Credentials file not found: ${CRED_FILE}"
  exit 1
fi

set -a
source "${CRED_FILE}"
set +a

export WORKSPACE CONFIG_FILE STATE_DIR LOG_FILE

python3 <<'PY'
import json, os, subprocess, datetime, pathlib, sys

workspace = pathlib.Path(os.environ['WORKSPACE'])
config_file = pathlib.Path(os.environ['CONFIG_FILE'])
state_dir = pathlib.Path(os.environ['STATE_DIR'])
log_file = pathlib.Path(os.environ['LOG_FILE'])

now = datetime.datetime.utcnow().replace(second=0, microsecond=0)

with config_file.open() as f:
    config = json.load(f)

channels = config.get('telegram', {}).get('channels', {})
reminders = config.get('reminders', [])


def log(level, message):
    with log_file.open('a') as f:
        ts = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        f.write(f'[{ts}] [{level}] {message}\n')


def cron_match(expr, dt):
    parts = expr.split()
    if len(parts) != 5:
        return False
    vals = [dt.minute, dt.hour, dt.day, dt.month, (dt.weekday()+1)%7]
    for part, val in zip(parts, vals):
        if part == '*':
            continue
        if part.startswith('*/'):
            step = int(part[2:])
            if val % step != 0:
                return False
        else:
            try:
                if int(part) != val:
                    return False
            except ValueError:
                return False
    return True


def state_path(reminder_id):
    return state_dir / f'{reminder_id}.state'


def already_sent(reminder):
    sp = state_path(reminder['id'])
    if not sp.exists():
        return False
    last = sp.read_text().strip()
    mode = reminder.get('dedupe', 'day')
    if mode == 'once':
        return True
    if mode == 'minute':
        return last == now.strftime('%Y-%m-%d %H:%M')
    return last == now.strftime('%Y-%m-%d')


def mark_sent(reminder):
    sp = state_path(reminder['id'])
    mode = reminder.get('dedupe', 'day')
    value = now.strftime('%Y-%m-%d %H:%M') if mode == 'minute' else now.strftime('%Y-%m-%d')
    if mode == 'once':
        value = now.strftime('%Y-%m-%d %H:%M')
    sp.write_text(value)


sent = 0
log('INFO', 'Starting reminder daemon check')

for reminder in reminders:
    if not reminder.get('enabled', False):
        continue
    rid = reminder.get('id')
    sched = reminder.get('schedule')
    channel_key = reminder.get('channel')
    message = reminder.get('message', '')
    if not rid or not sched or not channel_key or not message:
        continue
    if not cron_match(sched, now):
        continue
    if already_sent(reminder):
        continue
    channel = channels.get(channel_key, {})
    chat_id = channel.get('chat_id')
    if not chat_id:
        log('ERROR', f'No chat_id for channel {channel_key} ({rid})')
        continue

    token = os.environ.get('TELEGRAM_BOT_TOKEN')
    if not token:
        log('ERROR', 'TELEGRAM_BOT_TOKEN missing')
        continue

    cmd = [
        'curl', '-sS', '-X', 'POST',
        f'https://api.telegram.org/bot{token}/sendMessage',
        '-d', f'chat_id={chat_id}',
        '-d', f'text={message}',
        '-d', 'parse_mode=Markdown'
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0 and '"ok":true' in result.stdout:
        mark_sent(reminder)
        sent += 1
        log('INFO', f'✓ Reminder sent: {rid} -> {channel_key}')
        if reminder.get('dedupe') == 'once':
            reminder['enabled'] = False
    else:
        out = (result.stdout or '') + ' ' + (result.stderr or '')
        log('ERROR', f'Failed to send {rid}: {out[:400]}')

# auto-disable one-time reminders after send
with config_file.open('w') as f:
    json.dump(config, f, indent=2)
    f.write('\n')

log('INFO', f'Daemon check complete. Sent {sent} message(s)')
PY
