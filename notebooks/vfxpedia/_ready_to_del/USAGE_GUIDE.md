# VariableDecoder 사용 가이드

## 📁 파일 구조 (업데이트: 2025-10-09)

```
SKN19-2nd-2Team/
├── data/                                    # 팀 공통 데이터
│   ├── analy_data.csv                       # 분석용 데이터
│   └── raw_data.csv                         # 원본 데이터
│
└── notebooks/
    └── vfxpedia/                            # 개인 작업 공간
        ├── data/                            # 개인 데이터
        │   ├── variable.csv                 # ⭐ 변수 코드 매핑
        │   └── data_explain.csv             # 변수 설명
        │
        ├── utils/                           # 유틸리티
        │   ├── variable_decoder.py          # ⭐ 변수 디코더 (핵심)
        │   └── data_cleaning.py             # 데이터 정제
        │
        ├── eda/                             # EDA 노트북들
        └── docs/                            # 문서
```

---

## 🚀 빠른 시작

### 1. 기본 사용법 (Jupyter Notebook)

```python
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.abspath('../../..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# VariableDecoder import
from utils.variable_decoder import VariableDecoder
import pandas as pd

# 팀 공통 데이터 로드
df = pd.read_csv('../../../data/analy_data.csv')

# VariableDecoder 초기화 (자동으로 vfxpedia/data/variable.csv 로드)
decoder = VariableDecoder()

# 단일 값 디코딩
education_label = decoder.decode_value('sob_01z1', 5)
print(education_label)  # '고등학교'

# 컬럼 전체 디코딩
df = decoder.decode_column(df, 'sob_01z1')
print(df[['sob_01z1', 'sob_01z1_decoded']].head())
```

---

## 📊 주요 기능

### 1️⃣ 단일 값 디코딩

```python
decoder = VariableDecoder()

# 교육수준
print(decoder.decode_value('sob_01z1', 5))  # '고등학교'
print(decoder.decode_value('sob_01z1', 7))  # '4년제대학'

# 경제활동
print(decoder.decode_value('soa_01z1', 1))  # '예'
print(decoder.decode_value('soa_06z2', 88)) # '비경제활동인구'
```

### 2️⃣ 컬럼 디코딩 (새 컬럼 생성)

```python
# 단일 컬럼
df = decoder.decode_column(df, 'sob_01z1')
# → 'sob_01z1_decoded' 컬럼 생성

# 여러 컬럼 동시 디코딩
df = decoder.decode_multiple_columns(
    df, 
    ['sob_01z1', 'soa_01z1', 'sod_02z3']
)
# → 'sob_01z1_decoded', 'soa_01z1_decoded', 'sod_02z3_decoded' 컬럼 생성
```

### 3️⃣ Value Counts (디코딩된 결과로)

```python
# 원본 코드값으로 집계 → 자동으로 라벨로 변환
edu_counts = decoder.create_value_counts_decoded(df, 'sob_01z1')
print(edu_counts)

# 출력:
# 고등학교       31369
# 4년제대학      21721
# 2년3년제대학    11171
# ...
```

### 4️⃣ 변수 정보 조회

```python
# 변수명 조회
var_label = decoder.get_variable_label('sob_01z1')
print(var_label)  # '교육수준'

# 코드 매핑 전체 조회
code_mapping = decoder.get_code_mapping('sob_01z1')
print(code_mapping)
# {1: '무학', 2: '서당한학', 3: '초등학교', ...}

# 변수 전체 정보
var_info = decoder.get_variable_info('sob_01z1')
print(var_info)
```

---

## 💡 실전 활용 예제

### 예제 1: EDA - 분포 확인

```python
import matplotlib.pyplot as plt
import seaborn as sns

decoder = VariableDecoder()
df = pd.read_csv('../../../data/analy_data.csv')

# 디코딩된 value counts
edu_dist = decoder.create_value_counts_decoded(df, 'sob_01z1')

# 시각화
fig, ax = plt.subplots(figsize=(10, 6))
edu_dist.plot(kind='barh', ax=ax)
ax.set_title('교육수준별 분포', fontsize=16)
ax.set_xlabel('빈도')
plt.tight_layout()
plt.show()
```

### 예제 2: 데이터 정제 - 특수코드 제거

