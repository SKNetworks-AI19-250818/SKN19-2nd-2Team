# 🤖 Model (모델링 및 평가)

머신러닝 모델 개발 및 평가를 위한 노트북들입니다.

## 📁 예정된 파일 구조

### 1️⃣ 베이스라인 모델
- **01_model_baseline.ipynb**: 기본 모델 구축 및 성능 평가
  - Logistic Regression
  - Decision Tree
  - Random Forest (기본 설정)

### 2️⃣ 모델 최적화
- **02_model_optimization.ipynb**: 하이퍼파라미터 튜닝
  - GridSearchCV / RandomizedSearchCV
  - 교차 검증
  - Feature Engineering

### 3️⃣ 모델 평가 및 해석
- **03_model_evaluation.ipynb**: 최종 모델 평가 및 해석
  - 성능 지표 (Accuracy, Precision, Recall, F1-score, ROC-AUC)
  - Feature Importance
  - SHAP Values
  - 혼동 행렬 및 분류 보고서

### 4️⃣ 앙상블 및 고급 기법
- **04_ensemble_models.ipynb**: 앙상블 모델
  - XGBoost
  - LightGBM
  - Stacking / Voting

## 🔧 사용 방법

### 경로 설정
```python
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.abspath('../../..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 유틸리티 import
from util.variable_decoder import VariableDecoder

# 정제된 데이터 로드
df = pd.read_csv('../../../data/cleaned_data.csv')  # EDA 후 정제된 데이터
```

### 권장 실행 순서

1. **EDA 완료 확인** - `../eda/` 폴더의 분석 완료
2. **01_model_baseline.ipynb** - 기본 모델 성능 확인
3. **02_model_optimization.ipynb** - 모델 성능 개선
4. **03_model_evaluation.ipynb** - 최종 평가 및 해석
5. **04_ensemble_models.ipynb** - 앙상블로 성능 극대화

## 📊 평가 지표

### 분류 문제 (금연 성공 예측)
- **주요 지표**: F1-Score, ROC-AUC
- **보조 지표**: Accuracy, Precision, Recall
- **비즈니스 관점**: 금연 성공자를 정확히 예측하는 것이 중요 (Recall 중시)

### 모델 선택 기준
1. 해석 가능성 (정책 제안을 위해 중요)
2. 예측 성능
3. 과적합 방지
4. 계산 비용

## 🎯 목표

- **금연 성공 예측 모델** 구축
- **주요 영향 변수** 파악
- **정책 제안**을 위한 인사이트 도출

## 📌 체크리스트

- [ ] EDA 완료 및 정제된 데이터 준비
- [ ] 베이스라인 모델 구축
- [ ] 하이퍼파라미터 튜닝
- [ ] Feature Importance 분석
- [ ] 최종 모델 선정 및 해석
- [ ] 비즈니스 인사이트 도출

## 🔗 관련 리소스

- **EDA 결과**: `../eda/`
- **데이터**: `../../../data/`
- **유틸리티**: `../../../util/`

## ⚠️ 주의사항

- 모델 학습 전 데이터 스케일링 확인
- 클래스 불균형 문제 고려 (SMOTE, class_weight 등)
- 교차 검증으로 과적합 방지
- 랜덤 시드 고정으로 재현성 확보

## 📅 업데이트 이력

- 2025-10-09: Model 폴더 생성 및 구조 설계

