# 📚 Phase 1 완료: 프로젝트 파악 및 분석 가이드

**작성일**: 2025-10-12  
**작성자**: vfxpedia (오흥재)  
**목적**: 흡연 설문조사 Skip Logic 이해 및 Feature Engineering 가이드

---

## 🎯 Phase 1 핵심 요약

### 1. 프로젝트 구조 파악 ✅

**데이터 흐름:**
```
raw_data.csv
   ↓ (타겟 라벨링)
analy_data.csv (팀 공용, 89,822건)
   ↓ (개인별 EDA)
preprocessed_v1.csv (use="y" 변수만)
   ↓ (Feature Engineering)
df_merge (모델 학습용)
```

**팀 규칙:**
- `columns.json`: 변수 관리 (use="y/n")
   ```json
   {
   "카테고리": {
      "변수명": {
         "name": "한글명",
         "use": "y/n"  // 사용 여부
      }
   }
   }
   ```
- `features_01.py`: Feature 함수 규칙
  ```python
  def feature_{name}(df_merge):
      return df_merge
  ```
- `01_데이터정제.ipynb`: 카테고리별 전처리
   ```python
   # 카테고리별 전처리
   def preprocess_basic_house(data_path):
      # 1. use="y"인 컬럼만 로딩
      # 2. 'b' 문자 제거
      # 3. 특수코드(7, 77, 777, 8, 88, 888, 9, 99, 999) → NaN
      return df
    ```
- `02_ML학습준비.ipynb`: 추가 전처리

---

### 2. 설문조사 Skip Logic 핵심 이해 ✅

#### **Target Label: churn**
```
churn = 1: 금연 성공 (과거 흡연, 현재 안 피움)
churn = 0: 금연 실패 (현재 흡연 중)
```

#### **핵심 변수: sma_03z2 (현재 흡연 상태)**
```
1 = 매일 피운다        → churn = 0
2 = 가끔 피운다        → churn = 0
3 = 과거 피웠으나 현재 안 피움 → churn = 1 ⭐
결측값 = 비흡연자 (smf_01z1=2, Q8로 건너뜀)
```

#### **변수 그룹 (논리적 유효성)**

**Group A: 모든 사람에게 유효**
- `smf_01z1`: 평생 담배 경험
- `sma_01z1`: 평생 흡연량
- `sob_01z1`: 교육수준 ⭐
- `soa_01z1`: 경제활동여부 ⭐
- `soa_06z2`: 직업분류 ⭐
- `soa_07z1`: 종사상지위 ⭐
- `sod_02z3`: 혼인상태 ⭐

**Group B: 현재 흡연자만 유효 (sma_03z2=1,2)**
- `smb_01z1`: 매일흡연자 하루흡연량
- `smb_02z1`: 가끔흡연자 월간흡연일수
- `smb_03z1`: 가끔흡연자 일평균흡연량
- `smd_01z3`: 금연계획 ⭐⭐⭐
- `smd_02z3`: 금연시도 ⭐⭐

**Group C: 과거 흡연자만 유효 (sma_03z2=3)**
- `smb_04z1`: 과거 흡연기간_년
- `smb_05z1`: 과거 흡연기간_월
- `smb_06z1`: 과거 하루평균흡연량
- `smb_09z1`: 금연기간 ⭐⭐⭐⭐⭐

---

### 3. 논리적 결측값 vs 진짜 결측값 ⚠️

**논리적 결측값 (Skip Logic)**
```python
# 예시 1: 금연계획 (smd_01z3)
df[df['sma_03z2'] == 3]['smd_01z3'].isna()
→ True (과거 흡연자는 이미 금연했으므로 질문 안 받음)

# 예시 2: 금연기간 (smb_09z1)
df[df['sma_03z2'].isin([1,2])]['smb_09z1'].isna()
→ True (현재 흡연자는 금연한 적 없으므로 질문 안 받음)
```

