# 변수 디코딩 시스템 사용 가이드

## 📁 파일 구조

```
SKN19-2nd-2Team/
├── data/
│   ├── var_mapping.py              # 변수 디코딩 딕셔너리 (핵심!)
│   ├── PDF_VERIFICATION_NEEDED.md  # PDF 확인 필요 변수 목록
│   └── analy_data.csv
├── util/
│   ├── __init__.py
│   └── decode_helper.py            # 디코딩 유틸 함수 모음
└── notebooks/
    └── vfxpedia/
        └── eda__oo.ipynb
```

---

## 🚀 빠른 시작

### 1. 기본 사용법

```python
# Jupyter Notebook에서
import sys
sys.path.append('C:/SKN_19/SKN19-2nd-2Team')

from data.var_mapping import VAR_DICT, get_var_name, get_var_value
from util.decode_helper import decode_column, decode_dataframe, get_label
import pandas as pd

# 데이터 로드
df = pd.read_csv('../../data/analy_data.csv')

# 변수명 조회
print(get_var_name('nua_01z2'))  # '아침식사 빈도'

# 코드값 의미 조회
print(get_var_value('nua_01z2', 1))  # '주 5~7회'
```

---

## 📊 주요 활용 사례

### Case 1: EDA - 변수 정보 확인

```python
from util.decode_helper import print_var_info

# 변수 상세 정보 출력
print_var_info('sob_01z1')  # 교육수준
print_var_info('soa_06z2')  # 직업분류
```

**출력 예시:**
```
==================================================
변수코드: sob_01z1
변수명: 교육수준(최종학력)
카테고리: 교육경제-교육
타입: categorical
--------------------------------------------------
코드값:
  1: 무학
  2: 서당/한학
  3: 초등학교
  4: 중학교
  5: 고등학교
  6: 2-3년제 대학
  7: 4년제 대학
  8: 대학원 이상
==================================================
```

---

### Case 2: 데이터 정제 - 특수코드 제거

```python
from util.decode_helper import filter_special_codes

# 응답거부, 모름 제거
df_clean = filter_special_codes(df, 'mta_01z1', drop=True)

print(f"원본 데이터: {len(df)}건")
print(f"정제 데이터: {len(df_clean)}건")
```

---

### Case 3: 시각화 - 라벨 적용

```python
from util.decode_helper import decode_dataframe, get_label, prepare_plot_data
import matplotlib.pyplot as plt
import seaborn as sns

# 방법 1: 직접 디코딩
df['교육수준_라벨'] = decode_dataframe(df, 'sob_01z1')

# 방법 2: 시각화용 데이터 준비
plot_data = prepare_plot_data(df, 'sob_01z1', sort_by='code', remove_special=True)

# 막대 그래프
plt.figure(figsize=(10, 6))
plt.bar(plot_data['label'], plot_data['count'])
plt.xlabel(get_label('sob_01z1'))
plt.ylabel('빈도')
plt.title('교육수준 분포')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

---

### Case 4: 상관분석 - 교차표 생성

```python
from util.decode_helper import create_crosstab_with_labels

# 교육수준 X 금연성공 교차표 (비율 포함)
ct = create_crosstab_with_labels(
    df, 
    'sob_01z1',  # 교육수준
    'churn',      # 금연성공
    normalize='index'
)

print(ct)

# 히트맵
plt.figure(figsize=(8, 6))
sns.heatmap(ct, annot=True, fmt='.2%', cmap='YlGnBu')
plt.title('교육수준에 따른 금연 성공률')
plt.tight_layout()
plt.show()
```

---

### Case 5: 통계 분석 - 요약 통계

```python
from util.decode_helper import get_summary_stats

# 범주형 변수 요약
get_summary_stats(df, 'sex')

# 연속형 변수 요약
get_summary_stats(df, 'age')
```

**출력 예시:**
```
==================================================
📊 성별 (sex) 요약 통계
==================================================
전체 데이터 수: 45000
결측값: 0 (0.00%)

[범주형 변수 빈도]

코드       라벨                           빈도        비율(%)    
------------------------------------------------------------
1          남자                           22500       50.00     
2          여자                           22500       50.00     
==================================================
```

---

### Case 6: 그룹별 분석

```python
# 교육수준별 금연 성공률 계산
df_clean = filter_special_codes(df, 'sob_01z1', drop=True)
df_clean['교육수준'] = decode_dataframe(df_clean, 'sob_01z1')

success_rate = df_clean.groupby('교육수준')['churn'].mean() * 100

print("교육수준별 금연 성공률:")
print(success_rate.sort_values(ascending=False))
```

---

### Case 7: 여러 변수 한번에 디코딩

```python
from util.decode_helper import decode_multiple_columns

# 여러 컬럼 동시 디코딩
df_decoded = decode_multiple_columns(
    df, 
    ['sex', 'sob_01z1', 'soa_06z2', 'churn'],
    suffix='_라벨'
)

