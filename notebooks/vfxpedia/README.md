# 오흥재 (vfxpedia) - 개인 작업 공간

**주제**: 교육 및 경제활동에 따른 금연 성공 상관관계 분석

---

## 📁 폴더 구조

```
vfxpedia/
├── README.md                                      # 이 파일
│
├── utils/                                         # 🔧 유틸리티 모듈
│   └── data_cleaning.py                           # 데이터 정제 + Feature Engineering
│       ├── clean_data_for_analysis()              # 데이터 정제 메인 함수
│       ├── add_economic_status_features()         # 경제활동 상태 Feature 생성
│       ├── get_economic_status_summary()          # 경제활동 상태별 요약 통계
│       └── print_economic_code_info()             # 변수 코드 정보 출력
│
├── docs/                                          # 📚 문서
│   ├── ECONOMIC_STATUS_GUIDE.md                   # ⭐ 비경제활동인구 처리 가이드
│   ├── USAGE_GUIDE.md                             # 전체 사용 가이드
│   ├── PDF_VERIFICATION_NEEDED.md                 # PDF 확인 필요 변수
│   └── CHS_Variable.pdf                           # 원본 변수 설명 PDF
│
├── output/                                        # 📊 분석 결과
│   ├── analy_data_cleaned.csv                     # 정제된 데이터
│   └── analysis_results_education_economy_20251007.csv
│
└── 📓 노트북 파일들 (작업 순서대로)
    ├── 01_data_overview.ipynb                     # 전체 데이터 파악
    ├── 02_diagnosis_data_quality.ipynb            # 데이터 품질 진단
    ├── 03_data_cleaning_strategy.ipynb            # 정제 전략 수립
    ├── 04_data_cleaning_final.ipynb               # 최종 데이터 정제
    └── 05_analysis_education_economy.ipynb        # 교육/경제 분석
```

---

## 🚀 작업 순서 (Workflow)

### 1단계: 전체 데이터 파악
**📓 `01_data_overview.ipynb`**
- 데이터 기본 정보 확인 (shape, 컬럼, 데이터 타입)
- 기술 통계량 파악
- 전체 데이터셋 이해

### 2단계: 데이터 품질 진단
**📓 `02_diagnosis_data_quality.ipynb`**
- 변수별 실제 코드값 확인
- 특수코드 분포 파악 (응답거부, 모름, 비해당)
- 정의되지 않은 코드 탐지
- 분석 가능 표본 확인

### 3단계: 정제 전략 수립
**📓 `03_data_cleaning_strategy.ipynb`**
- 특수코드 처리 전략 수립
- 응답거부/모름 제거 방침 결정
- 비경제활동인구(88) 유지 결정 ⭐
- Skip Logic 처리 방안 수립

### 4단계: 최종 데이터 정제
**📓 `04_data_cleaning_final.ipynb`**
- `utils/data_cleaning.py` 모듈 사용
- 특수코드 체계적 처리
- 결측값 제거
- **Feature Engineering 적용** 🆕
- `output/analy_data_cleaned.csv` 생성

```python
from utils.data_cleaning import clean_data_for_analysis, add_economic_status_features

# 데이터 정제
df_clean, report = clean_data_for_analysis('../../data/analy_data.csv')

# Feature 생성
df_clean = add_economic_status_features(df_clean)
```

### 5단계: 교육/경제 분석
**📓 `05_analysis_education_economy.ipynb`**
- 교육수준에 따른 금연 성공률 분석
- 경제활동 상태에 따른 금연 성공률 분석
- 직업분류별 금연 성공률 분석
- 종사상 지위별 금연 성공률 분석
- 혼인상태별 금연 성공률 분석
- 가설 검증 (Chi-square test 등)
- 시각화 및 결과 해석

---

## 📊 분석 변수

### ✅ 최종 선정 (5개)