**⚠️ 단순 `fillna(0)`은 위험!**
```python
# ❌ 잘못된 처리
df['smd_01z3'].fillna(0)  # 과거 흡연자를 "금연계획 없음"으로 잘못 해석

# ✅ 올바른 처리
# 1. 그룹별로 따로 분석
current_smokers = df[df['sma_03z2'].isin([1, 2])]
past_smokers = df[df['sma_03z2'] == 3]

# 2. Feature Engineering으로 명시
df['is_current_smoker'] = df['sma_03z2'].isin([1, 2]).astype(int)
```

---

## 🚀 담당 분석: 교육/경제 변수

### 담당 변수 (5개)

| 변수명 | 설명 | 값 범위 | 비고 |
|--------|------|---------|------|
| sob_01z1 | 교육수준 | 1~8 | 1:무학 ~ 8:대학원 ✅ |
| soa_01z1 | 경제활동여부 | 1~2 | 1:취업, 2:비경제활동 ✅ |
| soa_06z2 | 직업분류 | 1~10 | 1:농림어업 ~ 10:군인 ✅ |
| soa_07z1 | 종사상지위 | 1~3 | 1:고용주/자영업, 2:임금근로자, 3:무급가족 ✅ |
| sod_02z3 | 혼인상태 | 1~5 | 1:유배우 ~ 5:별거 |

### 주요 가설

1. **H1: 교육수준**
   - 교육 수준이 높을수록 금연 성공률 ↑
   
2. **H2: 경제활동 안정성**
   - 취업 > 비경제활동 > 실업
   - 정규직 > 비정규직
   
3. **H3: 직업 유형**
   - 화이트칼라 > 블루칼라
   
4. **H4: 혼인 상태**
   - 기혼(유배우) > 기타

---

## 📂 생성된 파일

### 1. 분석 스크립트
**`scripts/01_smoking_logic_analysis.py`**
```bash
cd C:\SKN_19\SKN19-2nd-2Team\notebooks\vfxpedia
python scripts/01_smoking_logic_analysis.py
```

**기능:**
- churn 타겟 분포 확인
- 흡연 상태 변수 분석
- skip logic 검증
- 교육/경제 변수 기초 분석

---

### 2. Feature Engineering 모듈 (2가지 버전)

#### **Version 1: 상세 버전 (개인 사용)**
**`scripts/features_vfxpedia.py`**

**생성 Feature (7개):**
| # | Feature 명 | 설명 | 값 | 근거 |
|---|-----------|------|-----|------|
| 1 | `education_group` | 교육수준 그룹 | 0:저학력(무학~초등) / 1:중학력(중학~전문대) / 2:고학력(4년제~대학원) | EDA 06번: 역U자 패턴 ✅ |
| 2 | `is_economically_active` | 경제활동 여부 | 0:비경제활동 / 1:경제활동 | EDA 07번: 13.75%p 차이 ✅ |
| 3 | **job_risk_group** | **직업 위험도** | **0:저위험 / 1:중위험 / 2:고위험 / -1:해당없음** | **EDA 07번: 금연 성공률 기반** ✅ |
| 4 | **occupation_type** | **직업 유형** | **화이트칼라/블루칼라/비경제활동** | **일반 분류 (보조 변수)** 🔵 |
| 5 | `is_employee` | 임금근로자 여부 | 0:자영업/고용주/무급가족 / 1:임금근로자 | EDA 07번: 7.46%p 차이 ✅ |
| 6 | `is_married` | 배우자 있음 | 0/1 | 가설: 사회적 지지 🔵 |
| 7 | `marital_stability` | 혼인 안정성 | 안정/미혼/불안정 | 가설: 스트레스 관리 🔵 |

**✅ = EDA 근거 있음 (필수) | 🔵 = 가설 기반 (추가)**

**사용법:**
```python
from scripts.features_vfxpedia import add_education_economy_features

df_merge = add_education_economy_features(df_merge)
```

---

#### **Version 2: 팀 통합 버전**
**`scripts/features_01_vfxpedia.py`**

