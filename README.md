## 주의사항
1. **노션 링크 제거**: 최종 README에는 노션 링크를 포함하지 말고 실제 내용으로 채우기
2. **이미지 첨부**: 주요 시각화 결과는 images/ 폴더에 저장
3. **데이터 참고**: 모든 표와 수치는 노션 DB를 참고하여 작성
4. **Markdown 포맷팅**: GitHub Markdown 문법 준수

### 1. 프로젝트 타이틀 & 배지

👉 GitHub 배지를 사용하여 기술 스택 표시

### 2. 팀 소개

👉 [팀 소개](https://www.notion.so/27f649136c1181d39b48ec87bbe2ab5a?pvs=21)

- 팀명
- 팀원 이름 & GitHub 링크
- 역할 분담

#### 프로젝트 폴더 구조
- data : 데이터 저장소
- notebooks : EDA · ML 실험 공간 + 팀리뷰
- smoke_churn_model : (확정) 모델 패키지 코드

<details>
<summary>클릭</summary>

```bash
# 데이터 저장소
data/
  ├─ raw_data.csv           # 원본 데이터 (수정 금지)
  └─ analy_data.csv         # 분석 데이터 (수정 금지)

# EDA · ML 실험 공간 + 팀리뷰
notebooks/
 ├─ 팀원1/
 ├─ 팀원2/
 ├─ 팀원3/
 ├─ 팀원4/
 ├─ 팀원5/
 │
 └─ team/                  # 팀리뷰
    ├─ 01_데이터정제.ipynb  # 데이터 전처리 코드 통합 
    ├─ 02_ML학습준비.ipynb  # 모델 테스트 및 피처 생성
    │  
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
- 간단한 소개 (2-3문장)
- 프로젝트 필요성 (배경)
- 프로젝트 목표

### 4. 기술 스택

- Python
- 주요 라이브러리: pandas, scikit-learn, xgboost 등

### 5. WBS

👉 [WBS DB](https://www.notion.so/27f649136c11814db5cff4f0082b24d9?pvs=21)

### 6. 데이터 전처리 결과서

👉 [EDA 분석](https://www.notion.so/EDA-27f649136c1181f8822fd6c052931839?pvs=21)

- 데이터셋 개요
- 주요 발견사항
- 전처리 과정

### 7. 인공지능 학습 결과서

👉 [모델 레지스트리](https://www.notion.so/27f649136c1181b4bf82f370fb2ff3ba?pvs=21) 
👉 [성능 평가](https://www.notion.so/27f649136c1181569785c70b4efe519d?pvs=21) 

- 모델 비교 표
- 최종 모델 선정 이유
- 주요 성능 지표

### 8. 수행 결과

- 목표 달성 현황
- 주요 성과
- 한계 및 개선점

### 9. 한 줄 회고

👉 [최종 회고](https://www.notion.so/27f649136c11818e80b7ed752f31a687?pvs=21)

---

## 추가 권장 섹션

- **설치 및 실행 방법**
- **프로젝트 구조**
- **사용 예시**
- **라이센스**