```python
decoder = VariableDecoder()

# 응답거부, 모름 코드 확인
code_mapping = decoder.get_code_mapping('sob_01z1')
special_codes = [code for code, label in code_mapping.items() 
                 if '응답거부' in label or '모름' in label]

print(f"특수코드: {special_codes}")  # [77, 99]

# 제거
df_clean = df[~df['sob_01z1'].isin(special_codes)]
print(f"원본: {len(df)}건 → 정제: {len(df_clean)}건")
```

### 예제 3: 그룹별 분석

```python
# 교육수준별 금연 성공률
df_decoded = decoder.decode_column(df, 'sob_01z1')

success_rate = df_decoded.groupby('sob_01z1_decoded')['churn'].agg([
    ('표본수', 'count'),
    ('금연성공', 'sum'),
    ('성공률(%)', lambda x: x.mean() * 100)
])

print(success_rate.round(2))
```

### 예제 4: 교차분석 (히트맵)

```python
import seaborn as sns

# 두 변수 디코딩
df_decoded = decoder.decode_multiple_columns(df, ['sob_01z1', 'soa_01z1'])

# 교차표 (비율)
crosstab_pct = pd.crosstab(
    df_decoded['sob_01z1_decoded'],
    df_decoded['soa_01z1_decoded'],
    normalize='index'
) * 100

# 히트맵
plt.figure(figsize=(8, 6))
sns.heatmap(crosstab_pct, annot=True, fmt='.1f', cmap='YlOrRd')
plt.title('교육수준 × 경제활동 비율 (%)')
plt.tight_layout()
plt.show()
```

---

## 🔧 고급 기능

### 커스텀 CSV 경로 지정

```python
# 다른 경로의 variable.csv 사용
decoder = VariableDecoder(csv_path='path/to/your/variable.csv')
```

### 캐시 활용 (성능 최적화)

```python
# VariableDecoder는 내부적으로 캐시를 사용합니다
decoder = VariableDecoder()

# 첫 호출: variable.csv 로드
decoder.decode_value('sob_01z1', 5)

# 이후 호출: 캐시에서 즉시 반환 (빠름!)
decoder.decode_value('sob_01z1', 7)
```

---

## ⚠️ 주의사항

### 1. 프로젝트 루트 경로 설정 필수

```python
# ❌ 잘못된 예
from utils.variable_decoder import VariableDecoder  # ModuleNotFoundError!

# ✅ 올바른 예
import sys
import os
project_root = os.path.abspath('../../..')
sys.path.insert(0, project_root)

from utils.variable_decoder import VariableDecoder  # 성공!
```

### 2. 디코딩 전 결측치 처리

```python
# NaN이 포함된 경우 dropna=True 사용
value_counts = decoder.create_value_counts_decoded(df, 'sob_01z1', dropna=True)
```

### 3. 비경제활동인구(88) 처리

```python
# soa_06z2 = 88은 "비경제활동인구"로 정상값입니다!
# 응답거부/모름과 다르게 제거하면 안 됩니다

# ❌ 잘못된 처리
df_clean = df[df['soa_06z2'] < 88]  # 비경제활동인구 35% 손실!

# ✅ 올바른 처리
# 88을 분석에 포함 (별도 카테고리로 취급)
```

📚 **자세한 내용**: [`ECONOMIC_STATUS_GUIDE.md`](ECONOMIC_STATUS_GUIDE.md) 참고

---

## 🔗 관련 리소스

- **VariableDecoder 소스**: `../utils/variable_decoder.py`
- **변수 매핑 데이터**: `../data/variable.csv`
- **사용 예제**: `../examples/decoder_usage.py`
- **EDA 노트북들**: `../eda/`

---

## 📝 팀원들을 위한 팁

1. **노트북 시작 시 표준 템플릿**:
```python
import sys, os
project_root = os.path.abspath('../../..')
sys.path.insert(0, project_root)

from utils.variable_decoder import VariableDecoder
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

decoder = VariableDecoder()
df = pd.read_csv('../../../data/analy_data.csv')
```

2. **변수명을 모를 때**:
```python
# variable.csv 직접 확인
var_df = pd.read_csv('../data/variable.csv')
print(var_df[var_df['var_code'].str.contains('교육')])
```

3. **에러 발생 시 체크리스트**:
   - [ ] `sys.path` 설정 확인
   - [ ] `variable.csv` 파일 존재 확인
   - [ ] import 경로 (`utils.variable_decoder`) 확인
   - [ ] 상대 경로 (`../../../data/`) 확인

---

**작성**: 오흥재 (vfxpedia)  
**최종 업데이트**: 2025-10-09
