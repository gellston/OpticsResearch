---
유형: '루트 인덱스'
프로젝트: '광학정보모음집 — 광학계(카메라·렌즈·조명·조명컨트롤러) 부품 정보 정리'
총수집품수: 3670
상세문서수: 3670
수집일: '2026-11-20'
수록출처: 'fainstec.com · crevis.co.kr · vieworks.com · altsystem.co.kr · lfine.co.kr'
수용범위: '제조사·유통사 무관 — 새 출처는 대분류·필수 필드·문서 형식을 동일하게 유지해 추가'
---

# 광학정보모음집 — 카메라 · 렌즈 · 조명 · 조명컨트롤러

> **요약** | 머신비전 광학계 부품 **3670종** 수집 (fainstec 3215 + CREVIS 99 + Vieworks 183 + 알트시스템 115 + 엘파인 58) → 전 모델 **3670종**에 모델명 폴더 + README 상세 문서 보유

## 이 광학정보모음집에 대하여

- **범위**: 카메라 · 렌즈 · 조명(발광 소자) · 조명컨트롤러(광원·구동 장치) 네 대분류의 광학계 부품 사양과 조합·선정 기준을 모아 두는 **광학정보 모음집**입니다.
- **수록 출처**: 현재 **5개 출처**의 자료를 모아 두었습니다 — **화인스텍(fainstec)** · **크래비스(CREVIS)** · **뷰웍스(Vieworks)** · **알트시스템(Altsystem)** · **엘파인(Lfine)**. 출처별 상세는 하단 [현재 수록 출처](#현재-수록-출처-참고-기업)를 참조합니다.
- **다른 기업의 자료도 수용**: 특정 회사 전용이 아닙니다. 다른 제조사/공급처의 광학계 정보도 이 모음집에 **지속 추가**되며, 추가 시에도 대분류·필수 필드·문서 형식은 동일하게 유지합니다.
- **구조**: `대분류/모델명/README.md` — frontmatter(검색용 키워드) → 요약 → 핵심 사양 → 전체 사양 → 조합 참고 → 출처 순.
- **출처 표기**: 각 문서의 frontmatter `출처` URL과 본문의 링크가 원본 페이지를 가리킵니다. 도면·사양서 PDF 링크는 원본 그대로 유지합니다.

## 대분류

| 대분류 | 총 종수 | 상세 문서 | README |
| --- | ---: | ---: | --- |
| 카메라 | 1676 | 1676 | [카메라 README](카메라/README.md) |
| 렌즈 | 1727 | 1727 | [렌즈 README](렌즈/README.md) |
| 조명 | 168 | 168 | [조명 README](조명/README.md) |
| 조명컨트롤러 | 99 | 99 | [조명컨트롤러 README](조명컨트롤러/README.md) |

## 디렉토리 구조

```
OpticsResearch/
├── README.md                    # 이 문서 (루트 인덱스)
├── 광학계-계산-기준.md           # FOV · 배율 · 분해능 계산 규칙
├── 카메라/
│   ├── README.md                # 카메라 대분류 요약 + 선별 모델 표
│   ├── _인덱스/                 # 소분류별 전체 모델 색인
│   └── <모델명>/README.md       # 모델별 상세 (해상도 · 픽셀사이즈 필수 포함)
├── 렌즈/
│   ├── README.md                # 렌즈 대분류 요약 + 선별 모델 표
│   ├── _인덱스/
│   └── <모델명>/README.md       # 모델별 상세 (모델명 · WD · FOV · 배율 · Optical Resolution 필수 포함)
├── 조명/
│   ├── README.md                # 발광체 (Area/Line Light · Light Source)
│   ├── _인덱스/
│   └── <모델명>/README.md
└── 조명컨트롤러/
    ├── README.md                # 광원(Light Source) + 구동 컨트롤러 (출력(W) · 채널 · 구동방식)
    ├── _인덱스/
    └── <모델명>/README.md
```

## 필드 정의 (에이전트 검색 시 참고)

| 필드 | 의미 | 비고 |
| --- | --- | --- |
| 해상도 | 카메라 센서의 총 화소수 (MP) | `해상도(픽셀)` 열이 W x H 실해상도 |
| 픽셀 사이즈 | 센서 1픽셀의 물리 크기 (µm) | 일부 출처 사이트의 필드명은 `셀사이즈` |
| 배율 | 렌즈의 물체측 배율 (x) | 범위 표기는 WD 범위에 따른 것 |
| WD | Working Distance, 렌즈 전면~촬영 대상 거리 (mm) | CCTV 렌즈는 `MOD(min/max WD)`로 표기 |
| FOV | 카메라 + 렌즈 **조합** 시 산출되는 시야 | `FOV(mm) = 센서 사이즈(mm) ÷ 배율` — 렌즈 단독 값이 아니므로 상세 문서에 공식으로 표기 |
| Optical Resolution | **렌즈 자체**의 광학적 분해능 | 카메라 센서와 무관. 제조사에 표기가 있을 때만 값 기재, 없으면 공란(`null`) |
| NA | 렌즈의 개구수(Numerical Aperture) | NA가 있으면 이론 분해능 `0.61λ/NA`(λ=550nm)를 참고값으로 병기 |
| 정격출력 | 광원(Light Source) 자체의 소비 전력 | `조명컨트롤러/Light-Source` 전용. **단위는 출처 그대로** — LVS는 시리즈 내 모델별 W 범위, REVOX 라인 조명은 발광 길이 주문제작이라 `W/m`, REVOX 광섬유 광원은 `VA` |
| 최대지원출력 | 컨트롤러가 구동 가능한 최대 전력 | `조명컨트롤러/`의 Area·Line Controller 전용. 발광체의 정격출력 ≤ 이 값이면 조합 가능 (제조사 무관) |

## 상세 문서화 규칙

- 현재 수록된 **모든 모델(3314종)**이 `대분류/모델명/README.md` 상세 문서를 보유합니다. 인덱스의 모델명을 클릭하면 해당 문서로 이동합니다.
- 상세 문서 구성: frontmatter(검색용 키워드) → 요약 → 핵심 사양 → 전체 사양(원본 전체 필드) → 조합 참고 → 다운로드·출처 → 관련 문서.
- 모든 값은 출처 페이지에서 수집한 것이며, 없는 값은 추정하지 않고 `—`로 표기합니다.
- 상세 문서를 추가하거나 행을 수정하면 `제품수`·`상세문서수`를 함께 갱신하고 커밋 전 감사를 통과해야 합니다.

## 현재 수록 출처 (참고 기업)

> 아래는 **현재** 이 모음집에 들어 있는 데이터의 원본(참고 기업)입니다. 추후 다른 회사의 광학계 정보가 추가되면 출처 목록도 함께 갱신합니다.

- **화인스텍(FAINSTEC)** — https://www.fainstec.com (2026-11-20 추가 · **가장 큰 비중 — 카메라·렌즈·조명 전반**)
  - 카메라: `https://www.fainstec.com/product/product.php?ptype=list&catcode=10111000` (Area / Line 10111100 / Smart 10111200 / CIS 10111300)
  - 렌즈: `https://www.fainstec.com/product/product.php?ptype=list&catcode=10121000` (Telecentric 10121100 / CCTV 10121200 / Zoom 10121300 / Focus Tunable 10121400 / Microscope 10121500 / Accessory 10121600)
  - 조명: `https://www.fainstec.com/product/product.php?ptype=list&catcode=10141000` (Line 10141100 / Light Source 10141200 / Area Ctrl 10141300 / Line Ctrl 10141400)
  - `prdcode` / `catcode`는 화인스텍 사이트의 제품·카테고리 코드입니다. 다른 출처는 자체 식별자를 사용합니다.
  - 단종 제품은 포함하지 않았습니다 (사이트 기본 필터 기준).
- **크래비스(CREVIS)** — https://www.crevis.co.kr (2026-11-20 추가)
  - 비전카메라 카테고리: `https://www.crevis.co.kr/Product/productListD2?depth1=2` (스탠다드 `depth2=10` / 편광 `11` / SWIR `19` / 3CMOS `20`)
  - 상세 URL: `https://www.crevis.co.kr/Product/productView?idx=<idx>` — `idx`는 crevis.co.kr의 제품 코드.
  - 2026 카탈로그 PDF: `https://files.ioguide2-autoupdate.com/` (gige / usb3.0 / cameralink / coaXPress / linescan / Special 카탈로그).
  - 현재 수록 99종: Area Scan 84 · Line Scan 4 · SWIR 6 · Polarization 4 · 3CMOS 1.
- **LVS (주)엘브이에스** — https://www.lvs.co.kr (2026-11-23 추가 · **정격출력(W) 수집용**)
  - 조명 시리즈: `https://www.lvs.co.kr/products/db-db2-dbs-series` 등 — `seriesData`의 `Color Option / Power Consumption(W)` 컬럼에서 모델별 소비전력(W) 수집
  - 컨트롤러 사양서 PDF: `http://lvs.webmaker21.kr/pdf/LVS-EN-0412.pdf` 등 — 사양 표의 `Power` 값 (EN/ES/ET/DN 계열)
  - 주의: LVS 사양서 PDF는 대부분 **이미지 스캔본**이라 `pdftotext`로 텍스트가 안 나옵니다. HTML 페이지의 `seriesData`를 우선합니다.
- **REVOX 레보ックス** — https://www.revox.jp (2026-11-23 추가 · **정격출력(W) 수집용**)
  - 라인 조명: `https://www.revox.jp/products/led/spx-ta200/` 등 — `消費電力（最大照度時）`. 발광 길이가 주문제작이라 **`W/m` 단위**입니다.
  - 광섬유 광원: `https://www.revox.jp/products/optical-fiber/` — `消費電力（typ.）` (`W` 또는 `VA`)
  - 전용 전원: 각 제품 페이지의 `専用電源 技術仕様` (`最大300W` / `最大600W` 등)
- **뷰웍스 (Vieworks)** — https://vision.vieworks.com (2026-11-23 추가 · **카메라**)
  - Area Scan: `https://vision.vieworks.com/kr/camera/area_scan` (VC·VN·VNP·VP·VQ·VX·VZ 시리즈)
  - Line Scan: `https://vision.vieworks.com/kr/camera/line_scan` (VL 시리즈)
  - TDI Line Scan: `https://vision.vieworks.com/kr/camera/tdi_line_scan` (VT·VTC 시리즈)
  - 시리즈 페이지의 `data-role="opTable"` 블록에서 모델 표를 수집합니다.
- **알트시스템 (Altsystem)** — https://www.altsystem.co.kr (2026-11-23 추가 · **조명 · 조명컨트롤러**)
  - sitemap.xml에 시리즈 페이지 200여 개가 있어 그 목록으로 수집합니다.
  - 조명 사양표: `Model | Color | Dimension | Power Consumption(W) | Input Voltage(DC V)`
  - 컨트롤러 사양표: `Model | Dimension | Output Channel(CH) | Power Consumption(W)`
- **엘파인 (Lfine)** — https://lfine.co.kr (2026-11-23 추가 · **조명 · 조명컨트롤러**)
  - 조명 8종류(직접조사·무영·투과·동축낙사·특수·라인스캔·스폿·커스텀) + 제어기(정전압·정전류·스트로브)
  - 사이트가 SPA라 상세 스펙이 페이지에 노출되지 않아 **모델명·시리즈·채널수만** 수록하고 나머지는 `—`로 둡니다.
- (이후 추가될 출처는 이 목록에 추가합니다)

## 다른 회사 정보 추가 시 규칙

1. **같은 폴더 구조 유지**: `카메라/`, `렌즈/`, `조명/`, `조명컨트롤러/` 아래에 `모델명/README.md`를 만듭니다. 출처가 달라도 대분류·필수 필드는 동일합니다.
2. **frontmatter 필수 키**: `유형`, `대분류`, `소분류`, `모델명`, `제조사`, `출처`(원본 URL), `수집일`. 출처 사이트 고유 식별자가 있으면 `prdcode` 등으로 함께 남깁니다.
3. **필수 사양 열**: 카메라 = 모델명·픽셀사이즈·해상도 / 렌즈 = 모델명·WD·FOV·배율·Optical Resolution / 조명 = 모델명·유형 / 조명컨트롤러 = 모델명·유형·채널수.
4. **값이 없는 항목은 공란**:임의로 채우지 않습니다. FOV는 공식으로, Optical Resolution은 제조사 표기값이 있을 때만 기재합니다.
5. **출처 목록 갱신**: 위 [현재 수록 출처 (참고 기업)](#현재-수록-출처-참고-기업)에 새 출처를 추가하고, 본문의 회사 관련 서술은 그 출처에 한정해 기술합니다.
6. **원본 링크 유지**: 도면·사양서 PDF 등 다운로드 링크는 원본 URL 그대로 보존합니다.

## 관련 문서

- [광학계 계산 기준](광학계-계산-기준.md)
- [카메라 README](카메라/README.md)
- [렌즈 README](렌즈/README.md)
- [조명 README](조명/README.md)
- [조명컨트롤러 README](조명컨트롤러/README.md)