팀의 `features_01.py` 규칙에 맞춘 버전

**사용법:**
```python
# team/features_01.py에 복사 후
from features_01 import (
    feature_education_group,
    feature_is_economically_inactive,
    feature_occupation_type,
    feature_is_employee,
    feature_is_married,
    feature_marital_stability
)

df_merge = feature_education_group(df_merge)
df_merge = feature_is_economically_inactive(df_merge)
df_merge = feature_occupation_type(df_merge)
# ... (순서대로 적용)
df_merge = feature_marital_stability(df_merge)
```

---

## 🎬 다음 단계 (Phase 2)

### 1. 데이터 분석 실행
```python
# 1. skip logic 분석
python scripts/01_smoking_logic_analysis.py

# 2. Feature Engineering
from scripts.features_vfxpedia import add_education_economy_features
df = add_education_economy_features(df)

# 3. 상관관계 분석
# 교육수준 × 금연 성공률
# 경제활동 × 금연 성공률
```

### 2. 팀 코드 통합
```python
# team/02_ML학습준비.ipynb에 추가
# vfxpedia 파트
df_merge = feature_education_group(df_merge)
df_merge = feature_is_economically_inactive(df_merge)
# ...
```

### 3. 모델링 준비
- Target: churn
- Features: 교육/경제 + 기존 변수
- 그룹별 모델 고려:
  - 현재 흡연자 → 금연 성공 예측
  - 과거 흡연자 → 금연 유지 기간 예측

---

## 💡 핵심 인사이트

### 1. 설문조사 특성 이해 ⭐⭐⭐
```
결측값 ≠ 응답 안 함
결측값 = Skip Logic (질문 대상 아님)
```

### 2. 변수 그룹별 분석 필요
- **Group A**: 전체 대상 (교육/경제 변수)
- **Group B**: 현재 흡연자 (금연계획/시도)
- **Group C**: 과거 흡연자 (금연기간)

### 3. churn 타겟 이해
```
churn = 1: 금연 성공 (sma_03z2 = 3)
       → smb_09z1 (금연기간) 분석 중요

churn = 0: 현재 흡연 (sma_03z2 = 1,2)
       → smd_01z3 (금연계획), smd_02z3 (금연시도) 분석
```

---

## 🧩 조합 패턴 분석 방법

### **🎯 핵심 원리**

**❌ 종합 점수 방식 (사용 안 함)**
```python
# 이런 단순 합산은 의미 없음
stability_score = 교육(2) + 경제활동(1) + 기혼(1) = 4점
→ "점수 4점 = 금연 성공률 70%" (너무 단순)
```

**✅ 조합 패턴 분석 (권장)**
```python
# 구체적인 조합별 금연 성공률 확인
패턴 A: 화이트칼라 + 고학력 + 기혼 + 경제활동 = 85% ⭐
패턴 B: 블루칼라 + 저학력 + 미혼 + 비경제활동 = 32% ❌
```

### **✅ 방법 1: 교차 집계 (Crosstab)**

**2개 Feature 조합**
```python
# 직업 유형 × 교육 수준
pd.crosstab(
    [df['occupation_type'], df['education_group']], 
    df['churn']
).apply(lambda x: x/x.sum(), axis=1)

# 결과 예시:
#                                    churn=0  churn=1  금연성공률
# occupation_type  education_group                           
# 화이트칼라        2 (고학력)         0.22    0.78    78%  ⭐
# 화이트칼라        1 (중학력)         0.35    0.65    65%
# 블루칼라         0 (저학력)         0.68    0.32    32%  ❌
```

### **✅ 방법 2: GroupBy 집계**

**3개 이상 Feature 조합**
```python
# 직업 × 교육 × 혼인
result = df.groupby([
    'occupation_type',
    'education_group', 
    'is_married'
])['churn'].agg(['count', 'mean']).sort_values('mean', ascending=False)

# 결과 예시:
# occupation    education  married  count  mean(금연성공률)
# 화이트칼라     2(고학력)    1       1234   0.82  ⭐⭐⭐
# 화이트칼라     2(고학력)    0        456   0.75
# 블루칼라      0(저학력)    0        890   0.28  ❌❌❌
```

