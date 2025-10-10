# 🛠️ 유틸리티 (Utils)

작성일: 2025-10-10  
담당자: 오흥재 (vfxpedia)

**지역사회건강조사 데이터 분석 및 모델링을 위한 유틸리티 모음입니다.**

---

## 📁 파일 구조

| 파일 | 설명 | 주요 기능 |
|------|------|-----------|
| `variable_decoder.py` | 변수 코드 → 한글 텍스트 변환 | 디코딩, 라벨링, Fallback 시스템 |
| `feature_engineering.py` | Feature Engineering 함수 | EDA 인사이트 기반 변수 변환 |
| `data_cleaning.py` | 데이터 정제 | 특수코드 처리, 결측치 처리 |

---

# 🔤 Variable Decoder

**지역사회건강조사 데이터의 변수 코드를 의미있는 한글 텍스트로 자동 변환하는 유틸리티입니다.**

---

## 📌 핵심 기능

### 🔄 2단계 Fallback 시스템
1. **메인**: `variable.csv` (우선 사용)
2. **Fallback**: `variable_full.csv` (메인에 없을 경우 자동 사용)

→ 사용자는 신경 쓸 필요 없이 가장 적절한 라벨을 자동으로 가져옵니다!

### 🎨 한글 라벨링 (시각화용)
- 히트맵, 막대그래프 등의 축 라벨을 한글로 자동 변환
- 3가지 포맷 옵션 (`simple`, `with_var`, `newline`)

---

## 🚀 빠른 시작

### 기본 사용법 (Jupyter Notebook)

```python
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.abspath('../../..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Variable Decoder import
from notebooks.vfxpedia.utils.variable_decoder import (
    VariableDecoder,
    get_korean_label,
    get_korean_labels,
    create_korean_labels_dict
)

# 초기화
decoder = VariableDecoder()

# 1. 단일 값 디코딩
label = decoder.decode_value('sob_01z1', 5.0)
print(label)  # "고등학교"

# 2. 한글 라벨 (시각화용)
korean = get_korean_label('sob_01z1')
print(korean)  # "교육수준"
```

---

## 📊 주요 기능

### 1️⃣ 값 디코딩

```python
# 교육수준 코드 → 한글
decoder.decode_value('sob_01z1', 1)   # "무학"
decoder.decode_value('sob_01z1', 5)   # "고등학교"
decoder.decode_value('sob_01z1', 7)   # "4년제대학"

# 흡연상태 코드 → 한글
decoder.decode_value('sma_03z2', 1)   # "매일 피움"
decoder.decode_value('sma_03z2', 3)   # "과거에는 피웠으나 현재 피우지 않음"
```

### 2️⃣ 데이터프레임 디코딩

```python
import pandas as pd

# 데이터 로드
df = pd.read_csv('../../../data/analy_data.csv')

# 방법 1: apply() 사용 (권장)
df['sob_01z1_decoded'] = df['sob_01z1'].apply(
    lambda x: decoder.decode_value('sob_01z1', x)
)

# 방법 2: 여러 변수 한번에
for var in ['sob_01z1', 'soa_01z1', 'sma_03z2']:
    df[f'{var}_decoded'] = df[var].apply(
        lambda x: decoder.decode_value(var, x)
    )
```

### 3️⃣ Value Counts (디코딩)

```python
# 기존 방식 (코드만 보임)
df['sob_01z1'].value_counts()
# 5.0    31369
# 7.0    21721
# ...

# 디코딩 방식 (의미가 보임)
decoder.create_value_counts_decoded(df, 'sob_01z1')
# 고등학교      31369
# 4년제대학     21721
# ...
```

### 4️⃣ 한글 라벨링 (시각화용)

```python
# 단일 변수
label = get_korean_label('sob_01z1')
print(label)  # "교육수준"

# 여러 변수 (옵션 1: 한글만)
labels = get_korean_labels(['sob_01z1', 'soa_01z1'], format_type='simple')
print(labels)  # ['교육수준', '경제활동여부']

# 여러 변수 (옵션 2: 변수명 + 한글)
labels = get_korean_labels(['sob_01z1', 'soa_01z1'], format_type='with_var')
print(labels)  # ['sob_01z1 (교육수준)', 'soa_01z1 (경제활동여부)']

# 여러 변수 (옵션 3: 줄바꿈 - 히트맵용)
labels = get_korean_labels(['sob_01z1', 'soa_01z1'], format_type='newline')
print(labels)  # ['sob_01z1\n(교육수준)', 'soa_01z1\n(경제활동여부)']

# 딕셔너리 형태
labels_dict = create_korean_labels_dict(['sob_01z1', 'soa_01z1'])
print(labels_dict)  # {'sob_01z1': '교육수준', 'soa_01z1': '경제활동여부'}
```

