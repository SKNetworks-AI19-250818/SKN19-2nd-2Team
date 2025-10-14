# ==================================================
# 내용: 데이터 정제 및 전처리 코드 통합
# 1. preprocessing_data(data_path)
# 2. featuring_data(df_merge)
# ==================================================
import os
import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path
current_path=os.getcwd()
sys.path.append(os.path.abspath(os.path.join(os.path.join(current_path, 'notebooks/team'))))

ROOT_DIR = Path("").resolve().parent.parent
DATA_DIR = ROOT_DIR / "data"
DATA_PATH = DATA_DIR / "raw_data.csv"
ANAL_PATH =  DATA_DIR / "analy_data_v2.csv"
PREP_PATH = DATA_DIR / "prep_data_v1.csv" 
JSON_FILE = ROOT_DIR / "notebooks" / "team" / "columns.json"

# 개인 폴더 경로에 있는 columns.json 활용시
nick_name = "sosodoit"
MY_FILE = ROOT_DIR / "notebooks" / nick_name / "modules" / "columns.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    columns_dict = json.load(f)

# ==================================================
# Utill
# ==================================================
def get_columns(*categories):
    """columns.json의 카테고리별 use=y 컬럼 추출"""
    selected = []
    for cat in categories:
        for col, meta in columns_dict[cat].items():
            if meta.get("use", "n") == "y": 
                selected.append(col)
    
    if "churn" not in selected:
        selected.append("churn")

    if "exmprs_no" not in selected:
        selected.append("exmprs_no")

    return selected

def rename_to_kor(df):
    """columns.json의 name으로 한글 컬럼명 매핑"""
    rename_map = {
        col: meta["name"]
        for cat in columns_dict.values()
        for col, meta in cat.items()
        if col in df.columns
    }
    return df.rename(columns=rename_map)

# ==================================================
# Data Cleaning
# ==================================================
from modules.features_pdy import Liquid_method2
def make_target(data):

    # 과거 또는 현재 흡연자만 도출
    if isinstance(data, pd.DataFrame):
        anal_data = data[~((data['sma_03z2'] > 3.0) & (data['sma_12z2'] > 2.0) & (data['sma_37z1'] > 3.0))].reset_index(drop=True)
    else:
        com_df = pd.read_csv(data)
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
    
    # 액상형 관련 처리: 액상형 피워봤고, 최근 한 달 동안 피운 일수가 0을 초과하는데 churn이 1이면 0으로 변경
    anal_data = Liquid_method2(anal_data)
    anal_data.to_csv(ANAL_PATH, index=False, encoding='utf-8-sig')

    return anal_data

# ==================================================
# 1. 기본정보 + 가구조사 
# ==================================================
def preprocess_basic_house(data_path):
    cols = get_columns("기본정보", "가구조사")
    df = pd.read_csv(data_path, usecols=cols)

    # 'b' 문자 전처리
    if "exmprs_no" in df.columns:
        df['exmprs_no'] = df['exmprs_no'].apply(lambda x: x.split("'")[1])

    if "CTPRVN_CODE" in df.columns:
        df['CTPRVN_CODE'] = df['CTPRVN_CODE'].apply(lambda x: x.split("'")[1])
    
    if "SPOT_NO" in df.columns:
        df['SPOT_NO'] = df['SPOT_NO'].apply(lambda x: x.split("'")[1])
    
    if "sex" in df.columns:
        df['sex'] = df['sex'].apply(lambda x: 1 if x == 1 else 2).astype(str)

    # NaN 변경
    for col in ["fma_04z1", "nue_01z1", "fma_27z1", "fma_26z1"]:
        if col in df.columns:
            df.loc[df[col] >= 7, col] = np.nan

    for col in ["fma_13z1", "fma_14z1"]:
        if col in df.columns:
            df.loc[df[col] >= 77777, col] = np.nan

    for col in ["fma_24z2"]:
            if col in df.columns:
                df.loc[df[col] >= 77, col] = np.nan

    return df

