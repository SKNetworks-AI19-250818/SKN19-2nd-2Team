# Variable Decoder 사용 가이드

## 📌 개요

건강조사 데이터의 **변수 코드를 의미있는 한글 텍스트로 자동 변환**하는 유틸리티입니다.

`variable.csv`를 기반으로 모든 변수의 코드값을 해석합니다.

---

## 🚀 빠른 시작

### 1. 기본 사용법

```python
from util.variable_decoder import VariableDecoder

# 디코더 초기화
decoder = VariableDecoder()

# 단일 값 디코딩
교육수준 = decoder.decode_value('sob_01z1', 5)
print(교육수준)  # "고등학교"

흡연상태 = decoder.decode_value('sma_03z2', 3)
print(흡연상태)  # "과거에는 피웠으나 현재 피우지 않음"
```

### 2. 데이터프레임 디코딩

```python
import pandas as pd

# 데이터 로드
df = pd.read_csv('data/analy_data.csv')

# 단일 컬럼 디코딩
df = decoder.decode_column(df, 'sob_01z1')
# → df에 'sob_01z1_label' 컬럼 추가

# 여러 컬럼 한번에 디코딩
df = decoder.decode_multiple_columns(df, [
    'sob_01z1',  # 교육수준
    'soa_01z1',  # 경제활동여부
    'sma_03z2',  # 흡연상태
])
```

---

## 📊 주요 기능

### 1️⃣ 단일 값 디코딩

```python
# 교육수준 코드 → 한글
decoder.decode_value('sob_01z1', 1)  # "무학"
decoder.decode_value('sob_01z1', 5)  # "고등학교"
decoder.decode_value('sob_01z1', 7)  # "4년제대학"

# 흡연상태 코드 → 한글
decoder.decode_value('sma_03z2', 1)  # "매일 피움"
decoder.decode_value('sma_03z2', 3)  # "과거에는 피웠으나 현재 피우지 않음"
```

### 2️⃣ Value Counts (디코딩)

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

### 3️⃣ 변수 정보 조회

```python
# 변수 상세 정보 출력
decoder.print_variable_summary('sob_01z1')

# 출력 예시:
# ============================================================
# 📊 변수: sob_01z1
# 🏷️  라벨: 교육수준
# 📁 카테고리: 교육경제
# ============================================================
# 
# 코드 매핑:
#      1 → 무학
#      2 → 서당한학
#      3 → 초등학교
#      ...
```

---

## 🎯 실전 예제

### 예제 1: 교육수준별 분석

```python
from util.variable_decoder import VariableDecoder
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드 & 디코딩
df = pd.read_csv('data/analy_data.csv')
decoder = VariableDecoder()
df = decoder.decode_column(df, 'sob_01z1')

# 분석
교육수준별분포 = df['sob_01z1_label'].value_counts()
print(교육수준별분포)

# 시각화
교육수준별분포.plot(kind='bar')
plt.title('교육수준별 분포')
plt.xlabel('교육수준')
plt.ylabel('빈도')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
```

### 예제 2: 흡연상태별 금연성공률

```python
# 흡연상태 디코딩
df = decoder.decode_column(df, 'sma_03z2')

# 교차 분석
success_rate = df.groupby('sma_03z2_label')['churn'].mean() * 100
print(f"흡연상태별 금연성공률:\n{success_rate}")

# 시각화
success_rate.plot(kind='barh')
plt.title('흡연상태별 금연성공률')
plt.xlabel('성공률 (%)')
plt.tight_layout()
plt.show()
```

### 예제 3: 여러 변수 한번에 처리

```python
# 분석에 필요한 변수들 한번에 디코딩
key_vars = [
    'sob_01z1',  # 교육수준
    'soa_01z1',  # 경제활동여부
    'soa_06z2',  # 직업분류
    'sma_03z2',  # 흡연상태
    'smb_09z1',  # 금연기간
]

df = decoder.decode_multiple_columns(df, key_vars)

# 이제 모든 변수에 _label 컬럼이 생성됨
print(df.columns.tolist())
```

---

## 💡 편의 함수

클래스를 만들지 않고 바로 사용할 수 있는 함수들:

```python
from util.variable_decoder import decode_value, decode_column, print_var_info

# 단일 값 디코딩
label = decode_value('sob_01z1', 5)
print(label)  # "고등학교"

# 데이터프레임 디코딩
df = decode_column(df, 'sob_01z1')

# 변수 정보 출력
print_var_info('sob_01z1')
```

---

## 📁 파일 구조

```
SKN19-2nd-2Team/
├── util/
│   ├── variable_decoder.py    ← 메인 모듈
│   └── README.md              ← 이 파일
├── data/
│   ├── variable.csv           ← 변수 매핑 데이터 (원본)
│   └── analy_data.csv         ← 분석 데이터
└── notebooks/
    └── vfxpedia/
        └── 02_decoder_test.ipynb  ← 사용 예제
```

---

## 🔧 주요 메서드

| 메서드 | 설명 | 예시 |
|--------|------|------|
| `decode_value(var, code)` | 단일 값 디코딩 | `decode_value('sob_01z1', 5)` |
| `decode_column(df, col)` | 컬럼 디코딩 | `decode_column(df, 'sob_01z1')` |
| `decode_multiple_columns(df, cols)` | 여러 컬럼 디코딩 | `decode_multiple_columns(df, ['sob_01z1', 'sma_03z2'])` |
| `create_value_counts_decoded(df, col)` | value_counts (디코딩) | `create_value_counts_decoded(df, 'sob_01z1')` |
| `get_variable_label(var)` | 변수 라벨 조회 | `get_variable_label('sob_01z1')` → '교육수준' |
| `get_variable_info(var)` | 변수 상세 정보 | `get_variable_info('sob_01z1')` |
| `print_variable_summary(var)` | 변수 정보 출력 | `print_variable_summary('sob_01z1')` |
| `get_code_mapping(var)` | code→meaning 딕셔너리 | `get_code_mapping('sob_01z1')` |
| `get_all_variables(category)` | 변수 목록 | `get_all_variables('교육경제')` |
| `get_categories()` | 카테고리 목록 | `get_categories()` |

---

## ⚠️ 주의사항

### 1. variable.csv 업데이트

새로운 변수를 추가하거나 수정할 때는 `data/variable.csv`를 직접 편집하세요.

**variable.csv 구조:**
```csv
variable,label,code,meaning,category
sob_01z1,교육수준,1,무학,교육경제
sob_01z1,교육수준,5,고등학교,교육경제
...
```

### 2. 코드 타입

코드값은 자동으로 숫자/문자열 변환됩니다:
- `5`, `5.0`, `"5"` 모두 동일하게 처리됨

### 3. 결측값 처리

- `NaN`, `None` → `"Missing"` 으로 반환
- 매핑 없는 코드 → 원래 코드값 그대로 반환

---

## 🤝 팀원 협업

### variable.csv 업데이트 방법

1. **Excel/Google Sheets**에서 `data/variable.csv` 열기
2. 새로운 변수 추가 또는 기존 변수 수정
3. CSV 저장 (UTF-8 인코딩)
4. Git commit & push

### 주의: 다른 파일은 수정하지 마세요!

- ✅ `data/variable.csv` - 자유롭게 수정 가능
- ❌ `util/variable_decoder.py` - 코드 수정 금지

---

## 📞 문의

문제가 있거나 새로운 기능이 필요하면 팀 채널에 문의하세요!

**담당자:** vfxpedia

---

**마지막 업데이트:** 2025-10-09
