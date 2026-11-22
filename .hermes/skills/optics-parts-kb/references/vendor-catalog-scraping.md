# Vendor catalog collection recipe

Sequence that worked for a Korean machine-vision vendor site; adapt selectors per vendor, keep the shape.

## 1. Discover the full model list (browser, not curl, for listing pages)

Listing pages are usually JS-driven category trees. Use `browser_exec`:

- Start at the site root, collect category URLs from `document.querySelectorAll('a')` (filter hrefs containing the product-list path).
- For each category, walk subcategory links (`depth`/`cat` query params) and paginate explicitly — many Korean vendor lists default to a small page size and accept `page=N&page_size=60`; loop until a page returns zero new items.
- Extract model rows as `{href, title}` where href matches the product-view pattern (e.g. `productView?idx=<id>`).
- Dedupe by href into a JSON file in the scratch dir; the id in the URL is the source identifier that goes into frontmatter (`idx`, `prdcode`, etc.).

## 2. Bulk-download product pages (terminal, parallel)

```bash
cat urls.txt | xargs -P 8 -I{} sh -c \
  'i=$(echo "{}" | grep -o "idx=[0-9]*" | cut -d= -f2); \
   curl -sS -L --max-time 45 -A "Mozilla/5.0" "{}" -o "pages/$i.html"'
```

The user agent matters (bare curl often gets blocked); `-P 8` keeps it fast without tripping rate limits.

## 3. Parse specs from HTML tables first

Python regex over `<table>` → `<tr>` → `<t[dh]>`, strip tags, unescape entities, first cell = key, second = value (the vendor's `TECHNICAL DATA` table). Fallback when no table exists: strip tags to text and segment by a known key vocabulary (find each key's offset, value = text until the next key) — but validate the result, because column drift puts values under the wrong keys.

## 4. Catalog PDF as cross-check / for models missing from the site

```bash
curl -sS -L -A "Mozilla/5.0" "<catalog.pdf>" -o cat.pdf
pdftotext -layout cat.pdf cat.txt   # pdftotext available on this host (/ucrt64/bin)
```

Use the PDF for models absent from the website and to cross-check resolution/fps/sensor. Never trust a PDF-derived key→value pair without a semantic sanity check (see Pitfalls in SKILL.md).

## 5. Normalize to one JSON

Fields per model: `model, display, folder, subcat, color, sensor_short, stype, mount_n, res_n, mp_n, fps_n | lr_n, psize_n, ssize_n, iface, idx, url, spec{}`.

- `folder`: sanitize the display name to `[A-Za-z0-9._-]` — parentheses/spaces break markdown links (e.g. `HX-A530SW (AirJet)` → `HX-A530SW-AirJet`).
- `color`: model-name suffix first (`M`/`R`/`P` → MONO, `K`/`L` → COLOR), then spec table, then list title last.
- `iface`: derive from category path, cross-check against the `Interface` field in the spec table.
- Resolution buckets for 선별 규칙: `mp = W*H/1e6`; Line Scan uses horizontal pixels (2048 → 2 MP) and `라인레이트` instead of fps.

## 6. Cross-validation before generating

Diff spec-table values against list-title values for resolution / fps / color on every model; investigate every mismatch (label drift, marketing-title typos) and resolve it in the JSON before any markdown is generated. The JSON is the single source: index file, detail READMEs, and all counts are derived from it.
