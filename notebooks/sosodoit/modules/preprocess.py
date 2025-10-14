# ==================================================
# 내용: eda | ml 에서 사용된 전처리 코드
# 데이터 카테고리: 기본정보 + 가구정보
# ==================================================
import pandas as pd
import numpy as np

# 데이터 로드
filepath = "../../data/analy_data.csv"
data = pd.read_csv(filepath, encoding="utf-8")

# 데이터 전처리
data['EXAMIN_YEAR'] = data['EXAMIN_YEAR'].apply(lambda x: x.split("'")[1])
data['exmprs_no'] = data['exmprs_no'].apply(lambda x: x.split("'")[1])
data['CTPRVN_CODE'] = data['CTPRVN_CODE'].apply(lambda x: x.split("'")[1])
data['PBHLTH_CODE'] = data['PBHLTH_CODE'].apply(lambda x: x.split("'")[1])
data['SPOT_NO'] = data['SPOT_NO'].apply(lambda x: x.split("'")[1])
data['HSHLD_CODE'] = data['HSHLD_CODE'].apply(lambda x: x.split("'")[1])
data['MBHLD_CODE'] = data['MBHLD_CODE'].apply(lambda x: x.split("'")[1])
data['DONG_TY_CODE'] = data['DONG_TY_CODE'].apply(lambda x: x.split("'")[1])
data['HOUSE_TY_CODE'] = data['HOUSE_TY_CODE'].apply(lambda x: x.split("'")[1])
data['signgu_code'] = data['signgu_code'].apply(lambda x: x.split("'")[1])
data['kstrata'] = data['kstrata'].apply(lambda x: x.split("'")[1])
data['sex'] = data['sex'].apply(lambda x: 1 if x == 1 else 2).astype(str)
data['churn'] = data['churn'].astype(str)

# object 타입 컬럼 중에서 숫자형으로 보이는 컬럼들에 대해 변환(float -> int -> object)
type_convert = ['fma_19z3','fma_04z1','fma_12z1','fma_24z2','nue_01z1','fma_27z1','fma_26z1']
for col in type_convert:
    data[col] = data[col].apply(lambda x: str(int(x)) if pd.notnull(x) and float(x).is_integer() else str(x))

# 결측치 처리 (7 = 응답거부, 8 = 비해당, 9 = 모름 → NaN으로 변환)
data['fma_13z1'] = data['fma_13z1'].replace({77777: np.nan, 88888:np.nan, 99999: np.nan})
data['fma_14z1'] = data['fma_14z1'].replace({77777: np.nan, 88888:np.nan, 99999: np.nan})
data['fma_24z2'] = data['fma_24z2'].replace({'77': np.nan, '88':np.nan, '99': np.nan})
data['nue_01z1'] = data['nue_01z1'].replace({7: np.nan, 9: np.nan})

# 파생변수
def outliers_iqr(df, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1
    upper =  np.floor(q3 + 1.5 * iqr)
    new_col = f'{col}_iqr'
    df[new_col] = np.where(df[col] > upper, upper, df[col])
    return df

# 가구원수그룹
data = outliers_iqr(data, 'mbhld_co') 

# 연령대
data['age_group'] = (data['age'] // 10) * 10

# 성인 1인가구(x)
data['is_single_adult'] = np.where((data['mbhld_co'] == 1) & (data['reside_adult_co'] == 1), 1, 0)

# 1인가구
data['is_single'] = np.where((data['mbhld_co'] == 1), 1, 0)

# 월간소득 기준 가구소득컬럼 통합
data['fma_14z1_add'] = data['fma_14z1'] 
data['fma_14z1_add'] = round(data['fma_14z1_add'].fillna(data['fma_13z1'] / 12))
data['fma_14z1_log'] = np.log1p(data['fma_14z1_add'])

bins = [0, 50, 100, 200, 300, 400, 500, 600, float('inf')]
labels = [1, 2, 3, 4, 5, 6, 7, 8]
data['fma_14z1_group'] = pd.cut(data['fma_14z1_add'], bins=bins, labels=labels, right=False)
data['fma_14z1_group'] = np.where(data['fma_14z1_group'].isna(), data['fma_24z2'].astype(float), data['fma_14z1_group'])

# 소득 5분위(x)
data['fma_14z1_5q'] = pd.qcut(data['fma_14z1_add'], 5, labels=['1Q','2Q','3Q','4Q','5Q'])

# 식생활균형(x)
data['food_stable'] = np.where(data['nue_01z1'].isin(['1', '2']), 1, np.where(data['nue_01z1'].isin(['3', '4']), 0, np.nan))

# 치매가족여부
def get_dementia_case(row):
    if row['fma_27z1'] == '1' and row['fma_26z1'] == '1':
        return '1' # 치매가족 있음 + 같이 거주
    elif row['fma_27z1'] == '1' and row['fma_26z1'] == '2':
        return '2' # 치매가족 있음 + 비거주
    elif row['fma_27z1'] == '2':
        return '3' # 치매가족 없음
    else:
        return np.nan

data['fma_dementia_case'] = data.apply(get_dementia_case, axis=1)

# 일반담배일평균(단위: 개비)
data['smb_avg_per_day'] = data.apply(lambda x : x[['smb_01z1', 'smb_03z1', 'smb_06z1']].max(skipna=True), axis=1)

# 컬럼 삭제
data.drop(['fma_13z1', 'fma_14z1','fma_27z1','fma_26z1','smb_01z1','smb_03z1','smb_06z1'], axis=1, inplace=True)