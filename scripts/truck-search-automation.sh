#!/usr/bin/env bash
set -Eeuo pipefail

# Truck search automation
# - Scrapes Autoline.de, AutoScout24, and eBay Motors with agent-browser
# - Filters candidate trucks against configurable rules
# - Stores results locally as JSON (always) and optionally mirrors to Notion
# - Posts new matches to Telegram when credentials are supplied
# - Designed for cron / OpenClaw scheduler

WORKSPACE="/home/claw/.openclaw/workspace"
SCRIPT_DIR="$WORKSPACE/scripts"
DATA_DIR="$WORKSPACE/outputs/truck-search"
RAW_DIR="$DATA_DIR/raw"
STATE_DIR="$DATA_DIR/state"
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/truck-search-automation.log"
JSON_DB="$DATA_DIR/truck-listings.json"
SEEN_FILE="$STATE_DIR/seen-urls.txt"
RUNTIME_DIR="${TMPDIR:-/tmp}/truck-search-automation"

mkdir -p "$DATA_DIR" "$RAW_DIR" "$STATE_DIR" "$LOG_DIR" "$RUNTIME_DIR"
touch "$LOG_FILE" "$SEEN_FILE"

BRANDS=(HOWO DAF IVECO MAN MACK FAW)
COUNTRIES=(Germany UK Netherlands France Belgium Poland)
HP_TARGETS=(380 400 430)
MAX_AGE=15
MAX_PRICE_GBP=4000
CURRENT_YEAR="$(date -u +%Y)"
MIN_YEAR=$((CURRENT_YEAR - MAX_AGE))
TELEGRAM_GROUP_NAME="${TELEGRAM_GROUP_NAME:-Jarvis-Truck-Listings}"
TELEGRAM_BOT_TOKEN="8733839699:AAEwhBgxZ7Lj9O894AQwlcVjoR3cv5zg1vo"
TELEGRAM_CHAT_ID="-5025917446"
NOTION_TOKEN="${NOTION_TOKEN:-}"
NOTION_DATABASE_ID="${NOTION_DATABASE_ID:-}"
NOTION_VERSION="2022-06-28"
DRY_RUN="${DRY_RUN:-0}"

log() {
  local level="$1"; shift
  printf '%s [%s] %s\n' "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" "$level" "$*" | tee -a "$LOG_FILE" >&2
}

