#!/usr/bin/env python3
import json, re, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

BASE = Path('/home/claw/.openclaw/workspace/monitoring/instantload')
STATE_PATH = BASE / 'news_state.json'
LOG_PATH = BASE / 'news-log.md'
LATEST_PATH = BASE / 'latest-summary.json'
BASE.mkdir(parents=True, exist_ok=True)

QUERIES = [
    '"Instant Load" electricity Nigeria',
    '"remote token loading" Nigeria electricity',
    'Ikeja Electric Mojec remote token loading',
    'NERC prepaid meter STS 2.0 Nigeria',
    'Nigeria electricity vending meter smart meter',
    'Mojec meter Nigeria remote loading',
    'Eko Electric prepaid meter remote token',
    'Abuja Electric prepaid meter remote token',
    'Lagos power licence metering contractor Nigeria',
]

MATERIAL_KEYWORDS = [
    'nerc', 'ikeja electric', 'eko electric', 'abuja electric', 'mojec', 'meter',
    'prepaid', 'smart meter', 'remote token', 'sts 2.0', 'vending', 'licence',
    'permit', 'ministry of power', 'power minister', 'electricity act'
]


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return default
    return default


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def fetch_rss(query):
    url = 'https://news.google.com/rss/search?q=' + urllib.parse.quote(query) + '&hl=en-NG&gl=NG&ceid=NG:en'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read()


def normalize_link(link):
    return link.strip()


def text(s):
    return re.sub(r'\s+', ' ', s or '').strip()


def parse_items(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall('.//item'):
        title = text(item.findtext('title'))
        link = normalize_link(text(item.findtext('link')))
        pub = text(item.findtext('pubDate'))
        source = text(item.findtext('source'))
        items.append({'title': title, 'link': link, 'pubDate': pub, 'source': source})
    return items


def score_item(item):
    hay = (item['title'] + ' ' + item.get('source', '')).lower()
    score = 0
    for kw in MATERIAL_KEYWORDS:
        if kw in hay:
            score += 1
    return score


def main():
    state = load_json(STATE_PATH, {'seen_links': [], 'last_run': None})
    seen = set(state.get('seen_links', []))
    found = []
    errors = []
    for q in QUERIES:
        try:
            for item in parse_items(fetch_rss(q)):
                item['query'] = q
                if item['link'] not in seen:
                    found.append(item)
        except Exception as e:
            errors.append(f'{q}: {e}')
        time.sleep(1)

    # dedupe by link
    uniq = []
    used = set()
    for item in found:
        if item['link'] in used:
            continue
        used.add(item['link'])
        item['score'] = score_item(item)
        uniq.append(item)

    uniq.sort(key=lambda x: (-x['score'], x['title']))
    material = [i for i in uniq if i['score'] >= 2]

    ts = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    with LOG_PATH.open('a') as f:
        f.write(f'\n## Run {ts}\n')
        if uniq:
            for item in uniq[:25]:
                f.write(f"- [{item['title']}]({item['link']}) — {item.get('source','Unknown source')} | query: `{item['query']}` | score: {item['score']}\n")
        else:
            f.write('- No new items found.\n')
        if errors:
            f.write('\n### Errors\n')
            for e in errors:
                f.write(f'- {e}\n')

    latest = {
        'timestamp': ts,
        'new_items': len(uniq),
        'material_items': len(material),
        'material': material[:10],
        'top_items': uniq[:10],
        'errors': errors,
    }
    save_json(LATEST_PATH, latest)

    seen.update(i['link'] for i in uniq)
    state['seen_links'] = list(seen)[-1000:]
    state['last_run'] = ts
    save_json(STATE_PATH, state)

    print(json.dumps(latest, ensure_ascii=False))

if __name__ == '__main__':
    main()
