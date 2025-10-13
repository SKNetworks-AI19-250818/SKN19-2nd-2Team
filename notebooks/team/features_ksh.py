# ==================================================
# 내용: 피처생성코드
# 함수명: feature_[변수명]
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
import pandas as pd
import numpy as np

# 연령대
def feature_age_group(df_merge):    
    df_merge['age_group'] = (df_merge['age'] // 10) * 10
    return df_merge

# 1인가구
def feature_is_single(df_merge):    
    df_merge['is_single'] = np.where((df_merge['mbhld_co'] <= 1), 1, 0)
    return df_merge    

# 월간소득기준 가구소득컬럼
def feature_house_income(df_merge):

    bins = [0, 50, 100, 200, 300, 400, 500, 600, float('inf')]
    labels = [1, 2, 3, 4, 5, 6, 7, 8]

    df_merge['house_income'] = df_merge['fma_14z1'] 
    df_merge['house_income'] = round(df_merge['house_income'].fillna(df_merge['fma_13z1'] / 12))
    df_merge['house_income_log'] = np.log1p(df_merge['house_income'])
    df_merge['house_income_grp'] = pd.cut(df_merge['house_income'], bins=bins, labels=labels, right=False)
    df_merge['house_income_grp'] = np.where(df_merge['house_income_grp'].isna(), df_merge['fma_24z2'].astype(float), df_merge['house_income_grp'])

    return df_merge

# 치매가족여부
def get_dementia_case(row):
    if row['fma_27z1'] == 1 and row['fma_26z1'] == 1:
        return 1 # 치매가족 있음 + 같이 거주
    elif row['fma_27z1'] == 1 and row['fma_26z1'] == 2:
        return 2 # 치매가족 있음 + 비거주
    elif row['fma_27z1'] == 2:
        return 3 # 치매가족 없음
    else:
        return np.nan

def feature_dementia_case(df_merge):
    df_merge['fma_dementia_case'] = df_merge.apply(get_dementia_case, axis=1)
    return df_merge

# 일반담배일평균(단위: 개비)
def feature_smoke_avg_per_day(df_merge):
    df_merge['smoke_avg_per_day'] = df_merge.apply(lambda x : x[['smb_01z1', 'smb_03z1', 'smb_06z1']].max(skipna=True), axis=1)
    return df_merge