# 결과 확인
print(df_decoded[['sex', 'sex_라벨', 'sob_01z1', 'sob_01z1_라벨']].head())
```

---

## 🎯 귀하의 분석 주제 적용

### 주제 1: 교육 수준에 따른 흡연율 상관관계

```python
from util.decode_helper import (
    decode_dataframe, 
    filter_special_codes, 
    create_crosstab_with_labels
)

# 1. 데이터 정제
df_clean = filter_special_codes(df, 'sob_01z1', drop=True)

# 2. 라벨 적용
df_clean['교육수준'] = decode_dataframe(df_clean, 'sob_01z1')
df_clean['금연상태'] = decode_dataframe(df_clean, 'churn')

# 3. 교차 분석
ct = df_clean.groupby('교육수준')['churn'].agg(['count', 'mean', 'std'])
ct.columns = ['표본수', '금연성공률', '표준편차']
ct['금연성공률'] = ct['금연성공률'] * 100

print(ct.sort_values('금연성공률', ascending=False))

# 4. 시각화
import seaborn as sns
plt.figure(figsize=(10, 6))
sns.barplot(data=df_clean, x='교육수준', y='churn', ci=95)
plt.ylabel('금연 성공률')
plt.title('교육 수준에 따른 금연 성공률')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
```

---

### 주제 2: 경제활동에 따른 금연 성공 상관관계

```python
# 경제활동 관련 변수들
economic_vars = ['soa_01z1', 'soa_06z2', 'soa_07z1']

# 각 변수별 금연 성공률 분석
for var in economic_vars:
    print(f"\n{'='*50}")
    print(f"{get_label(var)} 분석")
    print('='*50)
    
    df_clean = filter_special_codes(df, var, drop=True)
    df_clean[f'{var}_label'] = decode_dataframe(df_clean, var)
    
    result = df_clean.groupby(f'{var}_label')['churn'].agg(['count', 'mean'])
    result.columns = ['표본수', '금연성공률']
    result['금연성공률'] = result['금연성공률'] * 100
    
    print(result.sort_values('금연성공률', ascending=False))
```

---

## ⚠️ 주의사항

### 1. PDF 확인 필수 변수

일부 변수는 **코드값이 불완전**합니다. 사용 전 확인하세요:

```python
from data.var_mapping import NEEDS_PDF_VERIFICATION

print(f"PDF 확인 필요 변수: {len(NEEDS_PDF_VERIFICATION)}개")
for var in NEEDS_PDF_VERIFICATION[:10]:  # 처음 10개만 출력
    print(f"  - {var}: {get_var_name(var)}")
```

자세한 내용은 `data/PDF_VERIFICATION_NEEDED.md` 참조

---

### 2. 결측값 처리

```python
# 결측값 확인
print(f"결측값 비율: {df['sob_01z1'].isna().mean() * 100:.2f}%")

# 결측값 제외
df_no_na = df[df['sob_01z1'].notna()]
```

---

### 3. 특수코드 처리

특수코드(응답거부, 모름 등)는 분석 전 제거하세요:

```python
# ✅ 권장
df_clean = filter_special_codes(df, 'mta_01z1', drop=True)

# ❌ 비권장 (특수코드 포함된 분석)
df.groupby('mta_01z1').mean()
```

---

## 🔧 트러블슈팅

### 문제 1: import 오류

```python
# 오류: ModuleNotFoundError: No module named 'data'

# 해결: 프로젝트 루트 경로 추가
import sys
sys.path.append('C:/SKN_19/SKN19-2nd-2Team')  # 절대경로
# 또는
sys.path.append('../../')  # 상대경로 (노트북 위치에 따라 조정)
```

---

### 문제 2: 디코딩 결과가 이상함

```python
# 문제: 숫자만 출력됨
# 원인: 변수 코드값이 var_mapping.py에 없음

# 해결 1: 변수 정보 확인
print_var_info('your_variable_code')

# 해결 2: PDF 확인 필요 목록 체크
if 'your_variable_code' in NEEDS_PDF_VERIFICATION:
    print("⚠️ 이 변수는 PDF 확인 필요!")
```

---

## 📚 추가 리소스

- **변수 전체 목록**: `data/var_mapping.py` 참조
- **PDF 확인 필요 변수**: `data/PDF_VERIFICATION_NEEDED.md` 참조
- **유틸 함수 문서**: `util/decode_helper.py` docstring 참조

---

## ✅ 체크리스트

분석 시작 전 확인하세요:

- [ ] `data/var_mapping.py`와 `util/decode_helper.py` 임포트 성공
- [ ] 사용할 변수가 PDF 확인 필요 목록에 있는지 체크
- [ ] 특수코드(응답거부, 모름) 제거 여부 결정
- [ ] 결측값 처리 방법 결정
- [ ] 라벨 적용 방식 선택 (decode_dataframe vs prepare_plot_data)

---

**작성일**: 2025-10-07  
**작성자**: 오흥재 (vfxpedia) + Claude
