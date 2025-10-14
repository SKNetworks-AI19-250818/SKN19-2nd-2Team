# PDY Feature Engineering 분석 문서

**작성자:** vfxpedia  
**분석 대상:** `notebooks/team/modules/features_pdy.py`  
**생성 파생변수:** 2개  
**담당 영역:** 체중조절/신체활동

---

## 📋 목차

1. [개요](#개요)
2. [생성된 파생변수](#생성된-파생변수)
3. [변수별 상세 분석](#변수별-상세-분석)

---

## 개요

PDY 팀원이 담당한 모듈은 **체중조절 방법**과 **신체활동 점수** 관련 변수를 다룹니다.

### 핵심 전략

- 체중조절 방법 3가지 조합
- 신체활동 강도별 가중치 적용
- 활동 점수 기반 4단계 분류

---

## 생성된 파생변수

| 번호 | 파생변수명 | 원본 변수 | 타입 | 설명 |
|------|-----------|----------|------|------|
| 1 | `weight_control_method` | `obb_02a1`, `obb_02b1`, `obb_02d1` | 문자열 | 체중조절 방법 조합 |
| 2 | `activity_score_weight` | `pha_04z1`, `pha_06z1`, `phb_01z1` | 수치 | 가중 활동 점수 |
| 2-1 | `activity_score` | `activity_score_weight` | 범주 | 활동 수준 (4단계) |

⚠️ 추가: `Liquid_method1`, `Liquid_method2` (액상형 담배 로직, 흡연 관련으로 별도 분류)

---

## 변수별 상세 분석

### 1. weight_control_method (체중조절 방법)

**목적:** 체중조절 방법이 건강 의식 → 금연 성공률에 영향

```python
def feature_weight_control_method(df_merge):
    cols = ['obb_02a1', 'obb_02b1', 'obb_02d1']
    # ["체중조절방법_운동", "체중조절방법_단식", "체중조절방법_무처방약물"]

    # NaN을 '비응답'으로 대체하고, 세 칼럼을 조합한 문자열 생성
    df_merge["weight_control_method"] = (
        df_merge[cols]
        .fillna("no_response")          # NaN → '비응답'
        .astype(str)                    # 숫자를 문자열로 변환
        .agg("-".join, axis=1)          # 3개 값을 '-'로 연결
    )

    return df_merge
```

**원본 변수:**
- `obb_02a1`: 체중조절방법 - 운동 (1=예, 2=아니오)
- `obb_02b1`: 체중조절방법 - 단식 (1=예, 2=아니오)
- `obb_02d1`: 체중조절방법 - 무처방약물 (1=예, 2=아니오)

**변환 로직:**
- 3개 값을 "-"로 연결
- 예: `"1-2-1"` → 운동+약물, 단식 X
- 결측 → `"no_response"`

**가능한 조합 예시:**
- `"1-1-1"`: 운동 + 단식 + 약물 (위험한 방법)
- `"1-2-2"`: 운동만 (건강한 방법)
- `"2-1-2"`: 단식만 (건강하지 않음)

**가설:**
건강한 체중조절 방법(운동)을 사용하는 사람이 금연 성공률 높음

---

### 2. activity_score (신체활동 점수)

**목적:** 신체활동 수준이 건강 의식 → 금연 성공률에 영향

```python
def feature_activity_score_and_weight(df_merge):

    df_merge["activity_score_weight"] = (
        3 * df_merge["pha_04z1"].fillna(0) +
        2 * df_merge["pha_06z1"].fillna(0) +
        1 * df_merge["phb_01z1"].fillna(0)
    )
    # 고강도, 중강도, 걷기 활동
    
    def activity_level(x):
        if x >= 10:
            return "high_activity"
        elif x >= 5:
            return "normal_activity"
        elif x >= 1:
            return "row_activity"
        else:
            return "no_activity"

    df_merge["activity_score"] = df_merge["activity_score_weight"].apply(activity_level)

    return df_merge
```

**원본 변수:**
- `pha_04z1`: 고강도 신체활동 (일수)
- `pha_06z1`: 중강도 신체활동 (일수)
- `phb_01z1`: 걷기 활동 (일수)

**변환 로직:**

1. **activity_score_weight (가중 점수):**
   ```
   점수 = 3 × 고강도 + 2 × 중강도 + 1 × 걷기
   ```
   - 고강도에 가장 높은 가중치 부여

2. **activity_score (범주화):**
   - `≥ 10`: `"high_activity"` (고활동)
   - `5-9`: `"normal_activity"` (보통)
   - `1-4`: `"row_activity"` (저활동)
   - `0`: `"no_activity"` (무활동)

**가설:**
신체활동이 많은 사람이 건강 의식 높음 → 금연 성공률 높음

**예시:**
- 고강도 3일 + 중강도 2일 + 걷기 1일:
  ```
  점수 = 3×3 + 2×2 + 1×1 = 14
  → "high_activity"
  ```

---

## 흡연 관련 함수 (별도 분류)

⚠️ **Liquid_method1, Liquid_method2는 흡연 변수 전처리 함수이므로 파생변수 개수에서 제외**

### Liquid_method2 (사용 중)

**목적:** 액상형 담배 흡연자의 churn 재정의

```python
def Liquid_method2(df_merge):
    # 9 모름 -> 2 아니오로 처리
    df_merge.loc[df_merge["sma_08z1"] == 9, 'sma_08z1'] = 2.0
    df_merge.loc[(df_merge['sma_08z1'] == 1) & (df_merge['sma_11z2'] != 0) & (df_merge['churn'] == 1), 'churn'] = 0
    return df_merge
```

**로직:**
- 액상형 흡연 경험 있음 + 최근 1개월 흡연 일수 > 0 + churn = 1
  → **churn = 0으로 변경** (실질적 금연 실패)

---

## 모델 학습 활용 방안

### 1. weight_control_method

```python
# 체중조절 방법별 성공률
df.groupby('weight_control_method')['churn'].mean()

# 빈도 분석
df['weight_control_method'].value_counts()
```

### 2. activity_score

```python
# 활동 수준별 성공률
df.groupby('activity_score')['churn'].mean()

# 순서: no < row < normal < high 활동
```

---

## 참고사항

1. **가중치 기준:**
   - 고강도: 3점
   - 중강도: 2점
   - 걷기: 1점

2. **범주 분류 기준:**
   - 10점 이상: 고활동
   - 5-9점: 보통
   - 1-4점: 저활동
   - 0점: 무활동

3. **상호작용 분석:**
   - `activity_score` × `weight_control_method`
   - 건강한 생활습관 조합이 금연 성공률에 미치는 영향

---

**작성 완료:** 2025-10-14  
**버전:** 1.0

