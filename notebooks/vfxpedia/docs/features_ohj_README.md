# 📊 Feature Engineering 문서 - features_ohj.py

**작성자:** OHJ (vfxpedia)  
**작성일:** 2025-10-14  
**담당 원본 변수:** 교육 및 경제활동 관련 (sob_01z1, soa_01z1, soa_06z2, soa_07z1, sod_02z3)

---

## 📋 목차

1. [개요](#1-개요)
2. [생성된 파생변수](#2-생성된-파생변수)
3. [각 Feature 상세 설명](#3-각-feature-상세-설명)
4. [주요 인사이트](#4-주요-인사이트)
5. [모델 학습 시 주의사항](#5-모델-학습-시-주의사항)

---

## 1. 개요

### 🎯 목적
- 원본 변수의 복잡한 카테고리를 **의미 있는 그룹으로 단순화**
- **금연 성공률과의 관계**를 기반으로 예측력 높은 feature 생성
- 모델 학습 효율성 향상 (카테고리 수 감소, 불균형 완화)

### 📊 데이터 규모
- **전체 데이터:** 89,822명
- **타겟 변수 (churn):** 금연 성공 여부
  - 0 (실패): 40,571명 (45.2%)
  - 1 (성공): 49,251명 (54.8%)
  - 전체 금연 성공률: **54.8%**

---

## 2. 생성된 파생변수

### 📋 최종 Feature 목록 (5개)

| Feature | 원본 변수 | 타입 | 카테고리 | 불균형 | 성공률 차이 |
|---------|----------|------|---------|--------|------------|
| `education_group` | sob_01z1 (10개) | int | 3개 | 51.62:1 ❌ | 17.0%p |
| `is_economically_active` | soa_01z1 (4개) | int | 2개 | 2.59:1 ✅ | 13.7%p |
| `occupation_type` | soa_06z2 (13개) | str | 3개 | 2.50:1 ✅ | 14.6%p |
| `is_employee` | soa_07z1 (6개) | int | 2개 | 2.59:1 ✅ | 13.7%p |
| `marital_stability` | sod_02z3 (7개) | str | 3개 | 18.72:1 ⚠️ | 21.9%p |

**변경 이력:**
- ~~`is_married`~~ → 제거 (`marital_stability`가 더 디테일)
- ~~`job_risk_group`~~ → `occupation_type`으로 통합

---

## 3. 각 Feature 상세 설명

### 3-1. education_group (교육수준 그룹)

#### 📌 생성 로직
```python
def feature_education_group(df_merge):
    """
    교육수준을 3그룹으로 분류
    - 0: 저학력 (무학/초졸/중졸) ← sob_01z1 <= 2
    - 1: 중학력 (고졸) ← sob_01z1 == 3
    - 2: 고학력 (대졸 이상) ← sob_01z1 >= 4
    """
    conditions = [
        df_merge['sob_01z1'] <= 2,
        df_merge['sob_01z1'] == 3,
        df_merge['sob_01z1'] >= 4
    ]
    choices = [0, 1, 2]
    df_merge['education_group'] = np.select(conditions, choices, default=np.nan)
    return df_merge
```

#### 📊 분석 결과

| 그룹 | 인원 | 비율 | 금연성공률 | 전체 평균 대비 |
|------|------|------|-----------|--------------|
| **저학력 (0)** | 1,519명 | 1.7% | **69.65%** | +14.85%p |
| **중학력 (1)** | 9,897명 | 11.0% | **70.00%** | +15.20%p |
| **고학력 (2)** | 78,406명 | 87.3% | **52.63%** | -2.17%p |

**🔍 왜 만들었나?**
- **원본 문제:** sob_01z1은 10개 카테고리로 과도하게 세분화
- **패턴 발견:** EDA 06번에서 "역U자 패턴" 확인
  - 저학력/중학력: 69~70% (높음)
  - 고학력: 52.63% (낮음)
- **해결:** 교육수준을 사회학적 의미 단위인 3그룹으로 통합

**⚠️ 주의사항:**
- 불균형 비율: **51.62:1** (위험)
- 고학력 87.3% 집중 → **class_weight 조정 필수**

---

### 3-2. is_economically_active (경제활동 여부)

#### 📌 생성 로직
```python
def feature_is_economically_active(df_merge):
    """
    경제활동 여부 (0/1)
    - 1: 경제활동 (취업자) ← soa_01z1 == 1
    - 0: 비경제활동 ← soa_01z1 != 1
    """
    df_merge['is_economically_active'] = np.where(
        df_merge['soa_01z1'] == 1, 1, 0
    )
    return df_merge
```

#### 📊 분석 결과

| 그룹 | 인원 | 비율 | 금연성공률 | 전체 평균 대비 |
|------|------|------|-----------|--------------|
| **비경제활동 (0)** | 24,999명 | 27.8% | **64.74%** | +9.94%p |
| **경제활동 (1)** | 64,823명 | 72.2% | **51.01%** | -3.79%p |

**🔍 왜 만들었나?**
- **가설:** 직장/업무 스트레스가 금연 실패에 영향
- **검증:** 경제활동 중인 사람이 **13.7%p 낮은 성공률**
- **활용:** 핵심 예측 변수 중 하나

**✅ 장점:**
- 불균형 비율: **2.59:1** (양호)
- 명확한 성공률 차이

---

### 3-3. occupation_type (직업 유형)

#### 📌 생성 로직
```python
def feature_occupation_type(df_merge):
    """
    직업을 3가지 유형으로 분류
    - white_color: 관리자, 전문가, 사무직 ← soa_06z2 in [1,2,3]
    - blue_color: 서비스, 판매, 농림어업, 기능원, 장치조작, 단순노무, 군인 ← 기타
    - inactive: 미취업자 ← soa_06z2 == 88
    """
    conditions = [
        df_merge['soa_06z2'].isin([1, 2, 3]),
        df_merge['soa_06z2'] == 88
    ]
    choices = ['white_color', 'inactive']
    df_merge['occupation_type'] = np.select(conditions, choices, default='blue_color')
    return df_merge
```

#### 📊 분석 결과

| 그룹 | 인원 | 비율 | 금연성공률 | 전체 평균 대비 |
|------|------|------|-----------|--------------|
| **inactive** | 24,995명 | 27.8% | **64.74%** | +9.94%p |
| **white_color** | 18,521명 | 20.6% | **53.17%** | -1.63%p |
| **blue_color** | 46,306명 | 51.6% | **50.15%** | -4.65%p |

**🔍 왜 만들었나?**
- **가설:** 화이트칼라(정신노동) vs 블루칼라(육체노동) 생활 패턴 차이
- **불균형 해소:** 군인 404명 + 무응답 13명 → blue_color 통합
- **활용:** `is_economically_active`의 보조 변수

**✅ 장점:**
- 불균형 비율: **2.50:1** (양호)
- 직업 환경별 금연 성공률 패턴 명확

---

### 3-4. is_employee (임금근로자 여부)

#### 📌 생성 로직
```python
def feature_is_employee(df_merge):
    """
    임금근로자 여부 (0/1)
    - 1: 임금근로자 (상용직, 임시직, 일용직) ← soa_07z1 in [1,2,3]
    - 0: 비임금근로자 (자영업자, 고용주, 무급가족종사자) ← 기타
    """
    df_merge['is_employee'] = np.where(
        df_merge['soa_07z1'].isin([1, 2, 3]), 1, 0
    )
    return df_merge
```

#### 📊 분석 결과

| 그룹 | 인원 | 비율 | 금연성공률 | 전체 평균 대비 |
|------|------|------|-----------|--------------|
| **비임금근로자 (0)** | 25,008명 | 27.8% | **64.73%** | +9.93%p |
| **임금근로자 (1)** | 64,814명 | 72.2% | **51.01%** | -3.79%p |

**🔍 왜 만들었나?**
- **가설:** 고용 형태(임금 vs 자영)에 따른 근로 환경 차이
- **검증:** 임금근로자가 **13.7%p 낮은 성공률**
- **활용:** `occupation_type`의 추가 세부 분류

**💡 인사이트:**
- 임금근로자: 직장 스트레스, 회식 문화, 규칙적 흡연 패턴
- 비임금근로자: 시간 자율성, 자기 관리 용이

---

### 3-5. marital_stability (혼인 안정성)

#### 📌 생성 로직
```python
def feature_marital_stability(df_merge):
    """
    혼인 상태를 안정성 기준으로 분류
    - stable: 유배우 ← sod_02z3 == 1
    - single: 미혼 ← sod_02z3 == 2
    - unstable: 사별, 이혼, 별거, 무응답 ← 기타
    """
    conditions = [
        df_merge['sod_02z3'] == 1,
        df_merge['sod_02z3'] == 2
    ]
    choices = ['stable', 'single']
    df_merge['marital_stability'] = np.select(conditions, choices, default='unstable')
    return df_merge
```

#### 📊 분석 결과

| 그룹 | 인원 | 비율 | 금연성공률 | 전체 평균 대비 |
|------|------|------|-----------|--------------|
| **stable (안정)** | 59,608명 | 66.4% | **61.76%** | +6.96%p |
| **single (미혼)** | 3,184명 | 3.5% | **51.85%** | -2.95%p |
| **unstable (불안정)** | 27,030명 | 30.1% | **39.90%** | -14.90%p |

**🔍 왜 만들었나?**
- **가설:** 배우자의 사회적 지지가 금연 성공에 영향
- **심화 분석:** is_married(단순 유/무)보다 **디테일한 3그룹 분류**
- **불균형 해소:** 무응답 17명 → unstable 통합 (3506:1 → 18.7:1)

**💡 핵심 패턴:**
```
안정 (61.76%) > 미혼 (51.85%) > 불안정 (39.90%)
```
- **21.9%p 차이** (안정 vs 불안정)
- 배우자 이별(사별/이혼/별거) → 정서적 불안 → 금연 실패

**⚠️ 주의사항:**
- 불균형 비율: **18.72:1** (주의)
- `is_married` 대비 장점: 미혼/불안정 구분 → 더 정교한 예측

---

## 4. 주요 인사이트

### 🔬 2-Way 상호작용 분석

#### education_group × is_economically_active

| 교육수준 | 비경제활동 | 경제활동 | 차이 |
|---------|-----------|---------|------|
| **저학력 (0)** | **70.12%** | 68.76% | -1.4%p |
| **중학력 (1)** | **70.76%** | 69.30% | -1.5%p |
| **고학력 (2)** | 62.97% | **49.27%** ⚠️ | **-13.7%p** |

**💡 핵심 발견:**

1. **고학력 × 경제활동 중 = 49.27% (전체 최저)**
   - 가설: 직장 스트레스, 회식 문화, 바쁜 일상
   - 고위험군 식별 → 맞춤형 금연 프로그램 필요

2. **저/중학력 × 비경제활동 = 70%+ (전체 최고)**
   - 가설: 시간적 여유, 생활 패턴 안정성
   - 금연 성공 가능성 높음

3. **상호작용 효과 존재**
   - 교육수준**만**으로는 정확한 예측 불가
   - 경제활동 여부와 **결합** 시 명확한 패턴

→ **Tree 기반 모델이 자동으로 학습 가능**

---

### 🔗 Feature 간 계층 구조

```
경제활동 관련 Feature (계층적 관계)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1차 분류: is_economically_active
           ↓
2차 분류: occupation_type (white_color/blue_color/inactive)
           ↓
3차 분류: is_employee (임금/비임금)

혼인 관련 Feature (독립적)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
marital_stability (stable/single/unstable)
```

**서로 보완적이지만 중복 아님** (다른 관점의 분류)

---

### 📈 금연 성공률 영향 요인 순위

| 순위 | Feature | 성공률 차이 | 영향 |
|------|---------|-----------|------|
| 1위 | `marital_stability` | **21.9%p** | 안정 vs 불안정 |
| 2위 | `education_group` | **17.0%p** | 저/중 vs 고 |
| 3위 | `occupation_type` | **14.6%p** | inactive vs blue_color |
| 4위 | `is_economically_active` | **13.7%p** | 비경제 vs 경제 |
| 5위 | `is_employee` | **13.7%p** | 비임금 vs 임금 |

---

## 5. 모델 학습 시 주의사항

### ✅ 원본 변수 제거 (필수)

**반드시 제거해야 할 원본 변수:**
```python
drop_features = [
    'sob_01z1',  # → education_group로 대체
    'soa_01z1',  # → is_economically_active로 대체
    'soa_06z2',  # → occupation_type로 대체
    'soa_07z1',  # → is_employee로 대체
    'sod_02z3',  # → marital_stability로 대체
]

# 모델 학습 전
X = df.drop(drop_features + ['churn'], axis=1)
y = df['churn']
```

**이유:**
- ❌ 원본 + 파생 동시 사용 시 **정보 중복 (Multicollinearity)**
- ❌ Feature Importance 분산, 해석력 저하
- ❌ Overfitting 위험 증가

---

### ⚠️ 불균형 처리 방안

#### 문제가 있는 Feature

| Feature | 불균형 비율 | 상태 | 권장 조치 |
|---------|------------|------|----------|
| `education_group` | 51.62:1 | ❌ 위험 | **class_weight** 또는 **SMOTE** |
| `marital_stability` | 18.72:1 | ⚠️ 주의 | **class_weight** 권장 |

#### LightGBM 파라미터 예시
```python
import lightgbm as lgb
from sklearn.model_selection import train_test_split

# 1. Train/Test 분리
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# 2. LightGBM 파라미터 (불균형 처리)
lgb_params = {
    'objective': 'binary',
    'metric': 'auc',
    'boosting_type': 'gbdt',
    
    # ⚠️ 불균형 처리 (중요!)
    'class_weight': 'balanced',  # 자동 가중치 조정
    
    # 하이퍼파라미터
    'learning_rate': 0.05,
    'num_leaves': 31,
    'max_depth': -1,
    'min_child_samples': 20,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    
    'verbose': -1,
    'n_jobs': -1
}

# 3. 학습
train_data = lgb.Dataset(X_train, label=y_train)
valid_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

model = lgb.train(
    lgb_params,
    train_data,
    num_boost_round=1000,
    valid_sets=[train_data, valid_data],
    early_stopping_rounds=50,
    verbose_eval=100
)
```

---

### 🎯 Feature 선택 전략

#### 최종 사용 Feature (5개 + 팀원 features)
```python
# OHJ 생성 Features (5개)
ohj_features = [
    'education_group',           # ⚠️ class_weight 필요
    'is_economically_active',    # ✅ 핵심 변수
    'occupation_type',           # ✅ 보조 변수
    'is_employee',               # ✅ 보조 변수
    'marital_stability',         # ⚠️ class_weight 권장
]

# 팀원 Features (확인 필요)
team_features = [
    # KSH: age_group, is_single, house_income, dementia_case, ...
    # PDY: weight_control_method, activity_score_and_weight, ...
    # Sangmin: ...
    # MHS: time_col, ...
]

# 최종 Feature 리스트
final_features = ohj_features + team_features
```

#### Feature 조합 우선순위
1. **필수 (단독 사용):**
   - `education_group`
   - `is_economically_active`
   - `marital_stability`

2. **보조 (함께 사용 시 효과):**
   - `occupation_type` (← `is_economically_active` 세부)
   - `is_employee` (← `occupation_type` 세부)

3. **수동 조합 (선택사항):**
   ```python
   # Tree 모델은 자동으로 상호작용 학습
   # 하지만 강력한 패턴 발견 시 수동 생성 가능:
   df['edu_eco_interaction'] = (
       df['education_group'].astype(str) + '_' + 
       df['is_economically_active'].astype(str)
   )
   # 예: '2_1' = 고학력 × 경제활동 (최저 그룹)
   ```

---

### 📊 예상 Feature Importance (Top 10)

**예측 순위:**
```
1. marital_stability     (21.9%p 차이)
2. education_group       (17.0%p 차이)
3. is_economically_active (13.7%p 차이)
4. [팀원 흡연 관련 변수들...]
5. occupation_type       (14.6%p 차이)
6. is_employee           (13.7%p 차이)
7. [기타 변수들...]
```

**근거:**
- 금연 성공률 차이가 클수록 Feature Importance 높음
- 상호작용 효과는 모델이 자동으로 포착

---

## 📝 검증 완료 사항

### ✅ 데이터 품질
- **결측값:** 모든 원본 변수 0% (우수)
- **이상값 처리:** 무응답 코드(77, 88, 99) 적절히 처리
- **타입 에러 해결:** 한글 → 영어 변경 (팀원 간 호환성)

### ✅ 로직 검증
- `features_anal_vfxpedia.ipynb`에서 전체 분석 완료
- 각 feature별 분포, 금연성공률, 불균형 검증
- 2-way 히트맵으로 상호작용 효과 확인

### ✅ 코드 통일
- `notebooks/team/modules/features_ohj.py` (팀 공유)
- `notebooks/vfxpedia/scripts/features_01_vfxpedia.py` (vfxpedia 버전)
- `notebooks/vfxpedia/scripts/features_vfxpedia.py` (최종 버전)

---

## 🚀 적용 가이드

### Step 1: 데이터 로드
```python
# 04_피처통합데이터.ipynb에서 생성된 최종 데이터
df = pd.read_csv('../../data/prep_data_v2.csv')

print(f"데이터 크기: {df.shape}")
print(f"생성된 Features: {[f for f in ohj_features if f in df.columns]}")
```

### Step 2: 원본 변수 제거
```python
# ⚠️ 중복 방지를 위해 원본 변수 제거
df_model = df.drop(drop_features, axis=1)

print(f"원본 변수 제거 후: {df_model.shape}")
```

### Step 3: Feature 확인
```python
# 생성된 feature 분포 확인
for feat in ohj_features:
    print(f"\n{feat}:")
    print(df_model[feat].value_counts())
    
    # 금연 성공률
    print(f"\n금연 성공률:")
    print(df_model.groupby(feat)['churn'].mean() * 100)
```

---

## ⚠️ 중요 변경 이력

### 2025-10-14 업데이트

#### 1. 한글 → 영어 변경
```python
# 변경 전
occupation_type: ['화이트칼라', '블루칼라', '비경제활동']
marital_stability: ['안정', '미혼', '불안정']

# 변경 후
occupation_type: ['white_color', 'blue_color', 'inactive']
marital_stability: ['stable', 'single', 'unstable']
```
**이유:** 팀원 간 인코딩 문제 방지, 코드 호환성

#### 2. 불균형 해소
```python
# occupation_type
- '기타' 417명 (군인 404 + 무응답 13) → blue_color 통합
- 불균형: 약 62:1 → 2.50:1

# marital_stability  
- '기타' 17명 (무응답) → unstable 통합
- 불균형: 3506:1 → 18.72:1
```

#### 3. is_married 제거
- **이유:** `marital_stability`가 더 디테일하고 예측력 높음
- **근거:**
  - is_married: 단순 배우자 유/무 (2개 카테고리)
  - marital_stability: 안정/미혼/불안정 구분 (3개)
  - 성공률 패턴: 안정 > 미혼 > 불안정 (명확)

**최종 Feature 개수:** ~~7개~~ → **5개**

---

## 📚 참고 자료

### 분석 노트북
- **EDA 06:** `06_education_smoking_analysis.ipynb` - 교육수준 분석
- **EDA 07:** `07_economic_activity_analysis.ipynb` - 경제활동 분석
- **EDA 08:** `08_analysis_education_economy.ipynb` - 교육×경제 상호작용
- **Feature 분석:** `scripts/features_anal_vfxpedia.ipynb` - 최종 검증

### 데이터 파일
- **원본:** `data/analy_data.csv` (89,822 × 210)
- **정제 v2:** `data/analy_data_v2.csv` (액상형 담배 로직 수정)
- **최종:** `data/prep_data_v2.csv` (파생변수 포함)

### 코드 파일
- **팀 공유:** `notebooks/team/modules/features_ohj.py`
- **vfxpedia:** `notebooks/vfxpedia/scripts/features_01_vfxpedia.py`
- **최종:** `notebooks/vfxpedia/scripts/features_vfxpedia.py`

---

## 💬 결론

### 핵심 가치

1. **단순화 (Simplification)**
   - 복잡한 원본 변수(10개 카테고리) → 의미 있는 그룹(3개)
   - 모델 학습 효율성 향상

2. **예측력 (Predictability)**
   - 금연 성공률 차이 명확 (최대 21.9%p)
   - 각 feature의 독립적 예측력 검증 완료

3. **해석력 (Interpretability)**
   - 사회학적 의미: 교육, 직업, 혼인 상태
   - 실무 적용: 고위험군 식별 → 맞춤형 프로그램

### 기대 효과

✅ **모델 성능 향상**
- Tree 기반 모델(LightGBM)에 최적화
- 상호작용 효과 자동 학습

✅ **금연 실패 고위험군 식별**
- "고학력 × 경제활동 중" 그룹
- "혼인 불안정" 그룹
→ 맞춤형 금연 지원 프로그램 설계 가능

✅ **Feature Importance 해석 용이**
- 각 변수의 사회적 의미 명확
- 정책 제언 가능 (예: 직장 내 금연 프로그램 강화)

---

## 📞 문의

**작성자:** OHJ (vfxpedia)  
**최종 수정:** 2025-10-14  
**관련 문의:** features_ohj.py 관련 질문은 @vfxpedia

---

**Last Updated:** 2025-10-14  
**Version:** 2.0 (최종)