### **✅ 방법 3: 조건 필터링**

**특정 조합의 금연 성공률 확인**
```python
# 화이트칼라 + 고학력 + 기혼 + 경제활동 조합
high_success = df[
    (df['occupation_type'] == '화이트칼라') &
    (df['education_group'] >= 1) &           # 중학력 이상
    (df['is_married'] == 1) &
    (df['is_economically_active'] == 1)
]

success_rate = high_success['churn'].mean()
print(f"✨ 금연 성공률: {success_rate*100:.1f}%")
print(f"📊 전체 평균과 차이: +{(success_rate - df['churn'].mean())*100:.1f}%p")
```

### **✅ 방법 4: Decision Tree 시각화**

**자동으로 최적 조합 찾기**
```python
from sklearn.tree import DecisionTreeClassifier, plot_tree

features = ['education_group', 'is_economically_active', 
            'occupation_type', 'is_employee', 
            'is_married', 'marital_stability']

model = DecisionTreeClassifier(max_depth=4)
model.fit(X[features], y)

# 시각화로 패턴 확인
plot_tree(model, feature_names=features, filled=True)

# 결과 예시 (자동 패턴 발견):
#                     ┌─ occupation_type = 화이트칼라
#                     │  └─ education_group >= 1
#                     │     └─ is_married = 1
#                     │        → 금연 성공률 85% ⭐
#     churn 예측 ───┤
#                     └─ occupation_type = 블루칼라
#                        └─ is_economically_active = 0
#                           → 금연 성공률 30% ❌
```

---

## 🗺️ 설문조사 Skip Logic 분석

### **핵심 이슈: "논리적 결측값"**

```
[Q1: smf_01z1] 담배 경험?
├─ YES (89,950명) → Q2로
└─ NO (141,774명) → Q8로 (건너뛰기)
    ↓ Q2~7 모두 skip
    ↓ 결측값의 의미: "비흡연자"

[Q2-1: sma_03z2] 현재 흡연?
├─ ① 매일 피운다 (33,801명)
│   ↓ smb_01z1 (하루 흡연량)
│   ↓ Q6-7 (금연시도/계획) 답변 가능
│
├─ ② 가끔 피운다 (3,597명)  
│   ↓ smb_02z1, smb_03z1
│   ↓ Q6-7 답변 가능
│
└─ ③ 과거 흡연, 현재 안 피움 (52,059명) ⭐
    ↓ smb_09z1 (금연기간) ← 이게 churn=1의 핵심!
    ↓ smd_01z3 (금연계획) = 비해당(결측)
```

### **변수의 의미론적 분류**

**Group A: Target Label 생성용**
```python
# churn = 1 (금연 성공)의 정의
if sma_03z2 == 3:  # 과거 흡연, 현재 안 피움
    churn = 1
    relevant_vars = ['smb_09z1']  # 금연기간만 의미 있음
    
# churn = 0 (금연 실패/현재 흡연)
elif sma_03z2 in [1, 2]:  # 매일 or 가끔 피움
    churn = 0
    relevant_vars = ['smb_01z1', 'smd_02z3', 'smd_01z3']
```

**Group B: 현재 흡연자에게만 유효**
- `smd_01z3` (금연계획)
- `smd_02z3` (금연시도)
- `smb_01z1` (현재 흡연량)

⚠️ 이 변수들은 churn=1인 사람에게 결측값!

**Group C: 금연 성공자에게만 유효**
- `smb_09z1` (금연기간) ← 가장 중요!
- `smb_06z1` (과거 흡연량)

⚠️ 이 변수들은 churn=0인 사람에게 결측값!

