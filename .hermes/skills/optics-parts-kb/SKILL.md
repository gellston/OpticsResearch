---
name: optics-parts-kb
description: Use when extending the OpticsResearch knowledge base.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Optics, Knowledge-Base, Markdown, Data-Collection, Git]
    related_skills: [obsidian]
---

# OpticsResearch knowledge base maintenance

## When to Use

Use when the user asks to check, extend, reorganize, or back up the OpticsResearch repo (`C:\Github\OpticsResearch`) — adding another vendor's camera/lens/light data, updating indexes or counts, editing README framing, or committing/pushing the knowledge base.

`C:\Github\OpticsResearch` — Korean-language markdown knowledge base (also an Obsidian vault) of machine-vision optics parts: 카메라 / 렌즈 / 조명. Remote: `github.com/gellston/OpticsResearch`, branch `main`. The repo lives at `C:\Github\OpticsResearch`, not under the home directory — go there directly instead of searching.

## Always-on rules

1. **Read before editing.** Open the root `README.md` and the target 대분류 `README.md` first. They define 필드 정의, 선별 규칙 (which models earn a detail doc), and the 다른 회사 추가 규칙: same folder structure `대분류/모델명/README.md`, mandatory frontmatter keys (`유형, 대분류, 소분류, 모델명, 제조사, 출처, 수집일`), required spec columns per category, and never inventing a missing value (leave `—`/blank).
2. **README voice (user preference).** Frame the repo as a 광학정보모음집: name the company the existing data was researched from, and state explicitly that other companies' data is also welcome and will be added. Never present it as single-vendor.
3. **Counts live in many places — update them all together.** Root frontmatter `총수집품수`/`상세문서수`, root 대분류 table, 대분류 README frontmatter + 소분류 구성 table + 상세 문서 보유 모델 table + 전체 제품 색인 section, and each `_인덱스/*.md` `제품수`/`상세문서수`. Verify by counting `대분류/*/README.md` folders on disk and checking every internal `[README](...)` link resolves **before** committing.
4. **Generate, don't hand-type.** Build one normalized JSON of the collected models, then write index files and detail READMEs programmatically from it. Never hand-type tables of dozens of rows, and never retype counts — derive them.
5. **One commit + push, at the very end.** Do all collection, generation, count updates, and verification first; only then a single `git add -A && git commit && git push origin main`. Confirm with `git rev-parse HEAD origin/main`.
6. **Existence questions get existence answers.** For "does the repo have X?" — confirm present/absent plus a short structure summary first; don't dump file contents.

## Workflow: add a new vendor's data

1. Read root README + target 대분류 README (current counts, 선별 규칙 for the new source).
2. Collect the catalog with `references/vendor-catalog-scraping.md`.
3. Normalize into one JSON: model, 소분류, resolution, pixel size, sensor, color, fps/line-rate, interface, mount, source URL/identifier.
4. Select detail-doc models by the repo's 선별 규칙 — Area Scan: one per resolution bucket (≤2 / 2-6 / 6-29 / ≥29 MP, tie-break highest fps then MONO); Line Scan: top by line rate; small 소분류 (SWIR, Polarization, 3CMOS, Smart, CIS): include wholesale.
5. Generate: a dedicated index at `카메라/_인덱스/<SOURCE>.md` plus each detail README. **A new source gets its own index file** — never append rows to an existing source's index, because columns like `prdcode`/URL patterns are source-specific. Detail README skeleton: frontmatter → `> 요약` line → 핵심 사양 table → 전체 사양 (원본 전체 필드) table → 시스템 조합 참고 (FOV = 센서 사이즈 ÷ 배율, 공간 분해능 = 픽셀 사이즈 ÷ 배율) → 다운로드·출처 → 관련 문서 (대분류 인덱스, 신규 소스 색인, `../../광학계-계산-기준.md`).
6. Wire the new source in: 대분류 README 소분류 table gains rows/links to the new index, 전체 제품 색인 section gains a subsection with that source's URL-identifier pattern, root README 현재 수록 출처 gains an entry, 출처사이트 becomes a comma list.
7. Verify (rule 3), then one commit + push (rule 5).

## Workflow: fast lookup & part combination (query side)

Never grep the 3,300+ index rows ad hoc — use `scripts/kb.py` (this skill), which parses every `대분류/_인덱스/*.md` once into a JSON cache (`<repo>/.kb-cache/index.json`, gitignored, auto-rebuilt when any index is newer) and answers in milliseconds:

- `kb.py search <text> [--cat 카메라|렌즈|조명]` — full-text across all normalized rows.
- `kb.py cam iface=GIGE mono --mp 5` · `kb.py lens tele --wd 110 --mount C` · `kb.py light power=...` — column filters (`col=value` regex, bare tokens = text match).
- `kb.py combo --cam <모델명|5mp> --wd 110 [--mount C] [--type macro|tele|cctv|zoom|line] [--ic <mm>]` — the compatibility answer: derives sensor diagonal from 해상도×픽셀사이즈, requires 렌즈 마운트 match + 이미지 서클 ≥ sensor diag + WD (min~max range or fixed) covering the target. `--cam` also accepts `5mp` (first match — always echo which camera was resolved).

Run: `python "C:\Github\OpticsResearch\.hermes\skills\optics-parts-kb\scripts\kb.py" <cmd>` — this skill lives inside the repo itself (`C:\Github\OpticsResearch\.hermes\skills\optics-parts-kb`), so KB data and skill move together; set `OPTICS_KB_REPO` only if the repo relocates. Prefer the `${HERMES_SKILL_DIR}` template var when it expands (e.g. `python "${HERMES_SKILL_DIR}/scripts/kb.py" <cmd>`).

Image-circle normalization handles `11.4(2/3)`, `22mm`, bare formats (`2/3`=11.0, `1/1.8`=8.93, `4/3`=21.6, `1`=16, `1.1`=17.6, `1.2`=18.9, `aps-c`=28.4). WD parsing accepts `a~b`, `∞`, fixed values.

Answering a combination question: run `combo`, then present the list grouped (e.g. by image circle headroom / series) with the resolved camera's sensor diagonal as the acceptance threshold, and mention when the user's exact WD is only achievable as `range covers 110` rather than a fixed 110 spec. A single run takes ~0.5s; verifying an edge (different camera format) = re-run with `--cam <that model>`.

## Pitfalls

- **Catalog PDFs misalign spec labels.** `pdftotext -layout` on two-column spec tables often shifts values one row, so a key gets the wrong value (e.g. `Interface => Off/Once/Continuous`). Treat PDF-derived specs as suspect: sanity-check every value against its key's meaning, and prefer the HTML product page table when both exist.
- **List titles are marketing strings.** When a product-page table and the list-page title disagree on color or fps, trust the model-name suffix (`M`/`R` → MONO, `K`/`L` → COLOR) and the spec table, not the title.
- **Line-ending warnings are noise.** Generating files with LF from a script makes git print `LF will be replaced by CRLF` warnings on Windows; content is unaffected — do not chase them.
- **Partial work must not be committed.** If a verification step fails, fix and re-verify; never push a state where frontmatter counts and on-disk folder counts disagree.