"""
설명: 식생활 + 비만 및 체중조절 + 구강건강 카테고리에서
      중요도 상위 13개 변수만 남기고 결측치 처리 (결측률 40% 이상 컬럼 자동 삭제)
"""

import pandas as pd
import numpy as np

# 1. 데이터 불러오기
data = pd.read_csv("../../data/analy_data.csv")

# 2. 유지할 컬럼
keep_cols = [
    "nua_01z2", "nuc_02z1", "nuc_03z1", "ore_03z2", "ord_05z1", "ord_01d2",
    "ord_01f3", "obb_02a1", "obb_02b1", "obb_02d1", "ora_01z1", "orb_01z1"
]

target_col = "churn"
if target_col in data.columns:
    keep_cols = [target_col] + keep_cols

data = data.loc[:, [c for c in keep_cols if c in data.columns]]

# 3. 결측률 40% 초과 컬럼 제거
missing_rate = data.isna().mean()
drop_cols = missing_rate[missing_rate > 0.4].index.tolist()
if drop_cols:
    print("결측률 40% 초과 컬럼:", drop_cols)
    data.drop(columns=drop_cols, inplace=True)

# 4. 결측치 처리 (수치형→중앙값, 범주형→최빈값)
num_cols = data.select_dtypes(include=[np.number]).columns
cat_cols = data.select_dtypes(exclude=[np.number]).columns

for col in num_cols:
    if data[col].isnull().any():
        data[col].fillna(data[col].median(), inplace=True)

for col in cat_cols:
    if data[col].isnull().any():
        mode_val = data[col].mode()
        data[col].fillna(mode_val.iloc[0] if len(mode_val) else "미상", inplace=True)

# 5. 결과 저장
data.to_csv("../../data/analy_data_clean.csv", index=False, encoding="utf-8-sig")
print("✅ 정제 완료. 저장 위치: ../../data/analy_data_clean.csv")