| 변수명 | 변수 설명 | 비고 |
|--------|-----------|------|
| **sob_01z1** | 교육수준(최종학력) | 무학~대학원 |
| **soa_01z1** | 경제활동 여부 | 취업/실업/비경제활동 |
| **soa_06z2** | 직업분류 | 표준직업분류 대분류 + 비경제활동(88) ⭐ |
| **soa_07z1** | 종사상 지위 | 근로형태 + 비경제활동(8) ⭐ |
| **sod_02z3** | 혼인상태 | 미혼/기혼/이혼/사별 |

### ❌ 제외
- **sob_02z1** - 졸업상태 (Skip Logic으로 인한 복잡도)

### ⭐ 중요: 비경제활동인구 처리

**`soa_06z2 == 88`은 "비경제활동인구"를 의미합니다.**

- 전체 데이터의 **약 35.6%** (31,973명)
- 학생, 주부, 은퇴자 등 포함
- **응답거부/결측값이 아닌 정상 분석 대상** ✅

**Feature Engineering으로 명확하게 처리:**
```python
from utils.data_cleaning import add_economic_status_features

df = add_economic_status_features(df)

# 생성되는 변수:
# - is_economically_inactive (int): 비경제활동인구 여부 (0/1)
# - is_economically_active (int): 경제활동인구 여부 (0/1)
# - economic_status (str): "비경제활동인구" / "경제활동인구"
```

📚 **자세한 내용**: [`docs/ECONOMIC_STATUS_GUIDE.md`](docs/ECONOMIC_STATUS_GUIDE.md) 참고

---

## 🎯 주요 가설

### H1: 교육수준
교육 수준이 높을수록 금연 성공률이 높다

### H2: 경제활동
경제활동 안정성이 높을수록 금연 성공률이 높다

### H3: 직업분류
직종별로 금연 성공률에 차이가 있다

### H4: 혼인상태
혼인 상태가 금연 성공에 영향을 미친다

---

## 🔧 유틸리티 함수 사용법

### 1. 데이터 정제

```python
from utils.data_cleaning import clean_data_for_analysis

# 데이터 정제 실행
df_clean, report = clean_data_for_analysis(
    input_path='../../data/analy_data.csv',
    output_path='./output/analy_data_cleaned.csv',
    verbose=True
)

# 정제 결과 요약
from utils.data_cleaning import get_analysis_summary
get_analysis_summary(report)
```

### 2. Feature Engineering (비경제활동인구)

```python
from utils.data_cleaning import add_economic_status_features

# Feature 생성
df = add_economic_status_features(df, verbose=True)

# 사용 예시
inactive_df = df[df['is_economically_inactive'] == 1]
active_df = df[df['is_economically_active'] == 1]

# 그룹별 금연 성공률
success_rate = df.groupby('economic_status')['churn'].mean()
```

### 3. 변수 코드 정보 확인

```python
from utils.data_cleaning import print_economic_code_info

# 변수 설명 출력
print_economic_code_info('soa_06z2')
```

### 4. 경제활동 상태별 요약 통계

```python
from utils.data_cleaning import get_economic_status_summary

# 요약 통계
summary = get_economic_status_summary(df, group_var='economic_status')
print(summary)
```

---

## ⚠️ 주의사항

### 📁 데이터 경로
- 원본 데이터: `../../data/analy_data.csv`
- 정제 데이터: `./output/analy_data_cleaned.csv`

### 👥 팀 공용 공간
- `data/` 폴더는 팀 공용이므로 **직접 수정 금지**
- 개인 파일은 `vfxpedia/` 폴더 내에서만 관리
- 분석 결과는 `output/` 폴더에 저장

### 📦 Import 경로

```python
import sys
sys.path.append('C:/SKN_19/SKN19-2nd-2Team')

# 팀 공용 유틸
from data.var_mapping import VAR_DICT, get_var_name, get_var_value
from util.decode_helper import decode_dataframe, filter_special_codes

# 개인 유틸 (Feature Engineering 포함)
sys.path.append('./utils')
from data_cleaning import (
    clean_data_for_analysis,
    add_economic_status_features,
    get_economic_status_summary,
    print_economic_code_info
)
```

