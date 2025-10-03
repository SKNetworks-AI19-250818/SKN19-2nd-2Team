## 데이터 정보
- 원본 데이터: data/raw_data.csv (건강설문 원본데이터)
- 분석 데이터: data/analy_data.csv (label 포함한 1차분석데이터)

## 데이터 위치
현재 프로젝트 폴더 구조는 아래와 같습니다.
```
root(SKN19-2ND-2TEAM)/
├─ data/
│  ├─ raw_data.csv       # 원본 데이터 (수정 금지)
│  └─ analy_data.csv     # 분석 데이터
├─ notebooks/
│  ├─ 이름1/
│  │  ├─ eda__건강환경.ipynb
│  │  ├─ model__xgb_baseline.ipynb
│  ├─ 이름2/
│  ├─ ...
│  └─ team/
```
👉 **본인 폴더(notebooks/이름/) 안에서 작업합니다.**

## 데이터 불러오기 코드
본인 폴더 안에서 아래 코드 그대로 실행하면 됩니다.

### 상대경로 이용시
```python
import pandas as pd

# notebooks/ → ../../ 로 두 단계 올라가서 data/ 폴더 접근
data = pd.read_csv("../../data/analy_data.csv")

print("데이터 크기:", data.shape)
data.head()
```

### 절대경로 이용시
```python
import os
import pandas as pd

# 현재 노트북 파일 기준 프로젝트 루트 경로 계산
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(".")))
DATA_PATH = os.path.join(BASE_DIR, "data", "analy_data.csv")

data = pd.read_csv(DATA_PATH)
print("데이터 크기:", data.shape)
data.head()
```
- 만일 폴더를 생성해서 경로가 달라지면 BASE_DIR을 루트 경로를 잘 찾아주면 됩니다.
- `BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath("..")))`
- `print(BASE_DIR)`

## 주의사항
- 절대 data/ 안의 파일을 직접 수정하지 마세요.
- 새로운 데이터 버전이 나오면 analy_data_v2.csv처럼 파일명을 바꿔서 공유할 예정입니다.