# ==================================================
# 2. 식생활 + 비만및체중조절 + 구강건강
# ==================================================
def preprocess_diet_obesity_oral(data_path):
    cols = get_columns("식생활", "비만및체중조절", "구강건강")
    df = pd.read_csv(data_path, usecols=cols)

    # 'b' 문자 전처리
    if "exmprs_no" in df.columns:
        df['exmprs_no'] = df['exmprs_no'].apply(lambda x: x.split("'")[1])

    # NaN 변경
    for col in ["nua_01z2", "nuc_02z1", "nuc_03z1", "obb_02a1", "obb_02b1", "obb_02d1", "ora_01z1", "orb_01z1", "ord_01d2", "ord_05z1", "ord_01f3"]:
        if col in df.columns:
            df.loc[df[col] >= 7, col] = np.nan

    for col in ["ore_03z2"]:
            if col in df.columns:
                df.loc[df[col] >= 77, col] = np.nan

    return df

# ==================================================
# 3. 음주 + 신체활동
# ==================================================
def preprocess_drink_physical(data_path):
    cols = get_columns("음주", "신체활동")
    df = pd.read_csv(data_path, usecols=cols)

    # 'b' 문자 전처리
    if "exmprs_no" in df.columns:
        df['exmprs_no'] = df['exmprs_no'].apply(lambda x: x.split("'")[1])

    # 값 변경
    if "drb_01z3" in df.columns:
        df["drb_01z3"] = df["drb_01z3"].replace(8, 1)

    if "drb_03z1" in df.columns:
        df["drb_03z1"] = df["drb_03z1"].replace(8, -1)

    # NaN 변경 
    for col in ["drb_01z3", "drb_03z1", "drg_01z3", "pha_11z1", "drb_04z1", "drb_05z1"]:
        if col in df.columns:
            df.loc[df[col] >= 7, col] = np.nan

    for col in ["pha_04z1", "pha_07z1", "phb_01z1"]:
            if col in df.columns:
                df.loc[df[col] >= 77, col] = np.nan

    return df

# ==================================================
# 4. 정신건강 + 보건이용
# ==================================================
def preprocess_mental_health(data_path):
    cols = get_columns("정신건강", "보건이용")
    df = pd.read_csv(data_path, usecols=cols)

    # 'b' 문자 전처리
    if "exmprs_no" in df.columns:
        df['exmprs_no'] = df['exmprs_no'].apply(lambda x: x.split("'")[1])

    # NaN 변경 
    for col in ["mta_01z1", "mta_02z1", "mtc_08z1", "mtc_12c1", "mtc_12h1", "mtj_05z2", "mtj_10z1", "mtj_11z1"]:
        if col in df.columns:
            df.loc[df[col] >= 7, col] = np.nan

    for col in ["edit_mtc_03z1"]:
            if col in df.columns:
                df.loc[df[col] >= 77, col] = np.nan

    return df

# ==================================================
# 5. 건강행태 + 교육및경제활동
# ==================================================
def preprocess_behavior_education(data_path):
    cols = get_columns("건강행태", "교육및경제활동")
    df = pd.read_csv(data_path, usecols=cols)

    # 'b' 문자 전처리
    if "exmprs_no" in df.columns:
        df['exmprs_no'] = df['exmprs_no'].apply(lambda x: x.split("'")[1])

    # NaN 변경
    for col in ["smf_01z1", "sma_01z1", "sma_03z2", "smb_09z1", "sma_36z1", "sma_37z1", "sma_08z1", "sma_12z2"\
                "smd_02z3", "smd_01z3", "smc_08z2", "smc_09z2", "smc_10z2", "sob_02z1", "soa_01z1", "soa_07z1", "sod_02z3"]:
        if col in df.columns:
            df.loc[df[col] >= 7, col] = np.nan

    for col in ["smb_02z1", "smb_05z1", "sma_11z2", "sob_01z1", "soa_06z2", "smb_12z1"]:
            if col in df.columns:
                df.loc[df[col] >= 77, col] = np.nan

    for col in ["smb_01z1", "smb_13z1", "smb_03z1", "smb_04z1", "smb_06z1", "smb_11z1"]:
            if col in df.columns:
                df.loc[df[col] >= 777, col] = np.nan
    return df