cleanup() {
  rm -rf "$RUNTIME_DIR"/* 2>/dev/null || true
}
trap cleanup EXIT
trap 'log ERROR "Command failed at line $LINENO: $BASH_COMMAND"' ERR

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || { log ERROR "Missing command: $1"; exit 1; }
}

json_escape() {
  python3 - <<'PY' "$1"
import json, sys
print(json.dumps(sys.argv[1]))
PY
}

browser_open() {
  local url="$1"
  agent-browser open "$url" >/dev/null
}

browser_snapshot() {
  agent-browser snapshot -c -d 8
}

snapshot_to_json() {
  local source="$1"
  python3 - "$source" <<'PY'
import json, re, sys
source = sys.argv[1]
items = []
for line in sys.stdin.read().splitlines():
    line = line.strip()
    if not line or ('link ' not in line and 'heading ' not in line and 'cell ' not in line):
        continue
    m = re.search(r'"([^"]+)"', line)
    if not m:
        continue
    title = m.group(1).strip()
    if len(title) < 6:
        continue
    if title.lower() in {'suche', 'suchen', 'autoline deutschland', 'autoline'}:
        continue
    refm = re.search(r'\[ref=(e\d+)\]', line)
    ref = refm.group(1) if refm else None
    items.append({
        'title': title,
        'url': f'{source}://{ref or title[:40]}',
        'text': title,
        'ref': ref,
    })
print(json.dumps(items, ensure_ascii=False))
PY
}

save_raw() {
  local source="$1"; shift
  local kind="$1"; shift
  local path="$RAW_DIR/${source}-${kind}-$(date -u +%Y%m%dT%H%M%SZ).txt"
  cat > "$path"
  printf '%s\n' "$path"
}

run_python_filter() {
  python3 - "$@" <<'PY'
import json, re, sys, urllib.parse
source = sys.argv[1]
brands = sys.argv[2].split(',')
countries = sys.argv[3].split(',')
hp_targets = [int(x) for x in sys.argv[4].split(',')]
min_year = int(sys.argv[5])
max_price_gbp = int(sys.argv[6])
raw = sys.stdin.read().strip()
if not raw:
    print('[]')
    raise SystemExit(0)
try:
    items = json.loads(raw)
except Exception:
    print('[]')
    raise SystemExit(0)
country_words = [c.lower() for c in countries]
brand_words = [b.lower() for b in brands]
results = []
for item in items:
    title = (item.get('title') or '').strip()
    url = item.get('url') or ''
    text = (item.get('text') or '').strip()
    hay = f"{title} {text}".lower()
    if not any(b in hay for b in brand_words):
        continue
    if '4x2' not in hay and '4×2' not in hay:
        continue
    if not any(word in hay for word in ['flatbed', 'platform', 'dropside', 'pritsche', 'plateau']):
        continue
    hp = None
    hp_match = re.search(r'\b(380|400|430)\s*(?:hp|ps|cv|pk)\b', hay)
    if hp_match:
        hp = int(hp_match.group(1))
    else:
        for t in hp_targets:
            if f' {t} ' in f' {hay} ':
                hp = t
                break
    if hp is None:
        continue
    years = [int(y) for y in re.findall(r'\b(20\d{2}|19\d{2})\b', text)]
    year = max([y for y in years if 1990 <= y <= 2030], default=None)
    if year and year < min_year:
        continue
    price = None
    # crude FX normalization into GBP
    for cur, fx in [('£',1.0), ('€',0.86), ('$',0.79), ('pln',0.20), ('zł',0.20)]:
        if cur in hay:
            m = re.search(rf'{re.escape(cur)}\s*([\d., ]+)', hay)
            if m:
                value = re.sub(r'[^\d.]', '', m.group(1).replace(',', ''))
                try:
                    price = round(float(value)*fx)
                    break
                except Exception:
                    pass
    if price is None:
        m = re.search(r'([\d., ]+)\s*(eur|gbp|usd)', hay)
        if m:
            value = re.sub(r'[^\d.]', '', m.group(1).replace(',', ''))
            fx = {'eur':0.86,'gbp':1.0,'usd':0.79}[m.group(2)]
            try:
                price = round(float(value)*fx)
            except Exception:
                pass
    if price is not None and price > max_price_gbp:
        continue
    country = next((c for c in countries if c.lower() in hay), None)
    if country is None:
        parsed = urllib.parse.urlparse(url)
        domain = parsed.netloc.lower()
        domain_map = {
            'de': 'Germany', 'co.uk':'UK', 'uk':'UK', 'nl':'Netherlands',
            'fr':'France', 'be':'Belgium', 'pl':'Poland'
        }
        for key, val in domain_map.items():
            if domain.endswith(key) or f'.{key}/' in url.lower():
                country = val
                break
    if country and country not in countries:
        continue
    condition_ok = any(w in hay for w in ['used', 'gebraucht', 'occasion', 'good', 'clean', 'running', 'working'])
    if not condition_ok:
        # soft filter, still keep if rest strongly matches
        pass
    results.append({
        'source': source,
        'title': title,
        'url': url,
        'country': country,
        'year': year,
        'price_gbp_est': price,
        'horsepower': hp,
        'raw_text': text[:1200],
    })
print(json.dumps(results, ensure_ascii=False))
PY
}

merge_results() {
  local incoming_json
  incoming_json="$(cat)"
  python3 -c '
import json, sys, pathlib
json_db = pathlib.Path(sys.argv[1])
seen_file = pathlib.Path(sys.argv[2])
incoming = json.loads(sys.argv[3] or "[]")
existing = []
if json_db.exists():
    try:
        existing = json.loads(json_db.read_text())
    except Exception:
        existing = []
seen = set(x.strip() for x in seen_file.read_text().splitlines() if x.strip()) if seen_file.exists() else set()
merged = {item.get("url"): item for item in existing if item.get("url")}
new_items = []
for item in incoming:
    url = item.get("url")
    if not url:
        continue
    merged[url] = item
    if url not in seen:
        new_items.append(item)
        seen.add(url)
json_db.write_text(json.dumps(list(merged.values()), indent=2, ensure_ascii=False))
seen_file.write_text("\n".join(sorted(seen)) + ("\n" if seen else ""))
print(json.dumps({"all": list(merged.values()), "new": new_items}, ensure_ascii=False))
' "$JSON_DB" "$SEEN_FILE" "$incoming_json"
}

post_telegram() {
  local text="$1"
  if [[ -z "$TELEGRAM_BOT_TOKEN" || -z "$TELEGRAM_CHAT_ID" ]]; then
    log WARN "Telegram not configured; skipping post to ${TELEGRAM_GROUP_NAME}. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID."
    return 0
  fi
  if [[ "$DRY_RUN" == "1" ]]; then
    log INFO "DRY_RUN=1, Telegram post suppressed"
    return 0
  fi
  curl -fsS -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    --data-urlencode "chat_id=${TELEGRAM_CHAT_ID}" \
    --data-urlencode "text=${text}" \
    --data-urlencode 'disable_web_page_preview=true' >/dev/null
  log INFO "Telegram post sent to ${TELEGRAM_GROUP_NAME}"
}

post_notion() {
  local listings_json="$1"
  if [[ -z "$NOTION_TOKEN" || -z "$NOTION_DATABASE_ID" ]]; then
    log INFO "Notion not configured; keeping local JSON only"
    return 0
  fi
  if [[ "$DRY_RUN" == "1" ]]; then
    log INFO "DRY_RUN=1, Notion writes suppressed"
    return 0
  fi
  python3 - "$NOTION_TOKEN" "$NOTION_DATABASE_ID" "$NOTION_VERSION" <<'PY' <<< "$listings_json"
import json, sys, urllib.request

token, db_id, notion_version = sys.argv[1:4]
items = json.loads(sys.stdin.read() or '[]')
for item in items[:10]:
    payload = {
        'parent': {'database_id': db_id},
        'properties': {
            'Name': {'title': [{'text': {'content': item.get('title','Untitled')[:180]}}]},
            'Source': {'rich_text': [{'text': {'content': item.get('source','')}}]},
            'URL': {'url': item.get('url')},
            'Country': {'rich_text': [{'text': {'content': item.get('country') or ''}}]},
            'Year': {'number': item.get('year')},
            'Price GBP': {'number': item.get('price_gbp_est')},
            'Horsepower': {'number': item.get('horsepower')},
        }
    }
    req = urllib.request.Request(
        'https://api.notion.com/v1/pages',
        data=json.dumps(payload).encode(),
        headers={
            'Authorization': f'Bearer {token}',
            'Notion-Version': notion_version,
            'Content-Type': 'application/json',
        },
        method='POST'
    )
    try:
        urllib.request.urlopen(req, timeout=20).read()
    except Exception as e:
        print(f'Notion write failed for {item.get("url")}: {e}', file=sys.stderr)
PY
  log INFO "Best-effort Notion sync attempted"
}

search_autoline() {
  log INFO "Searching Autoline"
  browser_open 'https://www.autoline.de/'
  sleep 2
  local snap search_ref search_button_ref query cards_json filtered_json
  snap="$(browser_snapshot)"
  printf '%s\n' "$snap" > "$RUNTIME_DIR/autoline-home.snapshot"
  search_ref="$( { printf '%s\n' "$snap" | grep -m1 -E 'textbox ".*Suche' | sed -E 's/.*\[ref=(e[0-9]+)\].*/@\1/'; } || true )"
  search_button_ref="$( { printf '%s\n' "$snap" | grep -m1 'button "Suche"' | sed -E 's/.*\[ref=(e[0-9]+)\].*/@\1/'; } || true )"
  query='MAN 4x2 flatbed 400 hp used'
  if [[ -n "$search_ref" ]]; then
    agent-browser type "$search_ref" "$query" >/dev/null || true
  fi
  if [[ -n "$search_button_ref" ]]; then
    agent-browser click "$search_button_ref" >/dev/null || true
  else
    agent-browser press Enter >/dev/null || true
  fi
  sleep 3
  snap="$(browser_snapshot)"
  printf '%s\n' "$snap" | save_raw autoline snapshot >/dev/null
  cards_json="$(printf '%s\n' "$snap" | snapshot_to_json autoline)"
  printf '%s\n' "$cards_json" | save_raw autoline cards >/dev/null
  filtered_json="$(printf '%s' "$cards_json" | run_python_filter autoline "$(IFS=,; echo "${BRANDS[*]}")" "$(IFS=,; echo "${COUNTRIES[*]}")" "$(IFS=,; echo "${HP_TARGETS[*]}")" "$MIN_YEAR" "$MAX_PRICE_GBP")"
  printf '%s\n' "$filtered_json"
}