---

## 📝 진행 상황

### ✅ 완료
- [x] 전체 데이터 파악 (`01_data_overview.ipynb`)
- [x] 데이터 품질 진단 (`02_diagnosis_data_quality.ipynb`)
- [x] 정제 전략 수립 (`03_data_cleaning_strategy.ipynb`)
- [x] 데이터 정제 스크립트 작성 (`utils/data_cleaning.py`)
- [x] Feature Engineering 구현 (비경제활동인구 처리)
- [x] 최종 데이터 정제 실행 (`04_data_cleaning_final.ipynb`)
- [x] 교육/경제 분석 진행 (`05_analysis_education_economy.ipynb`)

### 🚧 진행 중
- [ ] 추가 Feature Engineering (필요시)
- [ ] 머신러닝 모델링 (필요시)
- [ ] 특성 중요도 분석

### 📊 데이터 정제 결과

| 항목 | 값 |
|------|-----|
| 원본 데이터 | 89,822건 |
| 정제 후 데이터 | ~89,757건 |
| 제거율 | ~0.07% |
| 비경제활동인구 | 31,973건 (35.6%) |
| 최종 분석 변수 | 5개 |

---

## 📚 참고 문서

### 📖 가이드 문서
- **[비경제활동인구 처리 가이드](docs/ECONOMIC_STATUS_GUIDE.md)** ⭐ 필독!
  - Feature Engineering 방법
  - 코드 의미 설명
  - 사용 예시 및 Best Practice
  
- **[전체 사용 가이드](docs/USAGE_GUIDE.md)**
  - 프로젝트 전반 사용법
  
- **[PDF 확인 필요 변수](docs/PDF_VERIFICATION_NEEDED.md)**
  - 정의되지 않은 코드 목록

- **[원본 변수 설명 PDF](docs/CHS_Variable.pdf)**
  - 질병관리청 원본 변수 설명서

### 🔧 코드 모듈
- **[utils/data_cleaning.py](utils/data_cleaning.py)**
  - 데이터 정제 함수
  - Feature Engineering 함수
  - 요약 통계 함수

---

## 💡 Quick Start

### 새로운 노트북 시작할 때

```python
# 1. 라이브러리 임포트
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 경로 설정
sys.path.append('C:/SKN_19/SKN19-2nd-2Team')
sys.path.append('./utils')

# 2. 팀 공용 유틸
from data.var_mapping import VAR_DICT, get_var_name, get_var_value
from util.decode_helper import decode_dataframe

# 3. 개인 유틸 (Feature Engineering)
from data_cleaning import (
    clean_data_for_analysis,
    add_economic_status_features,
    get_economic_status_summary,
    print_economic_code_info
)

# 4. 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 5. 데이터 로드 & Feature 생성
df = pd.read_csv('../../data/analy_data.csv')
df = add_economic_status_features(df, verbose=False)

print("✅ 준비 완료!")
```

---

## 🤝 협업 규칙

1. **팀 공용 공간 (`data/`, `util/`) 수정 금지**
2. **개인 작업은 `notebooks/vfxpedia/` 내에서만**
3. **분석 결과는 `output/` 폴더에 저장**
4. **노트북 파일명은 번호_내용.ipynb 형식 유지**
5. **변수 코드 직접 사용 지양, Feature Engineering 활용 권장**

---

**최종 업데이트**: 2025-10-08  
**작성자**: 오흥재 (vfxpedia)

---

## 📮 문의

- 비경제활동인구 처리 방법: [`docs/ECONOMIC_STATUS_GUIDE.md`](docs/ECONOMIC_STATUS_GUIDE.md)
- 기타 문의: 오흥재 (vfxpedia)
