# ==================================================
# 내용: 피처생성코드
# 함수명: feature_[변수명]
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
import pandas as pd
import numpy as np

# feature_weight_control_method
# feature_activity_score_and_weight


# 체중조절방법
def feature_weight_control_method(df_merge):
    cols = ['obb_02a1', 'obb_02b1', 'obb_02d1']
    # ["체중조절방법_운동", "체중조절방법_단식", "체중조절방법_무처방약물"]

    # 세 컬럼 모두 NaN인 행의 개수
    all_nan_count = df_merge[cols].isna().all(axis=1).sum()

    # NaN을 '비응답'으로 대체하고, 세 칼럼을 조합한 문자열 생성
    df_merge["weight_control_method"] = (
        df_merge[cols]
        .fillna("no_response")          # NaN → '비응답'
        .astype(str)               # 숫자를 문자열로 변환
        .agg("-".join, axis=1)     # 3개 값을 '-'로 연결
    )

    return df_merge


# 가중치 곱한 활동점수, 그에 따른 범주화
def feature_activity_score_and_weight(df_merge):

    df_merge["activity_score_weight"] = (
        3 * df_merge["pha_04z1"].fillna(0) +
        2 * df_merge["pha_07z1"].fillna(0) +
        1 * df_merge["phb_01z1"].fillna(0)
    )
    # 고강도, 중강도, 걷기 활동. 77 이상 NaN 처리되었다 가정
    
    def activity_level(x):
        if x >= 10:
            return "high_activity"
        elif x >= 5:
            return "normal_activity"
        elif x >= 1:
            return "row_activity"
        else:
            return "no_activity"

    df_merge["activity_score"] = df_merge["activity_score_weight"].apply(activity_level)

    return df_merge

# 액상형 관련 처리
# 액상형을 피워봤는데 churn이 1이라 애매한 row 모두 제거. 3,148건 제거됨
def Liquid_method1(df_merge):
    # 9 모름 -> 2 아니오로 처리
    df_merge.loc[df_merge["sma_08z1"] == 9, 'sma_08z1'] = 2.0
    df_merge = df_merge[~((df_merge['sma_08z1']==1) & (df_merge['churn']==1))]
    return df_merge


# 액상형 피워봤고, 최근 한 달 동안 피운 일수가 0을 초과하는데 churn이 1이면 0으로 변경
def Liquid_method2(df_merge):
    # 9 모름 -> 2 아니오로 처리
    df_merge.loc[df_merge["sma_08z1"] == 9, 'sma_08z1'] = 2.0
    df_merge.loc[(df_merge['sma_08z1'] == 1) & (df_merge['sma_11z2'] != 0) & (df_merge['churn'] == 1), 'churn'] = 0
    return df_merge