search_autoscout24() {
  log INFO "Searching AutoScout24"
  browser_open 'https://www.autoscout24.com/'
  sleep 2
  local snap cards_json filtered_json
  snap="$(browser_snapshot)"
  printf '%s\n' "$snap" | save_raw autoscout24 snapshot >/dev/null
  cards_json="$(printf '%s\n' "$snap" | snapshot_to_json autoscout24)"
  printf '%s\n' "$cards_json" | save_raw autoscout24 cards >/dev/null
  filtered_json="$(printf '%s' "$cards_json" | run_python_filter autoscout24 "$(IFS=,; echo "${BRANDS[*]}")" "$(IFS=,; echo "${COUNTRIES[*]}")" "$(IFS=,; echo "${HP_TARGETS[*]}")" "$MIN_YEAR" "$MAX_PRICE_GBP")"
  printf '%s\n' "$filtered_json"
}

search_ebay_motors() {
  log INFO "Searching eBay Motors"
  browser_open 'https://www.ebay.co.uk/sch/i.html?_nkw=MAN+4x2+flatbed+truck+400hp+used'
  sleep 2
  local snap cards_json filtered_json
  snap="$(browser_snapshot)"
  printf '%s\n' "$snap" | save_raw ebay-motors snapshot >/dev/null
  cards_json="$(printf '%s\n' "$snap" | snapshot_to_json ebay-motors)"
  printf '%s\n' "$cards_json" | save_raw ebay-motors cards >/dev/null
  filtered_json="$(printf '%s' "$cards_json" | run_python_filter ebay-motors "$(IFS=,; echo "${BRANDS[*]}")" "$(IFS=,; echo "${COUNTRIES[*]}")" "$(IFS=,; echo "${HP_TARGETS[*]}")" "$MIN_YEAR" "$MAX_PRICE_GBP")"
  printf '%s\n' "$filtered_json"
}

