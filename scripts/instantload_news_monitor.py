#!/usr/bin/env python3
import json, re, sys, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
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

STRONG_KEYWORDS = [
    'nerc', 'ikeja electric', 'eko electric', 'abuja electric', 'mojec',
    'remote token', 'sts 2.0', 'vending', 'smart meter', 'prepaid meter'
]

EXCLUDE_TITLE_PATTERNS = [
    r'\bhow to\b',
    r'\bhelpful guide\b',
    r'\bdetailed guide\b',
    r'\bexplains how to get\b',
]

MAX_AGE_DAYS = 120


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


def parse_pub_date(pub):
    try:
        dt = parsedate_to_datetime(pub)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def is_recent_enough(item):
    dt = parse_pub_date(item.get('pubDate', ''))
    if not dt:
        return False
    return dt >= datetime.now(timezone.utc) - timedelta(days=MAX_AGE_DAYS)


def is_excluded_title(title):
    t = title.lower()
    return any(re.search(p, t) for p in EXCLUDE_TITLE_PATTERNS)


def normalized_title(title):
    t = re.sub(r'\s+', ' ', title.lower()).strip()
    t = re.sub(r'[^a-z0-9 ]+', '', t)
    return t


def score_item(item):
    hay = (item['title'] + ' ' + item.get('source', '')).lower()
    score = 0
    for kw in MATERIAL_KEYWORDS:
        if kw in hay:
            score += 1
    if any(kw in hay for kw in STRONG_KEYWORDS):
        score += 2
    if is_recent_enough(item):
        score += 2
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

    # dedupe by link and near-duplicate title; drop stale/generic guide content
    uniq = []
    used_links = set()
    used_titles = set()
    for item in found:
        if item['link'] in used_links:
            continue
        if is_excluded_title(item['title']):
            continue
        if not is_recent_enough(item):
            continue
        nt = normalized_title(item['title'])
        if nt in used_titles:
            continue
        used_links.add(item['link'])
        used_titles.add(nt)
        item['score'] = score_item(item)
        uniq.append(item)

    uniq.sort(key=lambda x: (-x['score'], x.get('pubDate', ''), x['title']))
    material = [i for i in uniq if i['score'] >= 4]

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
