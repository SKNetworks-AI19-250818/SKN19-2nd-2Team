# 📊 EDA (Exploratory Data Analysis)

작성일: 2025-10-10  
담당자: 오흥재 (vfxpedia)

**지역사회건강조사 2024년 데이터**를 활용한 금연 성공률 예측 모델 개발을 위한 탐색적 데이터 분석 과정입니다.

---

## 📁 파일 구조

### 1️⃣ 데이터 이해 단계
| 노트북 | 설명 | 주요 내용 |
|--------|------|-----------|
| **01_data_overview.ipynb** | 전체 데이터 개요 | 기본 통계, 변수 분포, 상관관계 분석 |
| **02_decoder_test.ipynb** | Variable Decoder 가이드 | Fallback 시스템, 한글 라벨링 사용법 |

### 2️⃣ 데이터 품질 진단 및 정제
| 노트북 | 설명 | 주요 내용 |
|--------|------|-----------|
| **03_diagnosis_data_quality.ipynb** | 품질 진단 | 결측치, 이상치, 특수코드 파악 |
| **04_data_cleaning_strategy.ipynb** | 정제 전략 | 특수코드 처리 방안 수립 |
| **05_data_cleaning_final.ipynb** | 최종 정제 | 정제 데이터 생성 (`analy_data_cleaned.csv`) |

### 3️⃣ 심층 분석 (교육·경제 → 금연)
| 노트북 | 분석 변수 | 주요 발견사항 | 문서 |
|--------|-----------|---------------|------|
| **06_education_smoking_analysis.ipynb** | `sob_01z1` (교육수준) | 역U자 패턴, 중학력 흡연율 최고 | `06_insights.md` |
| **07_economic_activity_analysis.ipynb** | `soa_01z1`, `soa_06z2`, `soa_07z1` | 비경제활동자 성공률 13.75%p 높음 | `07_insights.md` |
| **08_analysis_education_economy.ipynb** | 교육 × 경제 상호작용 | 교차효과, Feature 우선순위 | - |

### 4️⃣ Feature Engineering (모델링 준비)
| 노트북 | 설명 | 출력 데이터 | 비고 |
|--------|------|------------|------|
| **09_feature_engineering.ipynb** | EDA 인사이트 기반 변수 변환 | `model_ready_data.csv` | `variable.csv` 업데이트 포함 |

---

## 🔧 사용 방법