format_telegram_message() {
  python3 - <<'PY' "$1"
import json, sys
items = json.loads(sys.argv[1])
header = '🚛 Truck listing scan complete\nCriteria: HOWO/DAF/IVECO/MAN/MACK/FAW | 4x2 flatbed | 380/400/430hp | <=15 years | <=£4,000\n'
if not items:
    print(header + '\nNo new matches found this run.')
    raise SystemExit(0)
lines = [header, f'New matches: {len(items)}']
for item in items[:8]:
    parts = [item.get('title') or 'Untitled']
    meta = []
    if item.get('country'): meta.append(item['country'])
    if item.get('year'): meta.append(str(item['year']))
    if item.get('horsepower'): meta.append(f"{item['horsepower']}hp")
    if item.get('price_gbp_est') is not None: meta.append(f"~£{item['price_gbp_est']}")
    if meta:
        parts.append(' | '.join(meta))
    parts.append(item.get('url') or '')
    lines.append('\n'.join(parts))
print('\n\n'.join(lines))
PY
}

main() {
  require_cmd agent-browser
  require_cmd python3
  require_cmd curl

  log INFO "Truck search automation started"
  log INFO "Filters: brands=${BRANDS[*]} min_year=${MIN_YEAR} max_price_gbp=${MAX_PRICE_GBP} hp=${HP_TARGETS[*]}"

  local all_json merge_json new_json telegram_text
  local autoline_json autoscout_json ebay_json
  autoline_json="$(search_autoline)"
  autoscout_json="$(search_autoscout24)"
  ebay_json="$(search_ebay_motors)"
  all_json="$(python3 - <<'PY' "$autoline_json" "$autoscout_json" "$ebay_json"
import json, sys
items = []
for raw in sys.argv[1:]:
    try:
        data = json.loads(raw)
        if isinstance(data, list):
            items.extend(data)
    except Exception:
        pass
print(json.dumps(items, ensure_ascii=False))
PY
)"

  printf '%s' "$all_json" | save_raw combined filtered >/dev/null
  merge_json="$(printf '%s' "$all_json" | merge_results)"
  new_json="$(python3 - <<'PY' "$merge_json"
import json, sys
print(json.dumps(json.loads(sys.argv[1]).get('new', []), ensure_ascii=False))
PY
)"

  post_notion "$new_json"
  telegram_text="$(format_telegram_message "$new_json")"
  post_telegram "$telegram_text"

  log INFO "Run complete. Stored listings at $JSON_DB"
  log INFO "New matches this run: $(python3 - <<'PY' "$new_json"
import json, sys
print(len(json.loads(sys.argv[1])))
PY
)"
}

main "$@"
