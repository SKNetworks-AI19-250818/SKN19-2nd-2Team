# KSH Feature Engineering 분석 문서

**작성자:** vfxpedia  
**분석 대상:** `notebooks/team/modules/features_ksh.py`  
**생성 파생변수:** 6개  
**담당 영역:** 가구/소득/연령/치매

---

## 📋 목차

1. [개요](#개요)
2. [생성된 파생변수](#생성된-파생변수)
3. [변수별 상세 분석](#변수별-상세-분석)
4. [원본 변수 제거 목록](#원본-변수-제거-목록)

---

## 개요

KSH 팀원이 담당한 모듈은 **가구 구조, 소득, 연령, 치매 가족** 관련 변수를 다룹니다.

### 핵심 전략

- 연령대 그룹화 (10년 단위)
- 1인 가구 식별
- 소득 관련 3개 파생변수 생성 (원본, 로그, 그룹)
- 치매 가족 여부 및 동거 여부
- 일평균 흡연량 계산

---

## 생성된 파생변수

| 번호 | 파생변수명 | 원본 변수 | 타입 | 설명 |
|------|-----------|----------|------|------|
| 1 | `age_group` | `age` | 수치 | 연령대 (10년 단위) |
| 2 | `is_single` | `mbhld_co` | 이진 | 1인 가구 여부 (1/0) |
| 3 | `house_income` | `fma_14z1`, `fma_13z1` | 수치 | 월간 가구소득 |
| 4 | `house_income_log` | `house_income` | 수치 | 로그 변환 소득 |
| 5 | `house_income_grp` | `house_income`, `fma_24z2` | 범주 | 소득 그룹 (1-8) |
| 6 | `fma_dementia_case` | `fma_27z1`, `fma_26z1` | 범주 | 치매가족 여부/동거 |

⚠️ 추가: `smoke_avg_per_day` (흡연 관련 변수로 별도 분류)

---

## 변수별 상세 분석

### 1. age_group (연령대)

**목적:** 10년 단위 연령 그룹화로 모델 효율성 향상

```python
def feature_age_group(df_merge):    
    df_merge['age_group'] = (df_merge['age'] // 10) * 10
    return df_merge
```

**전략:**
- 나이를 10으로 나눈 후 다시 10을 곱해 10년 단위로 그룹화
- 예: 35세 → 30, 47세 → 40

**활용:**
- 연령대별 금연 패턴 분석
- 세대별 특성 파악

---

### 2. is_single (1인 가구)

**목적:** 독거 여부가 금연 성공률에 미치는 영향 분석

```python
def feature_is_single(df_merge):    
    df_merge['is_single'] = np.where((df_merge['mbhld_co'] <= 1), 1, 0)
    return df_merge
```

**원본 변수:**
- `mbhld_co`: 가구원 수

**변환 로직:**
- 가구원 수 ≤ 1 → `is_single = 1`
- 가구원 수 > 1 → `is_single = 0`

**가설:**
독거 노인의 경우 사회적 지지 부족으로 금연 성공률이 낮을 것

---

### 3. house_income (월간 가구소득)

**목적:** 경제적 수준이 금연 성공률에 미치는 영향

```python
def feature_house_income(df_merge):
    bins = [0, 50, 100, 200, 300, 400, 500, 600, float('inf')]
    labels = [1, 2, 3, 4, 5, 6, 7, 8]

    df_merge['house_income'] = df_merge['fma_14z1'] 
    df_merge['house_income'] = round(df_merge['house_income'].fillna(df_merge['fma_13z1'] / 12))
    df_merge['house_income_log'] = np.log1p(df_merge['house_income'])
    df_merge['house_income_grp'] = pd.cut(df_merge['house_income'], bins=bins, labels=labels, right=False)
    df_merge['house_income_grp'] = np.where(df_merge['house_income_grp'].isna(), df_merge['fma_24z2'].astype(float), df_merge['house_income_grp'])

    return df_merge
```

**원본 변수:**
- `fma_14z1`: 월간 가구소득 (만원)
- `fma_13z1`: 연간 가구소득 (만원)
- `fma_24z2`: 소득 구간 (1-8)

**변환 로직:**
1. **house_income (원본):**
   - `fma_14z1` 우선 사용
   - 결측 시 `fma_13z1 ÷ 12`로 계산
   - 반올림

2. **house_income_log (로그 변환):**
   - `np.log1p(house_income)`
   - 소득 분포 정규화

3. **house_income_grp (그룹화):**
   - 8개 구간으로 분류 (0-50, 50-100, ..., 600+)
   - 결측 시 `fma_24z2` 값 사용

**활용:**
- 경제 수준별 금연 패턴 비교
- 고소득층 vs 저소득층 성공률 차이

---

### 4. fma_dementia_case (치매 가족)

**목적:** 치매 환자 가족 여부가 스트레스 → 금연 실패에 영향

```python
def get_dementia_case(row):
    if row['fma_27z1'] == 1 and row['fma_26z1'] == 1:
        return 1  # 치매가족 있음 + 같이 거주
    elif row['fma_27z1'] == 1 and row['fma_26z1'] == 2:
        return 2  # 치매가족 있음 + 비거주
    elif row['fma_27z1'] == 2:
        return 3  # 치매가족 없음
    else:
        return np.nan

def feature_dementia_case(df_merge):
    df_merge['fma_dementia_case'] = df_merge.apply(get_dementia_case, axis=1)
    return df_merge
```

**원본 변수:**
- `fma_27z1`: 치매 환자 가족 유무 (1=있음, 2=없음)
- `fma_26z1`: 함께 거주 여부 (1=있음, 2=없음)

**변환 로직:**
- `1`: 치매 가족 있음 + 동거
- `2`: 치매 가족 있음 + 비동거
- `3`: 치매 가족 없음
- `NaN`: 무응답

**가설:**
치매 환자를 돌보는 가족의 스트레스가 금연 실패로 이어질 가능성

---

### 5. smoke_avg_per_day (일평균 흡연량)

**목적:** 흡연량이 금연 성공률에 미치는 영향

```python
def feature_smoke_avg_per_day(df_merge):
    df_merge['smoke_avg_per_day'] = df_merge.apply(
        lambda x: x[['smb_01z1', 'smb_03z1', 'smb_06z1']].max(skipna=True), 
        axis=1
    )
    return df_merge
```

**원본 변수:**
- `smb_01z1`: 흡연량 1
- `smb_03z1`: 흡연량 2
- `smb_06z1`: 흡연량 3

**변환 로직:**
3개 컬럼의 최댓값 → 일평균 흡연량

⚠️ **참고:** 흡연 관련 변수로 별도 분류 필요

---

## 원본 변수 제거 목록

**제거 대상 (7개):**

```python
['fma_13z1', 'fma_14z1', 'fma_27z1', 'fma_26z1', 'smb_01z1', 'smb_03z1', 'smb_06z1']
```

**제거 이유:**
- `fma_13z1`, `fma_14z1` → `house_income` 3개 파생변수로 대체
- `fma_27z1`, `fma_26z1` → `fma_dementia_case`로 통합
- `smb_01z1`, `smb_03z1`, `smb_06z1` → `smoke_avg_per_day`로 통합

---

## 모델 학습 활용 방안

### 1. age_group

```python
# 연령대별 성공률 분석
df.groupby('age_group')['churn'].mean()
```

### 2. is_single

```python
# 1인 가구 vs 다인 가구
df.groupby('is_single')['churn'].mean()
```

### 3. house_income_grp

```python
# 소득 구간별 성공률
df.groupby('house_income_grp')['churn'].mean()

# 로그 변환 소득 활용
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
df['house_income_log_scaled'] = scaler.fit_transform(df[['house_income_log']])
```

### 4. fma_dementia_case

```python
# 치매 가족 유무별 성공률
df.groupby('fma_dementia_case')['churn'].mean()
```

---

## 참고사항

1. **결측치 처리:**
   - 소득: 연간 → 월간 변환으로 대체
   - 치매: `NaN` 유지 (무응답)

2. **상호작용 분석 가능:**
   - `age_group` × `house_income_grp`
   - `is_single` × `fma_dementia_case`

3. **불균형 확인 필요:**
   - `fma_dementia_case`: 치매 가족 있는 경우가 소수일 가능성

---

**작성 완료:** 2025-10-14  
**버전:** 1.0

