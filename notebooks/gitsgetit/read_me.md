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
흡연 이탈 예측 프로젝트

- 간단한 소개 (2-3문장)
지역사회건강조사 데이터를 활용하여 흡연자들의 이탈 가능성을 예측하고 금연 희망자들의
특성을 입력받아 어떤 행동을 개선하면 좋을지 방향을 제시하는 금연 솔루션을 제공한다.

- 프로젝트 필요성 (배경)
금연을 하고자 하는 사람들에게 구체적인 행동 교정을 통해 목표 달성이 보다 수월하게 돕는다

- 프로젝트 목표
1. 어떤 요인들이 금연 이탈에 영향을 주는지 분석
2. 금연 이탈 여부 예측 모델 개발
3. 해당 모델에서 사용자의 특성을 입력받아 일부 특성 강화를 통해 흡연 이탈(금연 성공) 장려

### 4. 기술 스택

- Python
- 주요 라이브러리: pandas, scikit-learn, xgboost 등

### 5. WBS

👉 [WBS DB](https://www.notion.so/27f649136c11814db5cff4f0082b24d9?pvs=21)

### 6. 데이터 전처리 결과서

👉 [EDA 분석](https://www.notion.so/EDA-27f649136c1181f8822fd6c052931839?pvs=21)

- 데이터셋 개요
89822 rows,  75 columns

질문 내용에 따른 분류:

기본정보	흡연관련	음주관련	안전의식	건강행태	질병	수면시간	스트레스, 우울감	수면의 질	치매 및 인지장애	질병경험	사회인구학적 특성
EXAMIN_YEAR	smf_01z1	dra_01z1	sfa_02z3	pha_04z1	cva_11z2	ora_01z1	mta_01z1	edit_mtc_03z1	mtj_05z2	sca_01z1	sob_01z1
exmprs_no	sma_01z1	drb_01z3	sfb_05z2	pha_05z1	cva_12z1	orb_01z1	mta_02z1	mtc_04z1	mtj_06z2	hya_19z1	sob_02z1
age	sma_03z2	drb_03z1	sfa_12z2	pha_06z1	cva_14z2	ord_01d2	mtb_01z1	mtc_05z1	mtj_09z2	hya_04z1	soa_01z1
sex	smb_01z1	drb_16z1	sfb_07z1	pha_07z1	cva_16z2	ord_05z1	mtb_02z1	mtc_06z1	mtj_10z1	hya_15z1	soa_06z2
CTPRVN_CODE	smb_02z1	drb_04z1	sfa_06z2	pha_08z1	cva_17z1	ord_01f3	mtb_07a1	mtc_08z1	mtj_11z1	hya_14c2	soa_07z1
PBHLTH_CODE	smb_03z1	drb_05z1	sfb_03z2	pha_09z1	mya_10z2	ore_02z2	mtb_07b1	mtc_09z1		hya_14a2	sod_02z3
SPOT_NO	smb_04z1	drg_01z3	sfa_08z2	phb_01z1	mya_11z2	ore_03z2	mtb_07c1	mtc_10z1		hya_14b2	
HSHLD_CODE	smb_05z1	dre_03z1		phb_02z1	mya_12z2	스케일링경험	mtb_07d1	mtc_11z1		hya_30z1	
MBHLD_CODE	smb_06z1	dre_04z1		phb_03z1	mya_14z1	mtc_17z1	mtb_07e1	mtc_12a1		hya_10z1	
DONG_TY_CODE	smb_09z1			pha_11z1	mya_15z1	mtc_18z1	mtb_07f1	mtc_12b1		hya_11a2	
HOUSE_TY_CODE	sma_36z1			nua_01z2			mtb_07g1	mtc_12c1		hya_11c2	
signgu_code	sma_37z1			nuc_02z1			mtb_07h1	mtc_12d1		hya_11d2	
kstrata	smb_11z1			nuc_01z2			mtb_07i1	mtc_12e1		dia_19z1	
wt_h	smb_12z1			nuc_03z1			mtd_01z1	mtc_12f1		dia_04z1	
wt_p	smb_13z1			oba_02z1			mtd_02z1	mtc_12g1		dia_18z1	
mbhld_co	sma_08z1			oba_03z1				mtc_12h1		dia_13c2	
reside_adult_co	sma_11z2			oba_bmi				mtc_12i1		dia_13b2	
fma_19z3	sma_12z2			oba_01z1				mtc_12j1		dia_13a2	
fma_04z1	smd_02z3			obb_01z1				mtc_13z1		dia_09z1	
fma_12z1	smd_01z3			obb_02a1				mtc_14z1		dia_10a2	
fma_13z1	smc_08z2			obb_02b1				mtc_15z1		dia_10c2	
fma_14z1	smc_09z2			obb_02c1				mtc_16z1		dia_10d2	
fma_24z2	smc_10z2			obb_02k1						dia_22z2	
nue_01z1				obb_02d1						dia_14z1	
fma_27z1				obb_02e1						dia_15z1	
fma_26z1				obb_02f1						sra_01z3	
qoa_01z1				obb_02g1						sra_02z2	
				obb_02h1						ira_01z1	
				obb_02i1						ira_02z1	
										i1a_04z2	
										i2a_04z2	
										i3a_04z2	
										i4a_04z2	
										i5a_04z2	
										qoc_07z1	
										qoc_01z1	
										qoc_02z1	
										qoc_03z1	
										qoc_04z1	
										qoc_05z1	
										hma_01z3	
										cpr_01z1	
										cpr_02z1	
										cpr_03a2	
										cpr_03b2	
										cpr_04z1	

제거 컬럼: fma_13z1: 가구 소득(기간), fma_14z1: 가구 소득(금액), fma_27z1: 가족 중 치매 환자 여부, fma_26z1: 치매 환자와의 거주 여부,
smb_01z1: 일반담배를 매일 피우는 사람들의 흡연량, smb_03z1: 일반담배를 가끔 피우는 사람들의 흡연량, smb_06z1: 과거에는 피웠으나 현재는 피우지 않는 사람들의 흡연량, mtc_04z1, mtc_06z1, mtc_09z1, mtc_11z1: 수면(분)에 관한 컬럼, soa_01z1: 경제활동, sob_01z1: 교육 수준, 
soa_07z1: 경제활동상 지위, soa_06z2: 직업, sod_02z3: 혼인상태, nua_01z2: 아침식사 횟수, oba_02z1: 키, oba_01z1:체형



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

### 10. 자료 출처



## 추가 권장 섹션

- **설치 및 실행 방법**
- **프로젝트 구조**
- **사용 예시**
- **라이센스**