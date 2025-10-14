## 주의사항
1. **노션 링크 제거**: 최종 README에는 노션 링크를 포함하지 말고 실제 내용으로 채우기
2. **이미지 첨부**: 주요 시각화 결과는 images/ 폴더에 저장
3. **데이터 참고**: 모든 표와 수치는 노션 DB를 참고하여 작성
4. **Markdown 포맷팅**: GitHub Markdown 문법 준수

### 1. 프로젝트 타이틀 & 배지

👉 GitHub 배지를 사용하여 기술 스택 표시

### 2. 팀 소개

👉 [팀 소개](https://www.notion.so/27f649136c1181d39b48ec87bbe2ab5a?pvs=21)

- 팀명: 이조는 차분하조
- 팀원 이름 & GitHub 링크
- 역할 분담
#### 산출물 경로

분석/개발과정
분류|파일명|설명|경로
---|---|---|---
노트북|	...	|EDA 분석|	notebooks/...
노트북|	...	|ML 분석|	notebooks/...
노드북| ...	|팀리뷰|	notebooks/...

최종모델/결과
분류|파일명|설명|경로
---|---|---|---
전처리 코드|	preprocess.py|	데이터 전처리|	modules/...
모델 코드|	train.py|	모델 학습 및 저장|	components/...
Streamlit 코드|	app.py|	분석 대시보드|	streamlit/

#### 프로젝트 폴더 구조
- data : 데이터 저장소
- notebooks : EDA · ML 실험 공간 + 팀리뷰
- smoke_churn_model : (확정) 모델 패키지 코드

<details>
<summary>클릭</summary>

```bash
# 데이터 저장소
data/
  ├─ raw_data.csv           # 원본 데이터
  ├─ analy_data.csv         # 1차 전처리 데이터 
  └─ prep_data_v2.csv       # 2차 전처리 데이터

# EDA · ML 실험 공간 + 팀리뷰
notebooks/
 ├─ 김소희/
 ├─ 마한성/
 ├─ 박도연/
 ├─ 오흥재/
 ├─ 임상민/
 │
 └─ team/                  # 팀리뷰
    ├─ 01_데이터정제.ipynb  # 데이터 전처리 코드 통합 
    ├─ 02_ML학습준비.ipynb  # 모델 테스트 및 피처 생성
    ├─ 03_ML모델비교.ipynb 
    ├─ columns.json        # 활용 컬럼 관리
    ├─ features_01.py      # 담당자별 피처코드
    ├─ features_...py      
    ├─ preprocess.py       # 전처리 패키징
    └─ test.ipynb          # 모듈 테스트

# (확정) 모델 패키지 코드
smoke-churn-model/
 ├─ components/
 │   ├─ train.py      # 최종 모델 학습
 │   ├─ evaluate.py   # 최종 모델 평가
 │   ├─ predict.py    # 최종 모델 예측
 │   └─ cv.py         # 5개 모델 학습 및 평가 검증
 │
 ├─ modules/
 │   ├─ config.py     # 경로 및 환경설정
 │   └─ preprocess.py # 데이터 로드 및 전처리 
 │
 └─ resource/
     └─ columns.json  # 활용 피처 관리
```

</details>

### 3. 프로젝트 개요

- 프로젝트명
흡연 이탈 예측 프로젝트
기간: 2025.09.30 ~ 2025.10.15 (D+0)
팀원: 5인

- 간단한 소개 (2-3문장)
지역사회건강조사 데이터를 활용하여 흡연자들의 이탈 가능성을 예측하고 금연 희망자들의
특성을 입력받아 어떤 행동을 개선하면 좋을지 방향을 제시하는 금연 솔루션을 제공한다.

- 프로젝트 필요성 (배경)
금연을 하고자 하는 사람들에게 구체적인 행동 교정을 통해 목표 달성이 보다 수월하게 돕는다

- 프로젝트 목표
1. 어떤 요인들이 흡연 이탈에 영향을 주는지 분석
2. 금연 이탈 예측 모델 개발
3. 금연 희망자들이 "흡연 이탈"을 달성하도록 유도 → 흡연 이탈(금연 성공) 장려

### 4. 기술 스택

- Python
- 주요 라이브러리: pandas, scikit-learn, xgboost 등

### 5. WBS

👉 [WBS DB](https://www.notion.so/27f649136c11814db5cff4f0082b24d9?pvs=21)

### 6. 데이터 전처리 결과서

👉 [EDA 분석](https://www.notion.so/EDA-27f649136c1181f8822fd6c052931839?pvs=21)

#### 1) 데이터 출처
- 출처: 2024년 지역사회건강조사 (한국건강영양조사KCHS)
- 대상: 조사시점에 표본가구에 거주하는 만 19세 이상 성인
- 기간: 2024년 5월 16일 ~ 7월 31일
- 형태: 단면조사 (Cross-sectional)
- 표본 수: 약 85,000명
- 특징: 개인, 가구, 건강행태, 사회경제 정보로 구성<br>
※ 단면조사 (Cross-sectional): 특정 시점(혹은 짧은 기간)에 여러 개인/가구를 한 번만 조사 한 시점의 스냅샷

#### 2) 데이터 규모
원본: 231,728 rows × 209 columns
분석용 전처리 데이터: 89,822 rows × 75 columns (label 포함)
- 필요한 컬럼 식별 및 분석 대상 범위 조정
- churn 타겟변수 정의: 흡연 이탈 여부 (1=이탈, 0=유지) 
```python
# 최근 코드로 수정!!!!!!!!!!!!!
# 과거 또는 현재 흡연자만 도출
com_df = pd.read_csv('Community_Health_Survey_data.csv')
anal_data = com_df[~((com_df['sma_03z2'] > 3.0) & (com_df['sma_12z2'] > 2.0) & (com_df['sma_37z1'] > 3.0))].reset_index(drop=True)

# 현재 흡연 여부. 하나라도 현재 피우고 있으면 흡연 중
currently_smoking = (
    anal_data['sma_03z2'].isin([1, 2]) |
    (anal_data['sma_12z2'] == 1) |
    anal_data['sma_37z1'].isin([1, 2])
)

# 과거에 피웠으나 현재 피우지 않음
stop_smoked = (
    (anal_data['sma_03z2'] == 3) |
    (anal_data['sma_12z2'] == 2) |
    (anal_data['sma_37z1'] == 3)
)

# 금연 성공자: 현재는 흡연 안 하고, 과거엔 피운 적 있음
anal_data['churn'] = np.where(
    (~currently_smoking) & stop_smoked,
    1,
    0
)
anal_data.to_csv('smoke_anal_data_churn.csv', index=False, encoding='utf-8-sig')
```
- 최종 학습에 사용된 데이터: 89,822 rows × 147 columns (label 포함)

#### 3) 주요 전처리 결과
- 전처리 과정
	- 설문지를 보고 흡연이탈예측모델에 활용할 변수 1차 수동 식별
	- 결측치가 없어보이지만 설문데이터이므로 자제처리 필요: 응답거부(77777), 모름(99999) → NaN 변환
	- 변수간 상관관계, 변수중요도를 통해 변수 2차 식별
	- 설문지가 단계별로 진행되어 1-1, 1-2, 1-3 의 변수를 하나의 변수로 통합하는 등 전처리 과정 진행
	- EDA/모델링 과정에서 피처 생성 추가 진행
	- 피처 생성하면서 변수간 정보가 중복되는 변수는 제거


- 데이터 탐색 과정에서의 주요 발견사항
	- 작성필요

### 7. 인공지능 학습 결과서
#### 문제 정의
“흡연자 중 어떤 사람이 금연에 성공할 가능성이 높은가?”
이 질문을 예측 문제로 전환하면 다음과 같다

구분 | 내용|
---|---
입력(Feature) | 개인 및 가구 단위의 사회경제·건강 정보
출력(Target) | 	churn = 흡연 이탈 여부 (1: 이탈, 0: 유지)
문제유형 | 이진분류(Binary Classification)
평가지표 |	ROC-AUC, F1-score, Precision, Recall 

#### 기대 효과 (우리 목적에 맞게 검토필요!!!!!!!!)
	- 공공보건정책에서 금연 성공 가능성이 낮은 집단을 사전에 파악 가능
	- 지역별·계층별 금연지원 프로그램 설계의 근거 데이터 제공
	- 향후 “맞춤형 금연 지원 서비스” 개발로 확장 가능

- 모델링 과정
#### 주요 성능 평가 지표
Accuracy, Precision, Recall
F1-Score, ROC-AUC, PR-AUC
교차검증(k=5)으로 평균 성능 측정

#### 후보 모델 성능 비교
Logistic Regression
RandomForest
XGBoost
LightGBM
DecisionTree
CatBoost
ExtraTreesClassifier

#### 최종 모델 선정
선정 모델:
ROC-AUC:
PR-AUC:
주요 Feature Importance:

### 8. 수행 결과

- 목표 달성 현황
- 주요 성과
- 한계 및 개선점

### 9. 한 줄 회고

👉 [최종 회고](https://www.notion.so/27f649136c11818e80b7ed752f31a687?pvs=21)

---

### 10. 참고 자료



## 추가 권장 섹션

- **설치 및 실행 방법**
- **프로젝트 구조**
- **사용 예시**
- **라이센스**