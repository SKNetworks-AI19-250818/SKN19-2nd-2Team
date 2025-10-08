# 오흥재 (vfxpedia) - 개인 작업 공간

**주제**: 교육 및 경제활동에 따른 금연 성공 상관관계 분석

---

## 📁 폴더 구조

```
vfxpedia/
├── README.md                          # 이 파일
│
├── utils/                             # 유틸리티 함수
│   ├── data_cleaning.py               # 데이터 정제 모듈
│   └── (추가 유틸리티)
│
├── docs/                              # 문서
│   ├── PDF_VERIFICATION_NEEDED.md     # PDF 확인 필요 변수
│   ├── USAGE_GUIDE.md                 # 사용 가이드
│   └── (기타 문서)
│
├── output/                            # 분석 결과
│   ├── analy_data_cleaned.csv         # 정제된 데이터
│   ├── analysis_results.csv           # 분석 결과
│   └── (그래프, 보고서 등)
│
└── (노트북 파일들)
    ├── 01_diagnosis.ipynb             # 데이터 진단
    ├── 02_data_cleaning.ipynb         # 데이터 정제
    └── 03_final_analysis.ipynb        # 최종 분석
```

---

## 🚀 작업 순서

### 1단계: 데이터 진단
```bash
01_diagnosis_data_quality.ipynb
```
- 변수별 코드값 확인
- 특수코드 분포 파악
- 분석 가능 표본 확인

### 2단계: 데이터 정제
```bash
02_data_cleaning_final.ipynb
```
- 특수코드 처리
- 결측값 제거
- `output/analy_data_cleaned.csv` 생성

### 3단계: 최종 분석
```bash
03_final_analysis.ipynb (생성 예정)
```
- 상관관계 분석
- 특성 중요도 분석
- 가설 검증
- 최종 보고서

---

## 📊 분석 변수

### ✅ 최종 선정 (5개)
1. **sob_01z1** - 교육수준(최종학력)
2. **soa_01z1** - 경제활동 여부
3. **soa_06z2** - 직업분류
4. **soa_07z1** - 종사상 지위
5. **sod_02z3** - 혼인상태

### ❌ 제외
- **sob_02z1** - 졸업상태 (Skip Logic으로 인한 복잡도)

---

## 🎯 주요 가설

### H1: 교육수준
교육 수준이 높을수록 금연 성공률이 높다

### H2: 경제활동
경제활동 안정성이 높을수록 금연 성공률이 높다

### H3: 직업분류
직종별로 금연 성공률에 차이가 있다

### H4: 혼인상태
혼인 상태가 금연 성공에 영향을 미친다

---

## ⚠️ 주의사항

### 데이터 경로
- 원본 데이터: `../../data/analy_data.csv`
- 정제 데이터: `./output/analy_data_cleaned.csv`

### 팀 공용 공간
- `data/` 폴더는 팀 공용이므로 직접 수정 금지
- 개인 파일은 `vfxpedia/` 폴더 내에서만 관리

### Import 경로
```python
import sys
sys.path.append('C:/SKN_19/SKN19-2nd-2Team')

# 팀 공용 유틸
from data.var_mapping import VAR_DICT
from util.decode_helper import decode_dataframe

# 개인 유틸
sys.path.append('./utils')
from data_cleaning import clean_data_for_analysis
```

---

## 📝 진행 상황

- [x] 데이터 진단 완료
- [x] 정제 전략 수립
- [x] 정제 스크립트 작성
- [ ] 데이터 정제 실행
- [ ] 상관관계 분석
- [ ] 특성 중요도 분석
- [ ] 가설 검증
- [ ] 최종 보고서

---

**최종 업데이트**: 2025-10-07  
**작성자**: 오흥재 (vfxpedia)
