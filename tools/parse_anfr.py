#!/usr/bin/env python3
"""Summarise ANFR's national file of radio installations over 5 watts (the ZIPs fetched as `fr-anfr-5w`) for Band Atlas (standard library only).
From the tables inside (stations, transmitters with their system, operators) it counts, for every mobile operator and every system such as
"LTE 800" or "5G NR 3500", the stations that carry it, and writes official/fr-anfr-5w/summary.json. The count shows which bands an operator really
has on air in France, 4G and 5G separately, from the regulator's own register.
The column names are found by what they contain, so a renamed or reordered column does not break the reading.
usage: parse_anfr.py [raw_dir]      (default ./raw; reads raw/fr-anfr-5w__*.zip)"""
import collections, csv, glob, io, json, os, re, sys, zipfile, datetime

def tables(paths):
    """→ {kind: (zip path, member)} for the newest member of each kind"""
    out = {}
    for p in paths:
        try: z = zipfile.ZipFile(p)
        except zipfile.BadZipFile: continue
        for i in z.infolist():
            n = i.filename.upper()
            for kind, rx in (('emetteur', r'EMETTEUR'), ('station', r'SUP_STATION|(^|/)STATION'), ('exploitant', r'EXPLOITANT'), ('support', r'SUP_SUPPORT')):
                if re.search(rx, n) and n.endswith(('.TXT', '.CSV')) and (kind not in out or i.file_size > out[kind][2]): out[kind] = (p, i.filename, i.file_size)
    return out

def rows(zp, member):
    z = zipfile.ZipFile(zp); f = io.TextIOWrapper(z.open(member), encoding='latin-1', newline='')
    head = f.readline(); sep = ';' if head.count(';') >= head.count(',') else ','
    cols = [c.strip().strip('"').upper() for c in head.rstrip('\r\n').split(sep)]
    for r in csv.reader(f, delimiter=sep): yield cols, r

def col(cols, *pats):
    for pat in pats:
        for i, c in enumerate(cols):
            if re.search(pat, c): return i
    return None

def main(raw):
    T = tables(sorted(glob.glob(os.path.join(raw, 'fr-anfr-5w__*.zip'))))
    out = {'made': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'), 'tables': {k: {'file': os.path.basename(v[0]), 'member': v[1], 'bytes': v[2]} for k, v in T.items()}}
    dest = os.path.join('official', 'fr-anfr-5w'); os.makedirs(dest, exist_ok=True)
    if not all(k in T for k in ('emetteur', 'station', 'exploitant')):
        out['error'] = 'tables not found: ' + ', '.join(k for k in ('emetteur', 'station', 'exploitant') if k not in T)
        json.dump(out, open(os.path.join(dest, 'summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1); print(out['error']); return 1
    names = {}; heads = {}
    for cols, r in rows(*T['exploitant'][:2]):
        heads['exploitant'] = cols; a, b = col(cols, r'ADM_ID'), col(cols, r'ADM_LB', r'NOM')
        if a is None or b is None: break
        if len(r) > max(a, b): names[r[a].strip()] = r[b].strip()
    sta = {}
    for cols, r in rows(*T['station'][:2]):
        heads['station'] = cols; a, b = col(cols, r'STA_NM_ANFR'), col(cols, r'ADM_ID')
        if a is None or b is None: break
        if len(r) > max(a, b): sta[r[a].strip()] = r[b].strip()
    seen = collections.defaultdict(set); n = 0
    for cols, r in rows(*T['emetteur'][:2]):
        heads['emetteur'] = cols; a, b = col(cols, r'STA_NM_ANFR'), col(cols, r'SYSTEME')
        if a is None or b is None: break
        if len(r) <= max(a, b): continue
        s = r[b].strip(); n += 1
        if not re.match(r'(5G NR|LTE|UMTS|GSM)\b', s): continue
        seen[(sta.get(r[a].strip(), '?'), s)].add(r[a].strip())
    by = collections.defaultdict(dict)
    for (adm, s), st in seen.items(): by[names.get(adm, adm)][s] = len(st)
    big = {k: v for k, v in by.items() if sum(v.values()) >= 500}      # the mobile operators; small holders of a few sites are counted but not listed
    out.update(columns=heads, transmitters_read=n, operators={k: dict(sorted(v.items())) for k, v in sorted(big.items(), key=lambda kv: -sum(kv[1].values()))},
               other_holders=len(by) - len(big), note='stations (distinct STA_NM_ANFR) per operator and system; a system with 100 stations or more is on air nationally')
    json.dump(out, open(os.path.join(dest, 'summary.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for k, v in out['operators'].items(): print('%-40s %s' % (k[:40], ', '.join('%s %d' % kv for kv in v.items() if kv[0].startswith('5G'))))
    return 0

if __name__ == '__main__': sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else 'raw'))
