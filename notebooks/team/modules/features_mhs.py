# ==================================================
# 내용: 피처생성코드
# 함수명: feature_[변수명]
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
import pandas as pd
import numpy as np

def feature_time_col(df_merge):
    # 시간-분 컬럼 쌍 정의
    time_minute_pairs = [
        ('edit_mtc_03z1', 'mtc_04z1'),
        ('mtc_05z1', 'mtc_06z1'),
        ('mtc_08z1', 'mtc_09z1'),
        ('mtc_10z1', 'mtc_11z1')
    ]

    # 각 쌍에 대해 분을 시간으로 변환해 더함
    for time_col, minute_col in time_minute_pairs:
        # 분 컬럼이 존재할 경우만 처리
        if minute_col in df_merge.columns and time_col in df_merge.columns:
            df_merge[time_col] = df_merge[time_col].fillna(0) + (df_merge[minute_col].fillna(0) / 60)
    
    return df_merge