---

## 🎯 실전 예제

### 예제 1: 히트맵에 한글 라벨 적용

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 상관관계 매트릭스 생성
numeric_cols = ['age', 'sob_01z1', 'soa_01z1', 'churn']
corr_matrix = df[numeric_cols].corr()

# 히트맵 생성
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, 
            annot=True, 
            fmt='.2f',
            cmap='coolwarm',
            center=0,
            square=True)

# ✅ 한글 라벨 적용
korean_labels = get_korean_labels(corr_matrix.columns, format_type='simple')
plt.xticks(range(len(korean_labels)), korean_labels, rotation=45, ha='right')
plt.yticks(range(len(korean_labels)), korean_labels, rotation=0)

plt.title('상관관계 히트맵 (한글 라벨)', fontsize=14)
plt.tight_layout()
plt.show()
```

### 예제 2: 막대그래프에 한글 제목 적용

```python
# 교육수준별 분포
edu_counts = decoder.create_value_counts_decoded(df, 'sob_01z1')

plt.figure(figsize=(10, 6))
edu_counts.plot(kind='bar', color='steelblue')

# ✅ 한글 제목
var_label = get_korean_label('sob_01z1')
plt.title(f'{var_label}별 분포', fontsize=14)
plt.xlabel(var_label, fontsize=12)
plt.ylabel('빈도', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

### 예제 3: 여러 변수 분석

```python
# 분석 변수
key_vars = ['sob_01z1', 'soa_01z1', 'soa_06z2']

# 디코딩
for var in key_vars:
    df[f'{var}_decoded'] = df[var].apply(
        lambda x: decoder.decode_value(var, x)
    )

# 한글 라벨 확인
for var in key_vars:
    label = get_korean_label(var)
    print(f"{var}: {label}")

# 출력:
# sob_01z1: 교육수준
# soa_01z1: 경제활동여부
# soa_06z2: 직업분류
```

---

## 🔧 주요 메서드

### 📊 데이터 디코딩

| 메서드 | 설명 | 예시 |
|--------|------|------|
| `decode_value(var, code)` | 단일 값 디코딩 | `decode_value('sob_01z1', 5)` |
| `create_value_counts_decoded(df, col)` | value_counts (디코딩) | `create_value_counts_decoded(df, 'sob_01z1')` |

### 🎨 한글 라벨링 (시각화용)

| 메서드 | 설명 | 반환값 |
|--------|------|--------|
| `get_korean_label(var)` | 단일 변수 한글 라벨 | `'교육수준'` |
| `get_korean_labels(vars, format_type)` | 여러 변수 한글 라벨 리스트 | `['교육수준', '경제활동여부']` |
| `create_korean_labels_dict(vars)` | 한글 라벨 딕셔너리 | `{'sob_01z1': '교육수준'}` |

### 📋 변수 정보 조회

| 메서드 | 설명 | 예시 |
|--------|------|------|
| `get_variable_label(var)` | 변수 라벨 조회 | `get_variable_label('sob_01z1')` → '교육수준' |
| `get_variable_info(var)` | 변수 상세 정보 | `get_variable_info('sob_01z1')` |
| `print_variable_summary(var)` | 변수 정보 출력 | `print_variable_summary('sob_01z1')` |
| `get_code_mapping(var)` | code→meaning 딕셔너리 | `get_code_mapping('sob_01z1')` |

---

## 📋 format_type 옵션

| format_type | 출력 형식 | 사용 예시 |
|-------------|----------|----------|
| `'simple'` | 한글만 (예: '교육수준') | 막대그래프, 파이차트 |
| `'with_var'` | 변수명 + 한글 (예: 'sob_01z1 (교육수준)') | 범례, 타이틀 |
| `'newline'` | 변수명\n한글 (예: 'sob_01z1\n(교육수준)') | 히트맵, 복잡한 그래프 |

---

## ⚠️ 주의사항

### 🔄 Fallback 시스템 작동 원리

**자동 우선순위:**
1. `variable.csv`에 라벨이 있으면 → **메인 사용** ✅
2. `variable.csv`에 없으면 → **variable_full.csv에서 자동으로 가져옴** 🔄
3. 둘 다 없으면 → **변수명 그대로 반환** 📝

**예시:**
```python
# sob_01z1이 variable.csv에 있음 → variable.csv 사용
label = decoder.get_variable_label('sob_01z1')  # "교육수준"

# mtc_03z1이 variable.csv에 없음 → variable_full.csv 자동 사용
label = decoder.get_variable_label('mtc_03z1')  # "mtc 03z1" (fallback)

# unknown_var가 둘 다 없음 → 변수명 그대로
label = decoder.get_variable_label('unknown_var')  # "unknown_var"
```

### 📁 파일별 역할

| 파일 | 역할 | 편집 가능 | 우선순위 |
|------|------|-----------|----------|
| `variable.csv` | 팀이 주로 사용하는 변수 | ✅ **자유롭게 편집** | 🥇 1순위 |
| `variable_full.csv` | 전체 변수 (백업용) | ⚠️ **수정 비권장** | 🥈 2순위 (fallback) |
| `variable_decoder.py` | 디코딩 로직 | ❌ **수정 금지** | - |

### 📝 variable.csv 업데이트 방법

**구조:**
```csv
variable,label,code,meaning,category
sob_01z1,교육수준,1,무학,교육경제활동
sob_01z1,교육수준,5,고등학교,교육경제활동
...
```

**편집 방법:**
1. Excel/Google Sheets에서 `../data/variable.csv` 열기
2. 새로운 변수 추가 또는 기존 변수 수정
3. CSV 저장 (UTF-8 인코딩)
4. Git commit & push

### 🔧 기타 주의사항

- **코드 타입**: `5`, `5.0`, `"5"` 모두 동일하게 처리됨
- **결측값**: `NaN`, `None` → `"Missing"` 으로 반환
- **매핑 없는 코드**: 원래 코드값 그대로 반환

---

## 📁 파일 구조

```
SKN19-2nd-2Team/
├── data/
│   └── analy_data.csv                    # 팀 공통 분석 데이터
│
└── notebooks/
    └── vfxpedia/
        ├── data/
        │   ├── variable.csv              # ⭐ 변수 매핑 (메인)
        │   └── variable_full.csv         # 변수 매핑 (Fallback)
        │
        ├── utils/
        │   ├── variable_decoder.py       # ⭐ Variable Decoder (핵심)
        │   ├── __init__.py               # 모듈 export
        │   └── README.md                 # 이 문서
        │
        └── eda/
            ├── 01_data_overview.ipynb
            ├── 02_decoder_test.ipynb     # ⭐ 사용 예제 및 테스트
            └── ...
```

---

## 📚 관련 문서

- **사용 예제**: `../eda/02_decoder_test.ipynb` - Variable Decoder 전체 기능 테스트 및 예제
- **EDA 가이드**: `../eda/README.md` - 전체 EDA 프로세스 및 Variable Decoder 활용법
- **시각화 스타일**: `../docs/VISUALIZATION_STYLE_GUIDE.md` - 팀 통일 시각화 스타일

---

## 🎯 사용 권장사항

### ✅ 권장
- `apply()` + `decode_value()`로 디코딩
- `get_korean_label()` 활용한 시각화 한글화
- `variable.csv` 자유롭게 편집
- Fallback 시스템 활용 (자동)

### ⚠️ 주의
- `variable_full.csv` 수정 비권장
- `variable_decoder.py` 직접 수정 금지

---

---

# 🔧 Feature Engineering

**EDA 06, 07, 08번 노트북의 인사이트를 바탕으로 모델링용 변수를 생성하는 모듈입니다.**

---

## 📌 핵심 기능

### 생성되는 Feature 목록

| 함수 | 원본 변수 | 새 변수 | 변환 방법 | 근거 |
|------|----------|---------|-----------|------|
| `group_education()` | `sob_01z1` | `education_group` | 3그룹 분류 | 06번: 역U자 패턴 |
| `is_economically_active()` | `soa_01z1` | `is_economically_active` | Binary | 07번: 13.75%p 차이 |
| `group_job_risk()` | `soa_06z2` | `job_risk_group` | 3그룹 분류 | 07번: 22.71%p 차이 |
| `is_employee()` | `soa_07z1` | `is_employee` | Binary | 07번: 7.46%p 차이 |

---

## 🚀 빠른 시작

### 전체 Feature Engineering 일괄 적용

```python
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.abspath('../../..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import pandas as pd
from notebooks.vfxpedia.utils.feature_engineering import (
    apply_feature_engineering,
    print_feature_info
)

# 데이터 로드
df = pd.read_csv('../output/analy_data_cleaned.csv')

# Feature Engineering 적용
df_fe = apply_feature_engineering(df)

# 생성된 Feature 설명 출력
print_feature_info()

print(f"✅ 생성된 새 변수: {df_fe.shape[1] - df.shape[1]}개")
```

### 개별 함수 사용

```python
from notebooks.vfxpedia.utils.feature_engineering import (
    group_education,
    is_economically_active,
    group_job_risk,
    is_employee
)

# 1. 교육수준 그룹화
df['education_group'] = df['sob_01z1'].apply(group_education)

# 2. 경제활동 여부
df['is_economically_active'] = df['soa_01z1'].apply(is_economically_active)

# 3. 직업 위험도
df['job_risk_group'] = df['soa_06z2'].apply(group_job_risk)

# 4. 임금근로자 여부
df['is_employee'] = df['soa_07z1'].apply(is_employee)
```

---

## 📊 Feature 상세 설명

### 1️⃣ education_group (교육수준 그룹)

**변환 규칙**:
```python
0: 저학력_저위험 (무학~초등)        # 흡연율 27.5%
1: 중학력_고위험 (중학~전문대)      # 흡연율 44.4%
2: 고학력_중위험 (4년제~대학원)     # 흡연율 33.3%
```

**EDA 인사이트 (06번 노트북)**:
- 역U자 패턴: 중간 학력에서 흡연율 최고
- 8개 카테고리 → 3개 그룹으로 단순화
- 모델 해석 가능성 향상

---

### 2️⃣ is_economically_active (경제활동 여부)

**변환 규칙**:
```python
0: 비경제활동자  # 금연 성공률 64.76%
1: 경제활동자    # 금연 성공률 51.01%
```

**EDA 인사이트 (07번 노트북)**:
- **효과 크기**: 13.75%p (매우 큰 효과!)
- **가장 강력한 예측 변수**
- Binary 변수로 충분

---

### 3️⃣ job_risk_group (직업 위험도)

**변환 규칙**:
```python
-1: 해당없음 (비경제활동자)
 0: 저위험_고성공 (농림어업, 전문가, 관리자)     # 53~62%
 1: 중위험 (단순노무, 사무, 기계조작, 판매)      # 47~52%
 2: 고위험_저성공 (서비스, 기능원, 군인)         # 40~45%
```

**EDA 인사이트 (07번 노트북)**:
- 직업별 금연 성공률 최대 **22.71%p** 차이
- 10개 직업 → 3개 위험도 그룹
- 경제활동자에 대한 세부 정보

---

### 4️⃣ is_employee (임금근로자 여부)

**변환 규칙**:
```python
0: 자영업/고용주/무급가족  # 금연 성공률 55.6%
1: 임금근로자              # 금연 성공률 48.22%
```

**EDA 인사이트 (07번 노트북)**:
- 효과 크기: 7.46%p
- 종사상지위 정보 단순화
- 보조 변수로 활용

---

## 📋 변수 중요도 예상

| 순위 | 변수 | 효과 크기 | 예상 중요도 |
|------|------|-----------|-------------|
| 1 | `is_economically_active` | 13.75%p | ⭐⭐⭐⭐⭐ |
| 2 | `job_risk_group` | 22.71%p | ⭐⭐⭐⭐⭐ |
| 3 | `education_group` | ~10%p | ⭐⭐⭐ |
| 4 | `is_employee` | 7.46%p | ⭐⭐⭐ |

---

## 🔗 관련 노트북

- **06_education_smoking_analysis.ipynb**: 교육수준 분석 (역U자 패턴)
- **07_economic_activity_analysis.ipynb**: 경제활동 분석 (13.75%p 효과)
- **08_analysis_education_economy.ipynb**: 교육×경제 통합 분석
- **09_feature_engineering.ipynb**: Feature Engineering 적용 및 데이터셋 생성

---

## 📁 출력 데이터

**파일명**: `model_ready_data.csv`  
**위치**: `../output/model_ready_data.csv`

**내용**:
- 원본 데이터의 모든 변수
- 추가된 Feature Engineering 변수 4개
- 타겟 변수: `churn` (금연 성공=1, 실패=0)

**중요**: 생성된 변수들은 `variable.csv`에 자동 등록되어 Variable Decoder와 통합됩니다!

---

## 🎯 사용 권장사항

### ✅ 권장
- `apply_feature_engineering()` 사용하여 일괄 적용
- 09번 노트북에서 생성된 `model_ready_data.csv` 사용
- 모델링 시 원본 변수 대신 변환된 변수 사용

### ❌ 비권장
- 원본 변수와 변환 변수 동시 사용 (다중공선성)
- Feature Engineering 없이 원본 변수만 사용 (성능 저하)

---

**마지막 업데이트:** 2025-10-10