**Group D: 모두에게 유효**
- `smf_01z1` (평생 담배 경험)
- `sma_01z1` (평생 흡연량)
- `smc_08z2`, `smc_10z2` (간접흡연)

---

## 📖 Feature 사용법

### **방법 1: 개별 함수 사용**
```python
from features_01_vfxpedia import (
    feature_education_group,
    feature_is_economically_active,
    feature_occupation_type,
    feature_is_employee,
    feature_is_married,
    feature_marital_stability
)

df = feature_education_group(df)
df = feature_is_economically_active(df)
df = feature_occupation_type(df)
df = feature_is_employee(df)
df = feature_is_married(df)
df = feature_marital_stability(df)
```

### **방법 2: 통합 함수 사용**
```python
from features_01_vfxpedia import create_all_features

df = create_all_features(df)
# ✅ 6개 Feature 생성 완료!
```

### **방법 3: 상세 버전 사용**
```python
from features_vfxpedia import create_vfxpedia_features

df, stats = create_vfxpedia_features(df, verbose=True)

# 통계 확인
print(stats['education_group']['distribution'])
# {0: 15234, 1: 32456, 2: 23456}
```

---

## 🚀 다음 단계 (Phase 2)

### **1. Feature 적용 및 검증**
- [ ] `preprocessed_v1.csv` 로딩
- [ ] 6개 Feature 생성
- [ ] Feature 분포 확인
- [ ] 결측값 확인

### **2. 조합 패턴 분석**
- [ ] 2-way 조합 (교육 × 경제활동)
- [ ] 3-way 조합 (직업 × 교육 × 혼인)
- [ ] Decision Tree로 최적 패턴 발견

### **3. 교육수준/경제활동 심층 분석**
- [ ] 담당 변수별 금연 성공률 분석
- [ ] 교차 분석 및 시각화
- [ ] 주요 인사이트 도출

### **4. 팀 통합**
- [ ] `team/features_01.py`에 함수 추가
- [ ] 팀원들과 코드 리뷰
- [ ] 최종 Feature 확정

---

## 📚 참고 자료

### **생성된 파일**
1. `scripts/features_01_vfxpedia.py` - 팀 통합용 (간소화)
2. `scripts/features_vfxpedia.py` - 상세 버전
3. `scripts/01_smoking_logic_analysis.py` - 분석 스크립트

### **분석 노트북**
- `notebooks/vfxpedia/09_EDA_vfxpedia.ipynb` - 최종 분석

### **데이터 정의**
- `columns.json` - 변수 정의
- `smoking_survey.txt` - 설문지 원본

---

## ✅ Phase 1 체크리스트

- [x] 프로젝트 구조 파악
- [x] 팀 작업 규칙 이해
- [x] 담당 변수 확인
- [x] 설문조사 로직 분석
- [x] Feature Engineering 설계
- [x] 6개 Feature 함수 작성
- [x] 조합 패턴 분석 방법 정리
- [x] 사용 가이드 작성

**🎉 Phase 1 완료! 이제 Phase 2로 진행하세요!**

---

## 🔧 실행 체크리스트

### Phase 1 완료 ✅
- [x] 프로젝트 구조 파악
- [x] 설문조사 skip logic 이해
- [x] 변수 그룹핑 완료
- [x] Feature Engineering 코드 작성
- [x] 분석 스크립트 작성

### Phase 2 진행 중 🚧
- [ ] skip logic 분석 실행
- [ ] Feature Engineering 적용
- [ ] 교육/경제 변수 상관관계 분석
- [ ] 팀 코드 통합

### Phase 3 예정 📅
- [ ] 모델링 (이진분류)
- [ ] Feature Importance 분석
- [ ] 시각화 대시보드 (Streamlit)

---

## 📞 문의

**Phase 1 관련:**
- vfxpedia (오흥재) 


**팀 협업:**
- sosodoit (팀장)
- colaa222, doyeon, gitsgetit (팀원)

---

**최종 업데이트**: 2025-10-13  
**다음 업데이트**: Phase 2 완료 후

---