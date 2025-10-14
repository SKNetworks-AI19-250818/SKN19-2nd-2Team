# 📊 비경제활동인구 변수 처리 가이드

**작성자**: 오흥재 (vfxpedia)  
**작성일**: 2025-10-08  
**목적**: 팀원들이 경제활동 상태 변수를 쉽게 이해하고 사용할 수 있도록 안내

---

## 🎯 핵심 요약

### ⭐ 중요한 사실

**`soa_06z2 == 88`은 "비경제활동인구"를 의미합니다.**

- 전체 데이터의 약 **35.6%**를 차지하는 중요한 그룹
- **응답거부나 결측값이 아닌, 정상적인 분석 대상**
- 학생, 주부, 은퇴자 등이 포함됨

---

## 📋 변수 설명

### 원본 변수: `soa_06z2` (직업분류)

```python
# 코드 매핑
1~11  : 실제 직업 (관리자, 전문가, 사무종사자 등)
77    : 응답거부 ❌ (제거 대상)
88    : 비경제활동인구 ✅ (유지 대상)
99    : 모름 ❌ (제거 대상)
```

### 문제점

팀원들이 코드를 볼 때:
```python
# ❌ 이해하기 어려운 코드
non_econ_count = (df['soa_06z2'] == 88).sum()
```

**"88이 뭐지? 왜 88인가?"** → 문서를 찾아봐야 함 😥

---

## ✅ 해결 방법: Feature Engineering

### 1. 명확한 변수 생성

```python
from utils.data_cleaning import add_economic_status_features

# Feature 생성
df = add_economic_status_features(df)
```

**생성되는 3개 변수:**

| 변수명 | 타입 | 설명 | 예시값 |
|--------|------|------|--------|
| `is_economically_inactive` | int | 비경제활동인구 여부 | 0 또는 1 |
| `is_economically_active` | int | 경제활동인구 여부 | 0 또는 1 |
| `economic_status` | str | 경제활동 상태 레이블 | "비경제활동인구" 또는 "경제활동인구" |

---

## 💡 사용 예시

### Before (이해하기 어려움 ❌)

```python
# 팀원: "88이 뭔지 모르겠어요..."
non_econ_df = df[df['soa_06z2'] == 88]
non_econ_rate = (df['soa_06z2'] == 88).sum() / len(df)
```

### After (명확함 ✅)

```python
from utils.data_cleaning import add_economic_status_features

# 1. Feature 생성
df = add_economic_status_features(df, verbose=True)

# 2. 비경제활동인구만 필터링 (코드만 봐도 의미 명확!)
inactive_df = df[df['is_economically_inactive'] == 1]

# 3. 경제활동인구만 필터링
active_df = df[df['is_economically_active'] == 1]

# 4. 그룹별 금연 성공률 비교 (가독성 좋음!)
success_by_status = df.groupby('economic_status')['churn'].mean()
print(success_by_status)
# 출력:
# 경제활동인구      0.5234
# 비경제활동인구    0.5892
```

---

## 📊 실제 분석 예시

### 1. 기본 통계

```python
from utils.data_cleaning import get_economic_status_summary

# 경제활동 상태별 요약 통계
summary = get_economic_status_summary(df)
print(summary)
```

**출력 예시:**
```
                    샘플수  금연성공률  표준편차  금연성공률(%)
economic_status                                      
경제활동인구       57,784      0.52    0.50         52.34
비경제활동인구     31,973      0.59    0.49         58.92
```

### 2. 시각화

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 경제활동 상태별 금연 성공률 비교
plt.figure(figsize=(10, 6))
sns.barplot(data=df, x='economic_status', y='churn')
plt.title('경제활동 상태에 따른 금연 성공률')
plt.ylabel('금연 성공률')
plt.xlabel('경제활동 상태')
plt.show()
```

### 3. 통계 검정

```python
from scipy.stats import chi2_contingency

# 경제활동 상태와 금연 성공의 연관성 검정
contingency_table = pd.crosstab(
    df['economic_status'], 
    df['churn']
)
chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"Chi-square: {chi2:.4f}")
print(f"P-value: {p_value:.4f}")
```

---

## 🔍 변수 정보 확인하기

코드 의미가 헷갈릴 때:

```python
from utils.data_cleaning import print_economic_code_info

# soa_06z2 변수 설명 출력
print_economic_code_info('soa_06z2')
```

**출력:**
```
================================================================================
📊 soa_06z2 - 직업분류
================================================================================

설명: 현재 직업 (표준직업분류 대분류)

특수 코드:
     77: 응답거부
  ⭐ 88: 비경제활동인구
     99: 모름

💡 Note: 88(비경제활동인구)은 정상값으로 유지합니다. 약 35.6%를 차지하는 의미있는 그룹입니다.
================================================================================
```

---

## 🎓 왜 이렇게 하는가?

### 장점

1. **가독성 향상** 📖
   - `df['is_economically_inactive'] == 1` ← 코드만 봐도 의미 파악
   - `df['soa_06z2'] == 88` ← 문서를 찾아봐야 함

2. **유지보수 용이** 🔧
   - 변수 의미가 코드에 명시되어 있음
   - 나중에 다시 봐도 이해하기 쉬움

3. **협업 효율** 👥
   - 팀원들이 질문할 필요 없음
   - 일관된 변수명 사용으로 혼란 방지

4. **분석 품질** 📈
   - 명확한 변수로 실수 방지
   - 비즈니스 의미가 코드에 반영됨

---

## 📝 정리

### ✅ 권장 사항

```python
# 노트북 시작 부분에 항상 추가
from utils.data_cleaning import (
    add_economic_status_features,
    get_economic_status_summary,
    print_economic_code_info
)

# 데이터 로드 후 바로 Feature 생성
df = pd.read_csv('../../data/analy_data.csv')
df = add_economic_status_features(df, verbose=True)

# 이제 명확한 변수로 분석!
```

### ❌ 비권장

```python
# 직접 코드 값으로 필터링 (의미 불명확)
df_inactive = df[df['soa_06z2'] == 88]  # 88이 뭔지 모름
```

---

## 📚 관련 문서

- [데이터 정제 전략](../03_data_cleaning_strategy.ipynb)
- [최종 정제 코드](../04_data_cleaning_final.ipynb)
- [교육/경제 분석](../05_analysis_education_economy.ipynb)
- [전체 사용 가이드](USAGE_GUIDE.md)

---

## 🙋‍♂️ 질문이 있다면?

**오흥재 (vfxpedia)**에게 문의해주세요!

