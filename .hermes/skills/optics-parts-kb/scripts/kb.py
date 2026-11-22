#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""OpticsResearch KB fast query & combination tool.

Usage:
  kb.py rebuild                                   # rebuild cache (auto when stale)
  kb.py search <text> [--cat 카메라|렌즈|조명]      # full-text over cached rows
  kb.py cam  [col=value ...]                      # filter camera rows
      e.g. kb.py cam mp=5 iface=GIGE mono
  kb.py lens [col=value ...] [--wd 110] [--ic 11] # filter lens rows
      e.g. kb.py lens macro mount=C --wd 110 --ic-from-cam "HX-F251M-150"
  kb.py combo --cam <모델명|MP예:5mp> --wd 110 [--mount C] [--type macro|tele|cctv|zoom|any]
      -> lenses compatible with camera: mount + image circle >= sensor diag + WD covers
  kb.py light [col=value ...]

Columns (normalized): cam: model maker mp res psize sensor mono color fps khz iface mount ic src
                      lens: model maker type fl mag wd_min wd_max fno ic ic_mm mount dof src
Key=value matching is case-insensitive substring/regex on the RAW cell; flags like
--wd parse ranges. --ic accepts mm number or format (2/3, 1/1.8, 4/3, 1").
Cache: <repo>/.kb-cache/index.json (+ generated meta). Rebuilt when any .md is newer.
"""
import sys, os, re, json, math, argparse, time

def repo_root():
    for c in (r'C:\Github\OpticsResearch', os.environ.get('OPTICS_KB_REPO', '')):
        if c and os.path.isdir(os.path.join(c, '카메라', '_인덱스')):
            return c
    sys.exit('repo not found (set OPTICS_KB_REPO)')

REPO = repo_root()
CACHE = os.path.join(REPO, '.kb-cache', 'index.json')
CATS = ['카메라', '렌즈', '조명']

FMT_MM = {'1/4': 4.0, '1/3.6': 4.96, '1/3': 6.0, '1/2.7': 6.6, '1/2.5': 7.18,
          '1/2.3': 7.7, '1/2': 8.0, '1/1.8': 8.93, '1/1.7': 9.5, '1/1.6': 10.0,
          '2/3': 11.0, '1': 16.0, '1.1': 17.6, '1.2': 18.9, '4/3': 21.6,
          'aps-c': 28.4, 'aps-c/dx': 23.6}

def norm_ic(raw):
    """return image-circle diameter in mm or None."""
    if not raw: return None
    t = raw.replace('`', '').strip()
    m = re.search(r'\((\d+(?:/\d+)?(?:\.\d+)?)\)?["”]?\s*$', t)
    cand = t
    if m: cand = m.group(1)
    cand = cand.rstrip('"”').strip()
    mm = re.match(r'^(\d+(?:\.\d+)?)\s*mm$', cand, re.I)
    if mm: return float(mm.group(1))
    key = cand.lower()
    if key in FMT_MM: return FMT_MM[key]
    plain = re.match(r'^(\d+(?:\.\d+)?)$', cand)
    if plain:
        v = float(plain.group(1))
        return v if v >= 3 else None  # bare small number is not mm
    return None

def num(s):
    m = re.match(r'^\s*(-?[\d.,]+)\s*$', str(s).replace('`', ''))
    return float(m.group(1).replace(',', '')) if m else None

def wd_range(s):
    s = str(s).replace('`', '').strip()
    inf = ('∞', 'inf')
    if '~' in s:
        a, b = s.split('~', 1)
        lo = 0.0 if any(x in a for x in inf) else num(a)
        hi = 1e9 if any(x in b for x in inf) else num(b)
        if lo is None or hi is None: return None
        return (lo, hi)
    v = num(s)
    return (v, v) if v is not None else None

# ---------- parsing ----------

def split_row(line):
    cells = [c.strip() for c in line.strip().strip('|').split('|')]
    return cells

def header_map(hdr_cells):
    """map normalized key -> col index"""
    m = {}
    for i, h in enumerate(hdr_cells):
        hl = re.sub(r'\s+', '', h).lower()
        def has(*alts): return any(a in hl for a in alts)
        if has('모델명', 'model'): k = 'model'
        elif has('제조사'): k = 'maker'
        elif has('해상도(mp)') or hl in ('해상도_m', 'mp'): k = 'mp'
        elif has('해상도(픽셀)', '해상도_'): k = 'res'
        elif has('픽셀사이즈'): k = 'psize'
        elif hl == '센서': k = 'sensor'
        elif has('센서타입'): k = 'stype'
        elif has('모노/컬러', '모노컬러'): k = 'mono_color'
        elif has('프레임레이트'): k = 'fps'
        elif has('라인레이트'): k = 'khz'
        elif has('인터페이스'): k = 'iface'
        elif has('마운트'): k = 'mount'
        elif has('이미지서클', '서클'): k = 'ic'
        elif has('센서포맷'): k = 'sfmt'
        elif has('센서사이즈'): k = 'ssz'
        elif has('렌즈타입'): k = 'lens_type'
        elif has('카테고리', 'category'): k = 'category'
        elif has('type'): k = 'type'
        elif has('focal'): k = 'fl'
        elif has('배율') or hl == 'mag': k = 'mag'
        elif 'wdmin' in hl: k = 'wd_min'
        elif 'wdmax' in hl: k = 'wd_max'
        elif has('wd'): k = 'wd'
        elif has('f/#', 'f#', 'fno'): k = 'fno'
        elif has('na'): k = 'na'
        elif has('dof'): k = 'dof'
        elif has('o/i'): k = 'oi'
        elif has('lifetime'): k = 'life'
        elif has('power'): k = 'power'
        elif has('channels'): k = 'channels'
        elif has('coloroption'): k = 'color'
        elif has('voltage'): k = 'volt'
        elif has('illuminance'): k = 'illuminance'
        elif has('avg', 'luminance', 'luminous'): k = 'light'
        else: k = hl
        m[k] = i
    return m

def parse_index(path, cat):
    out = []
    txt = open(path, encoding='utf-8').read().split('\n')
    hdr_i = next((i for i, l in enumerate(txt) if l.startswith('| 모델명')), None)
    if hdr_i is None: return out
    hm = header_map(split_row(txt[hdr_i]))
    src = os.path.basename(path)
    for l in txt[hdr_i + 2:]:
        if not l.startswith('|'):
            if l.startswith('#'): continue
            else: continue
        cells = split_row(l)
        if len(cells) < 3 or cells == [''] * len(cells): continue
        row = {}
        for k, i in hm.items():
            if i < len(cells): row[k] = cells[i]
        row['_cat'] = cat
        row['_src'] = src
        # clean model name (strip markdown link)
        mm = re.match(r'\[([^\]]+)\]\(([^)]+)\)', row.get('model', ''))
        if mm:
            row['doc'] = mm.group(2)
            row['model'] = mm.group(1)
        else:
            row['doc'] = None
        out.append(row)
    return out

def cam_diag(row):
    """sensor diagonal mm computed from res x psize."""
    res = re.findall(r'(\d+)', (row.get('res') or '').replace(',', ''))
    if len(res) < 2: return None
    ps = re.findall(r'([\d.]+)', row.get('psize') or '')
    if not ps: return None
    p = float(ps[0])
    return math.hypot(int(res[0]) * p / 1000, int(res[1]) * p / 1000)

def build_cache():
    data = {'built': time.strftime('%Y-%m-%d %H:%M:%S'), 'rows': []}
    for cat in CATS:
        d = os.path.join(REPO, cat, '_인덱스')
        if not os.path.isdir(d): continue
        for f in sorted(os.listdir(d)):
            if f.endswith('.md'):
                data['rows'] += parse_index(os.path.join(d, f), cat)
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    json.dump(data, open(CACHE, 'w', encoding='utf-8'), ensure_ascii=False)
    return data

def cache_fresh(data):
    b = os.path.getmtime(CACHE)
    for cat in CATS:
        d = os.path.join(REPO, cat, '_인덱스')
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith('.md') and os.path.getmtime(os.path.join(d, f)) > b:
                    return False
    try:
        for root, dirs, files in os.walk(os.path.join(REPO, '카메라')):
            dirs[:] = [x for x in dirs if x != '_인덱스']
            for f in files:
                if f == 'README.md' and os.path.getmtime(os.path.join(root, f)) > b:
                    return False
    except Exception:
        pass
    return True

def load():
    if os.path.exists(CACHE):
        try:
            data = json.load(open(CACHE, encoding='utf-8'))
            if cache_fresh(data):
                return data
        except Exception:
            pass
    return build_cache()

# ---------- filtering ----------

def match(row, conds):
    for key, pat in conds:
        v = row.get(key)
        if v is None: return False
        vv = str(v)
        if not re.search(pat, vv, re.I): return False
    return True

def parse_cond(a):
    if '=' in a:
        k, v = a.split('=', 1)
        alias = {'해상도': 'mp', '마운트': 'mount', '인터페이스': 'iface', '제조사': 'maker',
                 '배율': 'mag', '조리개': 'fno', '렌즈타입': 'lens_type', '타입': 'type'}
        return alias.get(k, k), v
    return None, a  # bare token: text match handled by caller

COND_KEYS = set('model maker mp res psize sensor stype mono_color color fps khz iface mount ic '
                'sfmt ssz lens_type category type fl mag wd wd_min wd_max fno na dof oi life power '
                'channels volt illuminance light doc src _src'.split())

def generic(row, tokens):
    for t in tokens:
        blob = ' '.join(str(v) for v in row.values() if v)
        if not re.search(re.escape(t), blob, re.I): return False
    return True

def fmt_row(row, cols):
    return '| ' + ' | '.join(str(row.get(c, '') or '—')[:36] for c in cols) + ' |'

CAM_COLS = ['model', 'maker', 'mp', 'res', 'psize', 'mono_color', 'fps', 'khz', 'iface', 'mount', 'ic', '_src']
LENS_COLS = ['model', 'maker', 'lens_type', 'fl', 'mag', 'wd', 'wd_min', 'wd_max', 'fno', 'ic', 'mount', 'dof', '_src']
LIGHT_COLS = ['model', 'maker', 'type', 'category', 'power', 'channels', 'color', 'light', 'life', '_src']

def lens_type_pat(row, want):
    lt = (row.get('lens_type') or '') + ' ' + (row.get('_src') or '')
    pats = {'macro': r'매크로|macro', 'tele': r'텔레센트릭|telecentric',
            'cctv': r'cctv', 'zoom': r'zoom|변배', 'line': r'라인스캔|line'}
    return re.search(pats[want], lt, re.I) if want in pats else True

# ---------- commands ----------

def cmd_cam(args):
    rows = [r for r in load()['rows'] if r['_cat'] == '카메라']
    kv = [(a.split('=', 1)[0], a.split('=', 1)[1]) for a in args.rest if '=' in a]
    tk = [a for a in args.rest if '=' not in a]
    out = [r for r in rows if match(r, kv) and generic(r, tk)]
    if args.mp:
        out = [r for r in out if r.get('mp') and abs((num(r['mp']) or -1) - float(args.mp.rstrip('mp'))) < 0.3]
    print(f'{len(out)} cameras')
    for r in out[: args.top]:
        print(fmt_row(r, CAM_COLS))

def cmd_lens(args):
    rows = [r for r in load()['rows'] if r['_cat'] == '렌즈']
    kv = [(a.split('=', 1)[0], a.split('=', 1)[1]) for a in args.rest if '=' in a]
    tk = [a for a in args.rest if '=' not in a]
    out = []
    for r in rows:
        if not match(r, kv) or not generic(r, tk): continue
        if args.type and not lens_type_pat(r, args.type): continue
        if args.mount and (r.get('mount') or '').strip().upper() != args.mount.upper(): continue
        w = wd_range(r.get('wd') or '') or \
            (None if not (r.get('wd_min') or r.get('wd_max')) else
             ((num(r.get('wd_min')) or 0), (num(r.get('wd_max')) or 1e9)))
        if args.wd:
            if not w or not (w[0] - 0.5 <= args.wd <= w[1] + 0.5): continue
        if args.ic:
            icm = norm_ic(r.get('ic'))
            if icm is None or icm < args.ic - 0.05: continue
        r['_w'] = w
        out.append(r)
    print(f'{len(out)} lenses')
    for r in out[: args.top]:
        print(fmt_row(r, LENS_COLS))

def resolve_cam(rows, name):
    name_l = name.lower().rstrip(' ')
    exact = [r for r in rows if r.get('model', '').lower() == name_l]
    if exact: return exact[0]
    m = re.match(r'^(\d+(?:\.\d+)?)\s*(mp|메가|megapixels?)?$', name_l)
    if m and m.group(2):
        cand = [r for r in rows if r.get('mp') and abs((num(r['mp']) or -1) - float(m.group(1))) < 0.3]
        if cand: return cand[0]
    part = [r for r in rows if name_l in r.get('model', '').lower()]
    if part: return part[0]
    return None

def cmd_combo(args):
    rows = load()['rows']
    cams = [r for r in rows if r['_cat'] == '카메라']
    cam = resolve_cam(cams, args.cam)
    if not cam: sys.exit(f'camera not found: {args.cam}')
    d = cam_diag(cam)
    need_ic = args.ic if args.ic else (d + 0.0 if d else 11.0)
    mount = (args.mount or cam.get('mount') or 'C').strip().upper()
    lens_rows = [r for r in rows if r['_cat'] == '렌즈']
    ok = []
    for r in lens_rows:
        mnt = (r.get('mount') or '').strip().upper()
        if mnt != mount and mount not in mnt.replace(' ', ''): continue
        if args.type and not lens_type_pat(r, args.type): continue
        icm = norm_ic(r.get('ic'))
        if icm is None or icm < need_ic - 0.05: continue
        w = wd_range(r.get('wd') or '')
        if w is None and (r.get('wd_min') or r.get('wd_max')):
            w = ((num(r.get('wd_min')) or 0), (num(r.get('wd_max')) or 1e9))
        if args.wd:
            if not w or not (w[0] - 0.5 <= args.wd <= w[1] + 0.5): continue
        r['_w'] = w; r['_icm'] = icm
        ok.append(r)
    print(f'# combo: cam={cam["model"]} ' + (f'sensor_diag={d:.2f}mm -> need IC>={need_ic:.2f}mm' if d else f'(IC>= assumed {need_ic})')
          + f' mount={mount}' + (f' WD={args.wd}mm' if args.wd else ''))
    print(f'{len(ok)} compatible lenses')
    for r in ok[: args.top]:
        print(fmt_row(r, LENS_COLS))

def cmd_search(args):
    rows = load()['rows']
    out = [r for r in rows if generic(r, args.tokens) and (not args.cat or r['_cat'] == args.cat)]
    print(f'{len(out)} rows')
    for r in out[: args.top]:
        cols = CAM_COLS if r['_cat'] == '카메라' else LENS_COLS if r['_cat'] == '렌즈' else LIGHT_COLS
        print(r['_cat'], fmt_row(r, cols))

def cmd_light(args):
    rows = [r for r in load()['rows'] if r['_cat'] == '조명']
    kv = [(a.split('=', 1)[0], a.split('=', 1)[1]) for a in args.rest if '=' in a]
    tk = [a for a in args.rest if '=' not in a]
    out = [r for r in rows if match(r, kv) and generic(r, tk)]
    print(f'{len(out)} lights')
    for r in out[: args.top]:
        print(fmt_row(r, LIGHT_COLS))

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('rebuild')
    def common(p):
        p.add_argument('--top', type=int, default=60)
        return p
    p = common(sp.add_parser('cam')); p.add_argument('--mp'); p.add_argument('rest', nargs='*')
    p = common(sp.add_parser('lens'))
    p.add_argument('--wd', type=float); p.add_argument('--ic', type=float)
    p.add_argument('--mount'); p.add_argument('--type', choices=['macro', 'tele', 'cctv', 'zoom', 'line'])
    p.add_argument('rest', nargs='*')
    p = common(sp.add_parser('combo'))
    p.add_argument('--cam', required=True); p.add_argument('--wd', type=float)
    p.add_argument('--ic', type=float); p.add_argument('--mount')
    p.add_argument('--type', choices=['macro', 'tele', 'cctv', 'zoom', 'line'])
    p = common(sp.add_parser('search')); p.add_argument('--cat'); p.add_argument('tokens', nargs='+')
    p = common(sp.add_parser('light')); p.add_argument('rest', nargs='*')
    a = ap.parse_args()
    if a.cmd == 'rebuild':
        d = build_cache()
        print(f'rebuilt: {len(d["rows"])} rows ({d["built"]})')
    else:
        {'cam': cmd_cam, 'lens': cmd_lens, 'combo': cmd_combo, 'search': cmd_search, 'light': cmd_light}[a.cmd](a)

if __name__ == '__main__':
    main()
