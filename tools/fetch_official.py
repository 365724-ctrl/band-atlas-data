#!/usr/bin/env python3
"""Fetch the official files listed in official/manifest.json (standard library only).
For every item: download (or probe), then write official/<id>/meta.json (address, HTTP status, size, checksum, last-modified, when fetched, whether it changed)
and official/<id>/sample.txt (the first lines of a CSV, the keys of a JSON, the file list of a ZIP, the first page text markers of a PDF).
Raw files go to ./raw/ for the workflow to attach to the release; nothing large is committed to the repository.
usage: fetch_official.py [--only ID] [--force]"""
import csv, datetime, hashlib, io, json, os, re, sys, urllib.error, urllib.parse, urllib.request, zipfile

UA = 'band-atlas-official-fetch (github.com/365724-ctrl/band-atlas-data)'
NOW = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0, tzinfo=None)

FULL = {'User-Agent': 'Mozilla/5.0 (compatible; band-atlas-official-fetch/1.0; +https://github.com/365724-ctrl/band-atlas-data)', 'Accept': 'text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.7'}      # still says who is asking; some sites refuse a request without the usual Accept headers
def get(url, limit=400 * 2 ** 20):
    """One download. A site that answers 403 to the plain request (Ofcom, the FCC) is asked once more with the full set of usual headers, under the same
    name. A site that still refuses is not worked around: the entry is reported as failed and fetched another way (by hand, or from the project's server)."""
    for hdr in ({'User-Agent': UA, 'Accept': '*/*'}, FULL):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=hdr), timeout=180) as r:
                body = r.read(limit + 1)
                if len(body) > limit: raise ValueError('larger than %d MB' % (limit // 2 ** 20))
                return r.status, dict(r.headers), body, r.geturl()
        except urllib.error.HTTPError as e:
            if e.code != 403 or hdr is FULL: raise

def sample(body, name, ctype):
    low = (name or '').lower(); head = body[:4]
    try:
        if head[:2] == b'PK':
            z = zipfile.ZipFile(io.BytesIO(body)); out = ['ZIP: %d files' % len(z.namelist())] + ['  %s  %d bytes' % (i.filename, i.file_size) for i in z.infolist()[:60]]
            for i in z.infolist():      # the first lines of the first table inside
                if i.filename.lower().endswith(('.csv', '.txt')) and i.file_size:
                    out += ['--- first lines of %s' % i.filename] + z.open(i).read(6000).decode('utf-8', 'replace').splitlines()[:12]; break
            return '\n'.join(out)
        if head == b'%PDF': return 'PDF: %d bytes; markers: %s' % (len(body), ', '.join(sorted(set(m.decode('latin-1') for m in re.findall(rb'Generated \d+ \w+ \d{4}', body[:400000])))[:5]) or 'none found')
        text = body[:200000].decode('utf-8-sig', 'replace')
        if text.lstrip()[:1] in '{[':
            try:
                j = json.loads(body.decode('utf-8-sig', 'replace'))
                if isinstance(j, dict):
                    out = ['JSON object, keys: ' + ', '.join(list(j)[:40])]
                    for k in ('resources', 'results', 'data', 'records'):
                        if isinstance(j.get(k), list): out += ['%s: %d entries; first: %s' % (k, len(j[k]), json.dumps(j[k][0], ensure_ascii=False)[:1500] if j[k] else '-')] + ['  %s | %s | %s | %s' % (x.get('title'), x.get('format'), x.get('last_modified'), x.get('url')) for x in j[k][:20] if isinstance(x, dict) and x.get('url')]
                    return '\n'.join(out)
                return 'JSON array, %d entries; first: %s' % (len(j), json.dumps(j[0], ensure_ascii=False)[:1500] if j else '-')
            except ValueError: pass
        lines = text.splitlines()
        if low.endswith('.csv') or 'csv' in (ctype or '') or (lines and lines[0].count(';') + lines[0].count(',') >= 3):
            return 'CSV: %d bytes, about %d lines in the first 200 kB\n' % (len(body), len(lines)) + '\n'.join(lines[:15])
        return 'TEXT/HTML: %d bytes\n' % len(body) + '\n'.join(l.strip()[:200] for l in lines[:25] if l.strip())
    except Exception as e: return 'sample failed: %s: %s' % (type(e).__name__, e)

def one(it, force):
    d = os.path.join('official', it['id']); os.makedirs(d, exist_ok=True); mp = os.path.join(d, 'meta.json'); old = {}
    try: old = json.load(open(mp, encoding='utf-8'))
    except Exception: pass
    if not force and old.get('fetched') and old.get('ok'):
        age = (NOW - datetime.datetime.strptime(old['fetched'], '%Y-%m-%dT%H:%M:%SZ')).days
        if age < int(it.get('cycle_days') or 30): print('%-24s fetched %d days ago, next after %d' % (it['id'], age, it['cycle_days'])); return
    meta = {'id': it['id'], 'country': it.get('country'), 'publisher': it.get('publisher'), 'what': it.get('what'), 'url': it['url'], 'fetched': NOW.strftime('%Y-%m-%dT%H:%M:%SZ'), 'ok': False, 'files': []}
    try:
        st, hd, body, final = get(it['url'], 3 * 2 ** 20 if it.get('probe') else 400 * 2 ** 20); meta.update(status=st, final_url=final)
        targets = [(it['url'], hd, body, final)]
        if it.get('follow'):      # the entry is a page: the files are what it links to
            page = body.decode('utf-8', 'replace'); links = sorted({urllib.parse.urljoin(final, h) for h in re.findall(r'href=["\']([^"\']+)["\']', page) if re.search(it['follow'], h)})[:12]
            meta['links_found'] = links; targets = []
            for u in links:
                try: s2, h2, b2, f2 = get(u); targets.append((u, h2, b2, f2))
                except Exception as e: meta.setdefault('errors', []).append('%s: %s: %s' % (u, type(e).__name__, str(e)[:120]))
            if not links: open(os.path.join(d, 'sample.txt'), 'w', encoding='utf-8').write('no link on the page matches %s\n' % it['follow'] + sample(body, 'page.html', hd.get('Content-Type')))
        if it.get('api_latest'):      # the entry is a data.gouv.fr dataset (API): the newest resources whose title or address matches, `take` of them
            res = [x for x in json.loads(body.decode('utf-8', 'replace')).get('resources') or [] if re.search(it['api_latest'], '%s %s' % (x.get('title') or '', x.get('url') or ''))]
            res.sort(key=lambda x: str(x.get('last_modified') or x.get('created_at') or ''), reverse=True); res = res[:int(it.get('take') or 1)]
            meta['resources'] = [{'title': x.get('title'), 'url': x.get('url'), 'last_modified': x.get('last_modified'), 'filesize': x.get('filesize')} for x in res]; targets = []
            was_res = {x.get('url') for x in old.get('resources') or []}
            if res and not force and old.get('ok') and {x.get('url') for x in res} <= was_res:      # the same edition as last time: nothing to download again
                meta['files'] = old.get('files') or []; meta['ok'] = True; meta['changed'] = []; meta['new'] = []; meta['same_edition'] = True
                json.dump(meta, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print('%-24s same edition as last time (%s)' % (it['id'], (res[0].get('title') or '')[:60])); return
            for x in res:
                try: s2, h2, b2, f2 = get(x['url'], 1500 * 2 ** 20); targets.append((x['url'], h2, b2, f2))
                except Exception as e: meta.setdefault('errors', []).append('%s: %s: %s' % (x.get('url'), type(e).__name__, str(e)[:120]))
        smp = []
        for u, h, b, f in targets:
            name = re.sub(r'[^A-Za-z0-9._-]', '_', (re.search(r'filename="?([^";]+)', h.get('Content-Disposition') or '') or [None, os.path.basename(urllib.parse.urlparse(f).path) or 'file'])[1])[:80]
            sha = hashlib.sha256(b).hexdigest(); meta['files'].append({'url': u, 'name': name, 'bytes': len(b), 'sha256': sha, 'last_modified': h.get('Last-Modified'), 'content_type': h.get('Content-Type')})
            smp.append('=== %s (%d bytes)\n%s' % (name, len(b), sample(b, name, h.get('Content-Type'))))
            if not it.get('probe'):
                os.makedirs('raw', exist_ok=True); open(os.path.join('raw', '%s__%s' % (it['id'], name)), 'wb').write(b)
        if smp: open(os.path.join(d, 'sample.txt'), 'w', encoding='utf-8').write('\n\n'.join(smp)[:60000] + '\n')
        meta['ok'] = bool(meta['files']); was = {f.get('name'): f.get('sha256') for f in old.get('files') or []}
        meta['changed'] = [f['name'] for f in meta['files'] if was.get(f['name']) not in (None, f['sha256'])]; meta['new'] = [f['name'] for f in meta['files'] if f['name'] not in was]
    except Exception as e:
        meta['error'] = '%s: %s' % (type(e).__name__, str(e)[:200])
        if old.get('files'): meta['files'] = old['files']; meta['kept_from'] = old.get('fetched')      # a failed fetch never erases what the last good one found
    json.dump(meta, open(mp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('%-24s %s  %s' % (it['id'], 'ok' if meta['ok'] else 'FAILED', '; '.join('%s %d bytes' % (f['name'], f['bytes']) for f in meta['files'][:3]) or meta.get('error', '')))

if __name__ == '__main__':
    a = sys.argv[1:]; only = a[a.index('--only') + 1] if '--only' in a else None
    items = json.load(open('official/manifest.json', encoding='utf-8'))['items']; rows = []
    for it in items:
        if only and it['id'] != only: continue
        one(it, '--force' in a)
    for it in items:
        try: m = json.load(open(os.path.join('official', it['id'], 'meta.json'), encoding='utf-8'))
        except Exception: continue
        f = (m.get('files') or [{}])[0]; rows.append('| `%s` | %s | %s | %s | %s | %s |' % (it['id'], it.get('country', ''), it.get('what', ''), 'ok' if m.get('ok') else ('failed: ' + m.get('error', '')[:60]), m.get('fetched', '')[:10], f.get('last_modified') or ''))
    open('official/README.md', 'w', encoding='utf-8').write('# Official files fetched for Band Atlas\n\nFetched by `.github/workflows/fetch-official.yml` from the addresses in `manifest.json`. Raw files: release `official-data`.\n\n| id | country | what | last result | fetched | file date |\n|---|---|---|---|---|---|\n' + '\n'.join(rows) + '\n')
