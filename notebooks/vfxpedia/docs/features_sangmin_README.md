# Sangmin Feature Engineering 분석 문서

**작성자:** vfxpedia  
**분석 대상:** `notebooks/team/modules/features_sangmin.py`  
**생성 파생변수:** 16개  
**담당 영역:** 식생활/비만/체중조절/구강

---

## 📋 목차

1. [개요](#개요)
2. [생성된 파생변수](#생성된-파생변수)
3. [카테고리별 상세 분석](#카테고리별-상세-분석)
4. [원본 변수 제거 목록](#원본-변수-제거-목록)

---

## 개요

Sangmin 팀원의 `apply_my_features` 함수는 **식생활, 비만/체중조절, 구강건강** 3개 카테고리를 통합 처리합니다.

### 핵심 전략

- **식생활:** 아침식사 빈도, 영양표시 인지/활용/관심
- **비만/체중:** BMI, 체형 인지, 체중조절 방법
- **구강:** 양치 습관, 치과 방문 장벽, 주관적 구강건강

---

## 생성된 파생변수

### 📊 식생활 (5개)

| 번호 | 파생변수명 | 원본 변수 | 타입 | 설명 |
|------|-----------|----------|------|------|
| 1 | `breakfast_freq_cat` | `nua_01z2` | Ordered | 아침식사 빈도 (4단계) |
| 2 | `breakfast_freq_score` | `nua_01z2` | 수치 | 아침식사 점수 (0-3) |
| 3 | `nutrition_awareness_bin` | `nuc_02z1` | 이진 | 영양표시 인지 (1/0) |
| 4 | `nutrition_usage_bin` | `nuc_01z2` | 이진 | 영양표시 활용 (1/0) |
| 5 | `nutrition_interest_bin` | `nuc_03z1` | 이진 | 영양표시 관심 (1/0) |

### 📊 비만/체중조절 (5개)

| 번호 | 파생변수명 | 원본 변수 | 타입 | 설명 |
|------|-----------|----------|------|------|
| 6 | `height_m` | `oba_02z1` | 수치 | 신장 (cm → m) |
| 7 | `oba_bmi` | `oba_bmi` or 계산 | 수치 | BMI (체중/신장²) |
| 8 | `body_perception_cat` | `oba_01z1` | Ordered | 체형 인지 (5단계) |
| 9 | `weight_control_attempt_cat` | `obb_01z1` | Ordered | 체중조절 시도 (4단계) |
| 10 | `healthy_method_ratio` | `obb_02a1`, `obb_02b1` | 수치 | 건강한 방법 비율 |

### 📊 구강 (6개)

| 번호 | 파생변수명 | 원본 변수 | 타입 | 설명 |
|------|-----------|----------|------|------|
| 11 | `dental_visit_barrier_cat` | `ore_03z2` | Ordered | 치과 방문 장벽 (8단계) |
| 12 | `brush_after_lunch_cat` | `ord_01d2` | Ordered | 점심 후 양치 (3단계) |
| 13 | `brush_after_lunch_bin` | `ord_01d2` | 이진 | 점심 후 양치 (1/0) |
| 14 | `brush_impossible_evening_cat` | `ord_01f3` | Ordered | 저녁 양치 불가 (3단계) |
| 15 | `oral_hygiene_barrier_cat` | `ord_05z1` | Ordered | 구강관리 장벽 (4단계) |
| 16 | `subjective_oral_health_cat` | `ora_01z1` | Ordered | 주관적 구강건강 (5단계) |

---

## 카테고리별 상세 분석

### 📌 1. 식생활 (Diet)

#### breakfast_freq (아침식사 빈도)

**목적:** 아침식사 습관이 건강 의식 → 금연 성공률에 영향

**변환 로직:**

```python
# 1) 카테고리
map_lbl = {1: "주5~7회", 2: "주3~4회", 3: "주1~2회", 4: "거의안함"}
df["breakfast_freq_cat"] = df["nua_01z2"].map(map_lbl)

# 2) 점수 (높을수록 바람직)
df["breakfast_freq_score"] = df["nua_01z2"].replace({1: 3, 2: 2, 3: 1, 4: 0})
df["breakfast_freq_score"] = df["breakfast_freq_score"].fillna(df["breakfast_freq_score"].median())
```

**활용:**
- 규칙적 식사 습관이 금연 성공률에 긍정적 영향 예상

#### nutrition (영양표시 관련 3개)

**목적:** 건강 의식 수준 측정

**변환 로직:**

```python
_BIN_YN = {1: 1, 2: 0}  # 예/아니오 → 1/0

for raw, out in {
    "nuc_02z1": "nutrition_awareness_bin",
    "nuc_01z2": "nutrition_usage_bin",
    "nuc_03z1": "nutrition_interest_bin",
}.items():
    df[out] = df[raw].map(_BIN_YN)
    df[out] = _fill_mode(df[out])  # 최빈값으로 대체
```

**활용:**
- 3개 변수 합산 → 영양 의식 종합 점수 생성 가능

---

### 📌 2. 비만/체중조절 (Obesity & Weight Control)

#### BMI 계산 및 처리

**목적:** 비만도가 금연 성공률에 미치는 영향

**변환 로직:**

```python
# 신장 cm → m 변환
df["height_m"] = df["oba_02z1"] / 100

# BMI 계산 (체중 있을 경우)
bmi = weight / (height ** 2)
df["oba_bmi"] = bmi.fillna(df["oba_bmi"].median())
```

#### body_perception_cat (체형 인지)

**원본 값:**
- 1: 매우마름
- 2: 약간마름
- 3: 보통
- 4: 약간비만
- 5: 매우비만

**활용:**
실제 BMI vs 주관적 체형 인지 차이 분석

#### healthy_method_ratio (건강한 방법 비율)

**목적:** 건강한 체중조절 방법 사용 비율

**변환 로직:**

```python
# 운동(obb_02a1) + 식이(obb_02b1)를 건강한 방법으로 정의
healthy = [x for x in exist if x.startswith("obb_02a1") or x.startswith("obb_02b1")]
df["healthy_method_ratio"] = df[healthy].sum(axis=1) / len(healthy)
```

**해석:**
- 0: 건강한 방법 사용 X
- 0.5: 1개만 사용
- 1.0: 2개 모두 사용

---

### 📌 3. 구강 (Oral Hygiene)

#### dental_visit_barrier_cat (치과 방문 장벽)

**원본 값 (ore_03z2):**
1. 시간없음
2. 증상경미
3. 경제적이유
4. 교통/거리
5. 대기시간
6. 신체/예약어려움
7. 치료두려움
8. 기타

**가설:**
치과 방문 장벽이 높음 → 건강 관리 소홀 → 금연 실패

#### brush_after_lunch (점심 후 양치)

**변환:**
- `brush_after_lunch_cat`: 3단계 ("예", "아니요", "점심식사안함")
- `brush_after_lunch_bin`: 이진 (1=예, 0=아니오/안함)

**가설:**
규칙적 양치 습관 → 건강 의식 높음 → 금연 성공률 높음

---

## 원본 변수 제거 목록

**제거 대상 (19개):**

```python
[
    'nua_01z2',  # breakfast_freq로 대체
    'oba_02z1',  # height_m으로 대체
    'oba_01z1',  # body_perception_cat으로 대체
    'obb_01z1',  # weight_control_attempt_cat으로 대체
    'obb_02a1', 'obb_02b1', 'obb_02c1', 'obb_02d1',  # 체중조절 방법 (9개)
    'obb_02e1', 'obb_02f1', 'obb_02g1', 'obb_02h1', 'obb_02i1',
    'ore_03z2',  # dental_visit_barrier_cat으로 대체
    'ord_01d2',  # brush_after_lunch로 대체
    'ord_01f3',  # brush_impossible_evening_cat으로 대체
    'ord_05z1',  # oral_hygiene_barrier_cat으로 대체
    'ora_01z1',  # subjective_oral_health_cat으로 대체
    'orb_01z1'   # dental_discomfort_cat으로 대체
]
```

---

## 모델 학습 활용 방안

### 1. 식생활 변수

```python
# 아침식사 빈도 vs 금연 성공률
df.groupby('breakfast_freq_cat')['churn'].mean()

# 영양 의식 종합 점수
df['nutrition_total'] = df['nutrition_awareness_bin'] + df['nutrition_usage_bin'] + df['nutrition_interest_bin']
```

### 2. 비만/체중 변수

```python
# BMI vs 금연 성공률 상관관계
df[['oba_bmi', 'churn']].corr()

# 건강한 체중조절 방법 vs 성공률
df.groupby('healthy_method_ratio')['churn'].mean()
```

### 3. 구강 변수

```python
# 양치 습관 vs 성공률
df.groupby('brush_after_lunch_bin')['churn'].mean()

# 구강건강 인지 vs 성공률
df.groupby('subjective_oral_health_cat')['churn'].mean()
```

---

## 참고사항

1. **결측치 처리 방식:**
   - 수치형: `median()`
   - 이진형: `mode()` (최빈값) 또는 0
   - 범주형: `"Unknown"` 카테고리 추가

2. **Ordered Categorical:**
   - `pd.Categorical(... , ordered=True)` 사용
   - 순서 의미 있는 변수 처리

3. **활용 코드:**

```python
from notebooks.team.modules.features_sangmin import apply_my_features

# 파생변수 생성
df = apply_my_features(
    df,
    weight_col='체중컬럼명',  # 필요 시
    copy=True,
    keep_original=True  # False면 원본 제거
)
```

---

**작성 완료:** 2025-10-14  
**버전:** 1.0