def preprocessing_data(DATA_PATH):

    df_basic = preprocess_basic_house(DATA_PATH)
    df_health = preprocess_diet_obesity_oral(DATA_PATH)
    df_drink = preprocess_drink_physical(DATA_PATH)
    df_mental = preprocess_mental_health(DATA_PATH)
    df_behavior = preprocess_behavior_education(DATA_PATH)

    dfs = [df_basic, df_health, df_drink, df_mental, df_behavior]
    df_merge = dfs[0]
    for temp in dfs[1:]:
        join_cols = [c for c in ["exmprs_no", "churn"] if c in df_merge.columns and c in temp.columns]
        if join_cols:
            df_merge = pd.merge(df_merge, temp, on=join_cols, how="outer")

    print("(전처리)데이터 크기:", df_merge.shape, '(2개 제외)')

    return df_merge

# ==================================================
# Feature Enginerring
# ==================================================
def fillna(df_merge):
    """결측치 처리"""
    pass

def encode_feature(df_merge):
    """범주형 데이터를 숫자로 인코딩"""
    pass

def scaling_feature(train_data, test_data):
    """특성 스케일링"""
    pass

# 이곳에 담당 모듈 임포트 추가
from modules.features_ksh import feature_age_group, feature_is_single, feature_house_income, feature_dementia_case, feature_smoke_avg_per_day
from modules.features_mhs import feature_time_col
from modules.features_ohj import feature_education_group, feature_is_economically_active, feature_occupation_type, feature_is_employee, feature_marital_stability
from modules.features_pdy import feature_weight_control_method, feature_activity_score_and_weight
from modules.features_sangmin import apply_my_features

def featuring_data(df_merge):
    
    """이곳에 생성할 피처 추가"""
    df_merge = feature_age_group(df_merge)
    df_merge = feature_is_single(df_merge)
    df_merge = feature_house_income(df_merge)
    df_merge = feature_dementia_case(df_merge)
    df_merge = feature_smoke_avg_per_day(df_merge)
    df_merge = feature_time_col(df_merge)
    df_merge = feature_education_group(df_merge)
    df_merge = feature_is_economically_active(df_merge)
    df_merge = feature_occupation_type(df_merge)
    df_merge = feature_is_employee(df_merge)
    df_merge = feature_weight_control_method(df_merge)
    df_merge = feature_activity_score_and_weight(df_merge)
    df_merge = apply_my_features(df_merge) # 12개 피처생성 | 19개 삭제
    df_merge = feature_marital_stability(df_merge)

    return df_merge

def drop_feature(df_merge):
      
    """이곳에 모델 훈련과 관련 없는, 피처 생성 후 필요 없는 속성 제거 추가"""
    df_merge = df_merge.drop(['fma_13z1', 'fma_14z1', 'fma_27z1', 'fma_26z1', 'smb_01z1', 'smb_03z1', 'smb_06z1'], axis=1, errors='ignore') # ksh
    df_merge = df_merge.drop(['mtc_04z1', 'mtc_06z1', 'mtc_09z1', 'mtc_11z1','soa_01z1', 'sob_01z1','soa_07z1','soa_06z2', 'sod_02z3'], axis=1,  errors='ignore') # ohj
    df_merge = df_merge.drop(['nua_01z2', 'oba_02z1', 'oba_01z1', 'obb_01z1', 'obb_02a1', 'obb_02b1', 'obb_02c1',
                              'obb_02d1', 'obb_02e1', 'obb_02f1', 'obb_02g1', 'obb_02h1', 'obb_02i1',
                              'ore_03z2', 'ord_01d2', 'ord_01f3', 'ord_05z1', 'ora_01z1', 'orb_01z1'],
                              axis=1, errors='ignore') # sangmin
    return df_merge