### 📦 필수 라이브러리
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from scipy.stats import chi2_contingency
import matplotlib.font_manager as fm
```

### 🗂️ 경로 설정
모든 노트북은 **프로젝트 루트 기준** 상대 경로를 사용합니다:

```python
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.abspath('../../..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ✅ Variable Decoder import (Fallback 지원)
from notebooks.vfxpedia.utils.variable_decoder import (
    VariableDecoder,
    get_korean_label,
    get_korean_labels,
    create_korean_labels_dict
)

decoder = VariableDecoder()

# 📂 데이터 로드
df = pd.read_csv('../output/analy_data_cleaned.csv')  # 정제 데이터
```

### 🎨 팀 통일 시각화 스타일
```python
# 한글 폰트 설정
try:
    font_path = "C:/Windows/Fonts/HMFMMUEX.TTC"
    if os.path.exists(font_path):
        font_prop = fm.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()
    else:
        plt.rcParams['font.family'] = 'Malgun Gothic'
except:
    plt.rcParams['font.family'] = 'Malgun Gothic'

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (12, 6)

# 팀 컬러 (sosodoit 팀장님 스타일)
TEAM_COLORS = {
    'primary': '#1f77b4',
    'success': '#ff7f0e',  # 파란색 (금연성공=1)
    'danger': '#1f77b4',   # 주황색 (금연실패=0)
    'palette': ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']
}
```


### 📊 Variable Decoder 활용

**기본 사용법**:
```python
# 1. 값 디코딩
decoder.decode_value('sob_01z1', 5.0)  # '고등학교'

# 2. 한글 라벨 (시각화용)
get_korean_label('sob_01z1')  # '교육수준'

# 3. 여러 변수 라벨
labels = get_korean_labels(['sob_01z1', 'soa_01z1'], format_type='simple')
# → ['교육수준', '경제활동여부']

# 4. 히트맵 라벨링
x_labels = get_korean_labels(crosstab.columns, format_type='simple')
plt.xticks(range(len(x_labels)), x_labels, rotation=45)
```

**format_type 옵션**:
- `'simple'`: 한글만 (예: '교육수준')
- `'with_var'`: 변수명 포함 (예: 'sob_01z1 (교육수준)')
- `'newline'`: 줄바꿈 (예: 'sob_01z1\n(교육수준)')

---

## 📝 권장 실행 순서

### Phase 1: 데이터 이해 (01~02)
1. **01_data_overview.ipynb** - 전체 데이터 개요 파악
2. **02_decoder_test.ipynb** - Variable Decoder 사용법 익히기

### Phase 2: 데이터 정제 (03~05)
3. **03_diagnosis_data_quality.ipynb** - 품질 문제 진단
4. **04_data_cleaning_strategy.ipynb** - 정제 전략 수립
5. **05_data_cleaning_final.ipynb** - 최종 정제 실행

### Phase 3: 심층 분석 (06~08)
6. **06_education_smoking_analysis.ipynb** - 교육수준 분석
7. **07_economic_activity_analysis.ipynb** - 경제활동 분석
8. **08_analysis_education_economy.ipynb** - 교육·경제 통합 분석

### Phase 4: Feature Engineering (09)
9. **09_feature_engineering.ipynb** - 모델링용 변수 생성 및 데이터셋 저장

---

## 🔍 주요 분석 결과

### 📌 교육수준 분석 (06번 노트북)

**주요 발견**:
- **역U자 패턴**: 중간 학력에서 흡연율 최고
  - 전문대(2-3년제): 48.91%
  - 고등학교: 47.92%
  - 대학원: 26.59%
- **통계적 유의성**: χ² = 2,361, p < 0.001
- **상관관계 강도**: 크래머 V ≈ 0.16 (약한 상관)

**모델링 시사점**:
- ✅ 변수 포함 필수 (통계적으로 유의)
- 📝 3그룹 분류 권장 (저/중/고학력)
- 🔄 연령 보정 분석 필요

### 💼 경제활동 분석 (07번 노트북)

**주요 발견**:
- **비경제활동자 성공률**: 64.76% vs 경제활동자 51.01%
  - **차이**: 13.75%p (매우 큰 차이!)
- **직업별 차이**: 최대 22.71%p
  - 최고: 농림어업 62.31%
  - 최저: 군인 39.60%
- **통계적 유의성**: 모든 변수 p < 0.001

**모델링 시사점**:
- ⭐⭐⭐⭐⭐ **경제활동 여부** (최우선 Feature)
- ⭐⭐⭐⭐⭐ **직업분류** (3그룹 분류)
- ⭐⭐⭐⭐ **종사상지위** (보조 변수)

### 🔗 교육 × 경제 비교 (06 vs 07)

| 비교 항목 | 교육수준 | 경제활동 | 우선순위 |
|----------|----------|----------|----------|
| 효과 크기 | ~10%p | **13.75%p** | 경제 ✅ |
| 패턴 | 복잡 (역U자) | **명확** | 경제 ✅ |
| 예측력 | 중간 | **높음** | 경제 ✅ |
| χ² 통계량 | 2,361 | 1,374 | 교육 |

**핵심 결론**: **경제활동 변수가 교육수준보다 금연 성공 예측에 더 중요!**

---

## 🛠️ 코드 수정 가이드

### 📝 **Variable Decoder 최신 사용법**

**06, 07번 노트북 디코딩 방법**:
```python
df_work = df.copy()
df_work['sob_01z1_decoded'] = df_work['sob_01z1'].apply(
    lambda x: decoder.decode_value('sob_01z1', x)
)

# 한글 라벨 확인
print(f"sob_01z1: {get_korean_label('sob_01z1')}")  # "교육수준"
```

**시각화 한글화**:
```python
# 제목 한글화
var_label = get_korean_label('sob_01z1')
ax.set_title(f"sob_01z1 ({var_label})", fontsize=12)

# x축 라벨 한글화
korean_labels = [decoder.decode_value(var, code) for code in all_codes]
ax.set_xticklabels(korean_labels, rotation=45, ha='right')
```

---

## 📋 분석 결과 문서

각 심층 분석 노트북마다 상세한 인사이트 문서가 별도로 제공됩니다:

- **06_INSIGHTS.md**: 교육수준 분석 전체 결과
- **07_INSIGHTS.md**: 경제활동 분석 전체 결과

---

## 🔗 관련 리소스

### 📂 데이터
- **입력**: `../../../data/analy_data.csv` (팀 공통 분석 데이터)
- **출력**: `../output/analy_data_cleaned.csv` (정제 완료 데이터)

### 🛠️ 유틸리티
- **Variable Decoder**: `../utils/variable_decoder.py`
  - Fallback 시스템: `variable.csv` → `variable_full.csv`
  - 한글 라벨링: `get_korean_label()`, `get_korean_labels()`
  - 상세 가이드: `../utils/README.md`

### 📊 시각화
- **팀 스타일 가이드**: `../docs/VISUALIZATION_STYLE_GUIDE.md`
  - 팀 컬러 정의
  - 폰트 설정
  - 그래프 스타일 예시

---

## ⚠️ 주의사항

### 🔧 필수 설정
1. **Python 경로 추가**: 프로젝트 루트를 `sys.path`에 추가
2. **한글 폰트**: `HMFMMUEX.TTC` 또는 `Malgun Gothic`
3. **Variable Decoder**: Fallback 시스템 활용 (자동)

### 📝 코딩 규칙
- ✅ **디코딩**: `apply()` + `decode_value()` 사용
- ✅ **라벨링**: `get_korean_label()` 활용
- ✅ **시각화**: 팀 컬러 (`TEAM_COLORS`) 사용

### 🎯 상대 경로
- 팀 공통 데이터: `../../../data/`
- 개인 유틸: `../utils/`
- 개인 데이터: `../data/`
- 개인 출력: `../output/`

---

## 📅 업데이트 이력

- **2025-10-10**: 09번 Feature Engineering 노트북 완성, `model_ready_data.csv` 생성
- **2025-10-10**: 06~08번 노트북 분석 완료, Variable Decoder Fallback 시스템 추가
- **2025-10-09**: EDA 폴더 구조 정리, 경로 통일, 팀 시각화 스타일 적용
- **2025-10-09**: 01~05번 노트북 Variable Decoder 통합, 한글 라벨링 기능 추가

---

## 🎯 향후 계획

- [x] 연령대별 효과 분석
- [x] 교육 × 경제활동 상호작용 상세 분석
- [x] Feature Engineering 구체화
- [x] 최종 변수 선택 및 모델링 준비
- [ ] 베이스라인 모델 구축 (`../model/01_model_baseline.ipynb`)
- [ ] 모델 최적화 및 평가

