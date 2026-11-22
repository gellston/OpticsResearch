---
유형: '인덱스'
대분류: '조명컨트롤러'
제품수: 45
상세문서수: 45
소분류: 'Area Controller, Line Controller'
수집일: '2026-11-20'
출처: 'https://www.fainstec.com/product/product.php?ptype=list&catcode=10141000'
출처사이트: 'fainstec.com'
---

# 조명컨트롤러

> **요약** | 총 **45종** 수집 · 전 **45종** 상세 문서화 · 면/선 조명 구동용 컨트롤러 (LVS · REVOX)

## 이 대분류를 따로 둔 이유

조명 **발광체**(Area Light · Line Light · Light Source)와 조명을 **구동하는 장치**(Controller)는 서로 다른 부품입니다. 한 폴더에 섞어 두면 아래 문제가 생깁니다.

- **조합 선정이 안 됩니다.** 발광체의 정격출력(W)과 컨트롤러의 최대 지원출력(W)을 맞춰야 하는데, 같은 표에 섞이면 비교가 불가능합니다.
- **서로 다른 회사 제품도 매칭**해야 합니다. 발광체는 LVS, 컨트롤러는 REVOX인 조합이 흔하므로, 두 부품을 각각의 축으로 두고 출력(W) 기준으로 연결해야 합니다.

따라서 **발광체는 `조명/`, 구동 장치는 `조명컨트롤러/`** 로 분리합니다.

## 소분류 구성

| 소분류 | 종수 | 상세 문서 | 인덱스 |
| --- | ---: | ---: | --- |
| Area Controller | 19 | 19 | [전체 목록](_인덱스/Area-Controller.md) |
| Line Controller | 26 | 26 | [전체 목록](_인덱스/Line-Controller.md) |

## 상세 문서

아래 `전체 제품 색인`의 모든 모델명은 각 `모델명/README.md` 상세 문서로 연결됩니다. 상세 문서 구성: frontmatter(검색용 키워드) → 요약 → 핵심 사양 → 전체 사양(원본 전체 필드) → 조합 참고 → 출처. 없는 값은 `—`로 표기합니다.

## 조합 · 선정 시 참고

- **호환 조건**: 컨트롤러의 `최대 지원 출력(W)` ≥ 발광체의 `정격 출력(W)`.
- **채널 수**: 발광체 개수와 컨트롤러 채널 수가 맞아야 합니다. 다채널 컨트롤러는 한 채널에 여러 발광체를 물릴 수 있습니다.
- **구동 방식**: 스트로브(strobe) / PWM / 정전압(constant voltage)이 발광체와 맞아야 합니다. 인덱스의 `Type` 열에서 확인합니다.
- **제조사 무관**: 발광체와 컨트롤러는 같은 회사일 필요 없습니다. 위 조건만 맞으면 조합 가능합니다.

## 전체 제품 색인

아래 인덱스 파일에는 현재 수집된 조명컨트롤러 전체 45종이 포함되어 있습니다. prdcode는 출처 사이트의 제품 코드이며, 상세 URL은 https://www.fainstec.com/product/product.php?ptype=view&prdcode=<prdcode>&page=1&catcode=<catcode> 형식입니다. (현재 출처: 화인스텍(FAINSTEC) · fainstec.com)

- **Area Controller** (19종) → [_인덱스/Area-Controller.md](_인덱스/Area-Controller.md)
- **Line Controller** (26종) → [_인덱스/Line-Controller.md](_인덱스/Line-Controller.md)

## 관련 문서

- [조명 (발광체)](../조명/README.md)
- [루트 README](../README.md)
- [광학계 계산 기준](../광학계-계산-기준.md)
