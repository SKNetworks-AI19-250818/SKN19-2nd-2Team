## 데이터 받는 방법 (Git LFS 설치 필수)

- 우리 프로젝트의 데이터(.csv 등 대용량 파일)는 Git LFS (Large File Storage) 로 관리됩니다.
- **가장 먼저 Git LFS를 설치한 뒤 저장소를 clone 해야 정상적으로 데이터를 확인할 수 있습니다.**

Git LFS 설치가 안 되어 있으면, 데이터 파일이 아래처럼 포인터 파일로만 보일 수 있습니다.
```
version https://git-lfs.github.com/spec/v1
oid sha256:xxxxxxxx
size 210123456
```

### 1. Git LFS 설치 (최초 1회)
```bash
# Windows (Git Bash)
git lfs install
```

### 2. 저장소 Clone
```bash
git clone https://github.com/SKNetworks-AI19-250818/SKN19-2nd-2Team.git
cd SKN19-2nd-2Team
```

### 3. LFS 파일 다운로드
``` bash
# 일반 clone 시 자동으로 내려오지만, 혹시 빠진 경우 실행
git lfs pull
```

---

<br>
<br>

## 흡연 이탈(흡연 → 비흡연) 예측 프로젝트

### 프로젝트 개요
- 고객 이탈 예측이라는 큰 주제에서 출발하여, 이를 **흡연 이탈(금연 성공)** 이라는 주제로 구체화하였습니다.
- 지역사회건강조사(Community Health Survey) 데이터를 활용하여 흡연자의 이탈(흡연 → 비흡연) 가능성을 예측하고, 
- 금연 희망자들이 어떤 상황을 달성하면 성공 확률이 높아지는지 인사이트를 도출하는 것을 목표로 합니다.

### 문제 정의
- 문제: 어떤 요인들이 흡연자의 금연 이탈에 영향을 주는가?
- 목표: 금연 이탈 여부를 예측하는 모델 개발
- 활용: 금연 희망자들이 "성공 조건(특정 피처)"을 달성하도록 유도 → 금연 이탈 확률 향상 기대

### 데이터 개요
- 출처: 2024년 지역사회건강조사 (설문조사 기반)
- 대상: 조사시점에 표본가구에 거주하는 만 19세 이상 성인
- 기간: 2024년 5월 16일 ~ 7월 31일
- 규모
    - 원본: 231,728 rows × 209 columns
    - 분석용(1차 가공): 89,822 rows × 147 columns (label 포함)
- 주요 변수(카테고리)
    ```
    기본정보
    가구정보
    건강행태(흡연)
    건강행태(음주)
    건강행태(신체활동)
    건강행태(식생활)
    건강행태(비만및체중조절)
    건강행태(구강건강)
    정신건강
    보건기관이용
    교육및경제활동
    ```

### 분석 데이터 1차 가공 코드
- 필요한 컬럼 식별 및 분석 대상 범위 조정
- smoke_anal_data_churn.csv → data/analy_data.csv

```python
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