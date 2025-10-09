# 📊 EDA (Exploratory Data Analysis)

탐색적 데이터 분석을 위한 노트북들입니다.

## 📁 파일 구조

### 1️⃣ 데이터 이해 단계
- **01_data_overview.ipynb**: 전체 데이터 개요 및 기본 통계
- **02_decoder_test.ipynb**: VariableDecoder 기능 테스트 및 검증

### 2️⃣ 데이터 품질 진단
- **03_diagnosis_data_quality.ipynb**: 데이터 품질 문제 파악 및 진단

### 3️⃣ 데이터 정제
- **04_data_cleaning_strategy.ipynb**: 데이터 정제 전략 수립
- **05_data_cleaning_final.ipynb**: 최종 데이터 정제 실행

### 4️⃣ 심층 분석
- **06_education_smoking_analysis.ipynb**: 교육 수준과 금연의 관계 분석
- **07_economic_activity_analysis.ipynb**: 경제활동 상태와 금연의 관계 분석
- **08_analysis_education_economy.ipynb**: 교육·경제 종합 분석

## 🔧 사용 방법

### 경로 설정
모든 노트북은 프로젝트 루트 기준으로 상대 경로를 사용합니다:

```python
import sys
import os

# 프로젝트 루트를 Python 경로에 추가
project_root = os.path.abspath('../../..')
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 유틸리티 import (개인 폴더 내)
from utils.variable_decoder import VariableDecoder

# 팀 공통 데이터 로드
df = pd.read_csv('../../../data/analy_data.csv')
```

### 권장 실행 순서

1. **01_data_overview.ipynb** - 데이터 전체 파악
2. **02_decoder_test.ipynb** - 디코더 기능 확인
3. **03_diagnosis_data_quality.ipynb** - 데이터 품질 진단
4. **04_data_cleaning_strategy.ipynb** - 정제 전략 수립
5. **05_data_cleaning_final.ipynb** - 데이터 정제 실행
6. **06, 07, 08** - 세부 주제별 분석

## 📌 주요 발견사항

### 데이터 현황
- **전체 데이터**: 89,822건
- **분석 대상 변수**: 교육수준, 경제활동, 흡연 관련 변수

### 주요 인사이트
- 교육 수준별 금연 성공률 차이 존재
- 경제활동 상태가 금연 성공에 영향
- 특정 변수들의 결측치 및 특수코드 처리 필요

## 🔗 관련 리소스

- **팀 공통 데이터**: `../../../data/analy_data.csv` (분석용), `../../../data/raw_data.csv` (원본)
- **개인 데이터**: `../data/variable.csv` (변수 매핑), `../data/data_explain.csv` (변수 설명)
- **유틸리티**: `../utils/variable_decoder.py` (변수 디코더)
- **개인 유틸**: `../utils/data_cleaning.py` (데이터 정제)

## ⚠️ 주의사항

- 노트북 실행 전 필요한 라이브러리 설치 확인
- 한글 폰트 설정 필요 (Malgun Gothic)
- 상대 경로 기준으로 작성되어 있으므로 폴더 구조 변경 시 주의

## 📅 업데이트 이력

- 2025-10-09: EDA 폴더로 구조 정리 및 경로 통일

