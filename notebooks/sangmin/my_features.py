# import pandas as pd
# import numpy as np

# # -----------------------------------
# # 유틸
# # -----------------------------------
# _BIN_YN = {1: 1, 2: 0}  # 예/아니오 → 1/0

# def _as_copy(df, copy=True):
#     return df.copy() if copy else df

# def _safe_num(s):
#     return pd.to_numeric(s, errors="coerce")

# def _fill_mode(s):
#     try:
#         return s.fillna(s.mode().iloc[0])
#     except Exception:
#         return s.fillna(s.dropna().iloc[0] if s.dropna().size else s)

# def _ordered_cat(series, labels, add_unknown=True):
#     cats = labels + (["Unknown"] if add_unknown and "Unknown" not in labels else [])
#     s = series.astype("object").where(series.notna(), "Unknown")
#     return pd.Categorical(s, categories=cats, ordered=True)

# # -----------------------------------
# # 1) 식생활
# # -----------------------------------
# def _feature_diet(df):
#     df = df.copy()

#     # 아침식사빈도 (1=주5~7회, 4=거의안함)
#     if "nua_01z2" in df.columns:
#         map_lbl = {1: "주5~7회", 2: "주3~4회", 3: "주1~2회", 4: "거의안함"}
#         df["breakfast_freq_cat"] = df["nua_01z2"].map(map_lbl)
#         df["breakfast_freq_cat"] = _ordered_cat(
#             df["breakfast_freq_cat"], ["주5~7회", "주3~4회", "주1~2회", "거의안함"]
#         )
#         # 점수(높을수록 바람직): 주5~7회=3 … 거의안함=0
#         df["breakfast_freq_score"] = df["nua_01z2"].replace({1: 3, 2: 2, 3: 1, 4: 0})
#         df["breakfast_freq_score"] = df["breakfast_freq_score"].fillna(df["breakfast_freq_score"].median())

#     # 영양표시 인지/활용/관심 (1/2 → 1/0)
#     for raw, out in {
#         "nuc_02z1": "nutrition_awareness_bin",
#         "nuc_01z2": "nutrition_usage_bin",
#         "nuc_03z1": "nutrition_interest_bin",
#     }.items():
#         if raw in df.columns:
#             df[out] = df[raw].map(_BIN_YN)
#             df[out] = _fill_mode(df[out])

#     return df

# # -----------------------------------
# # 2) 비만·체중조절
# # -----------------------------------
# def _feature_obesity_weight(df, weight_col: str | None = None):
#     """
#     weight_col: BMI가 없고 체중이 따로 있을 때 체중 컬럼명 (예: 'oba_03z1' or 'weight_kg')
#     """
#     df = df.copy()

#     # 신장(cm) → m
#     if "oba_02z1" in df.columns:
#         df["height_m"] = _safe_num(df["oba_02z1"]) / 100

#     # BMI (있으면 median 대체, 없고 키/체중 있으면 계산)
#     if "oba_bmi" in df.columns:
#         df["oba_bmi"] = _safe_num(df["oba_bmi"])
#         df["oba_bmi"] = df["oba_bmi"].fillna(df["oba_bmi"].median())
#     else:
#         if weight_col and weight_col in df.columns and "height_m" in df.columns:
#             w = _safe_num(df[weight_col])
#             h = _safe_num(df["height_m"])
#             bmi = w / (h ** 2)
#             df["oba_bmi"] = bmi
#             df["oba_bmi"] = df["oba_bmi"].fillna(df["oba_bmi"].median())

#     # 체형인지(자기평가) 1~5
#     if "oba_01z1" in df.columns:
#         map_lbl = {1: "매우마름", 2: "약간마름", 3: "보통", 4: "약간비만", 5: "매우비만"}
#         df["body_perception_cat"] = df["oba_01z1"].map(map_lbl)
#         df["body_perception_cat"] = _ordered_cat(
#             df["body_perception_cat"], ["매우마름", "약간마름", "보통", "약간비만", "매우비만"]
#         )
#         df["oba_01z1"] = _fill_mode(_safe_num(df["oba_01z1"]))

#     # 체중조절 '시도여부' (1=줄이기,2=유지,3=늘리기,4=안함)
#     if "obb_01z1" in df.columns:
#         map_lbl = {1: "줄이려했다", 2: "유지하려했다", 3: "늘리려했다", 4: "조절해본적없다"}
#         df["weight_control_attempt_cat"] = df["obb_01z1"].map(map_lbl)
#         df["weight_control_attempt_cat"] = _ordered_cat(
#             df["weight_control_attempt_cat"], ["줄이려했다", "유지하려했다", "늘리려했다", "조절해본적없다"]
#         )
#         df["obb_01z1"] = _fill_mode(_safe_num(df["obb_01z1"]))

#     # 체중조절 방법(운동/식이/단식… 1/2 → 1/0) + 건강한 방법 비율
#     weight_methods = [
#         "obb_02a1","obb_02b1","obb_02c1","obb_02d1",
#         "obb_02e1","obb_02f1","obb_02g1","obb_02h1","obb_02i1"
#     ]
#     exist = []
#     for c in weight_methods:
#         if c in df.columns:
#             out = c + "_bin"
#             df[out] = df[c].map(_BIN_YN)
#             df[out] = _fill_mode(df[out])
#             exist.append(out)

#     if exist:
#         # '건강한 방법'(운동+식이)을 단순 지표로
#         healthy = [x for x in exist if x.startswith("obb_02a1") or x.startswith("obb_02b1")]
#         if healthy:
#             df["healthy_method_ratio"] = df[healthy].sum(axis=1) / len(healthy)

#     return df

# # -----------------------------------
# # 3) 구강/치과 관련
# # -----------------------------------
# def _feature_oral(df):
#     df = df.copy()

#     # 최근치과방문 사유 (장벽 요인)
#     if "ore_03z2" in df.columns:
#         map_lbl = {
#             1: "시간없음", 2: "증상경미", 3: "경제적이유", 4: "교통/거리",
#             5: "대기시간", 6: "신체/예약어려움", 7: "치료두려움", 8: "기타"
#         }
#         df["dental_visit_barrier_cat"] = df["ore_03z2"].map(map_lbl)
#         df["dental_visit_barrier_cat"] = _ordered_cat(
#             df["dental_visit_barrier_cat"],
#             ["시간없음","증상경미","경제적이유","교통/거리","대기시간","신체/예약어려움","치료두려움","기타"]
#         )

#     # 점심 후 양치 여부 (1/2/3) → 이진 + 카테고리
#     if "ord_01d2" in df.columns:
#         lbl = {1: "예", 2: "아니요", 3: "점심식사안함"}
#         df["brush_after_lunch_cat"] = df["ord_01d2"].map(lbl)
#         df["brush_after_lunch_cat"] = _ordered_cat(df["brush_after_lunch_cat"], ["예","아니요","점심식사안함"])
#         df["brush_after_lunch_bin"] = df["ord_01d2"].map({1: 1, 2: 0, 3: 0})
#         df["brush_after_lunch_bin"] = _fill_mode(df["brush_after_lunch_bin"])

#     # 양치 불가 이유 (저녁 기준) 1~4 → 카테고리
#     if "ord_01f3" in df.columns:
#         lbl = {1:"예", 2:"아니요", 3:"저녁/수면없음"}  # 제공 정의 기반
#         df["brush_impossible_evening_cat"] = df["ord_01f3"].map(lbl)
#         df["brush_impossible_evening_cat"] = _ordered_cat(
#             df["brush_impossible_evening_cat"], ["예","아니요","저녁/수면없음"]
#         )

#     # 구강건강관리 실천(양치불가 사유) 1~4 → 카테고리
#     if "ord_05z1" in df.columns:
#         lbl = {1:"시간부족", 2:"장소없음", 3:"주변사람없음", 4:"필요성못느낌"}
#         df["oral_hygiene_barrier_cat"] = df["ord_05z1"].map(lbl)
#         df["oral_hygiene_barrier_cat"] = _ordered_cat(
#             df["oral_hygiene_barrier_cat"], ["시간부족","장소없음","주변사람없음","필요성못느낌"]
#         )

#     # 주관적 구강건강 1~5 (Ordered)
#     if "ora_01z1" in df.columns:
#         lbl = {1:"매우좋음", 2:"좋음", 3:"보통", 4:"나쁨", 5:"매우나쁨"}
#         df["subjective_oral_health_cat"] = _ordered_cat(
#             pd.Series(df["ora_01z1"]).map(lbl), lbl
#         )
#         df["ora_01z1"] = _fill_mode(_safe_num(df["ora_01z1"]))

#     # 치과치료 필요 불편도 1~5 (Ordered)
#     if "orb_01z1" in df.columns:
#         lbl = {1:"매우불편", 2:"불편", 3:"그저그렇다", 4:"별로불편X", 5:"전혀불편X"}
#         df["dental_discomfort_cat"] = _ordered_cat(
#             pd.Series(df["orb_01z1"]).map(lbl), lbl
#         )
#         df["orb_01z1"] = _fill_mode(_safe_num(df["orb_01z1"]))

#     return df

# # -----------------------------------
# # 통합 엔트리포인트
# # -----------------------------------
# def apply_my_features(
#     df: pd.DataFrame,
#     *,
#     weight_col: str | None = None,   # BMI 직접 계산 시 체중 컬럼명
#     copy: bool = True,
#     keep_original: bool = True,
#     output: str = "both",            # "both" | "model" | "human"
#     unknown_value: int = 0           # 라벨 미일치/결측 시 코딩값
# ) -> pd.DataFrame:
#     """
#     - 식생활/비만·체중조절/구강 파생 생성
#     - *_cat → *_code (1..N, Unknown=0) 자동 인코딩
#     - output 모드로 반환 형태 제어:
#         * "both"  : *_cat + *_code 모두 보존
#         * "model" : *_code(숫자)만 남기고 *_cat 제거
#         * "human" : *_cat(라벨)만 남기고 *_code 제거
#     """
#     base = _as_copy(df, copy)
#     out = base.copy()

#     # 1) 파생 생성
#     out = _feature_diet(out)
#     out = _feature_obesity_weight(out, weight_col=weight_col)
#     out = _feature_oral(out)

#     # 2) 카테고리 → 코드 인코딩 (모든 *_cat에 대해)
#     for c in [col for col in out.columns if col.endswith("_cat")]:
#         s = out[c]
#         if s.dtype.name != "category":
#             # 혹시 object면 카테고리로 변환
#             s = s.astype("category")
#         codes = s.cat.codes.replace(-1, np.nan)   # 카테고리 외 값/결측 → NaN
#         out[c.replace("_cat", "_code")] = (codes + 1).fillna(unknown_value).astype("int16")

#     # 3) 출력 모드 제어
#     if output == "model":
#         # 모델 입력용: 라벨(문자열) 제거, 숫자만 유지
#         drop_cols = [c for c in out.columns if c.endswith("_cat")]
#         out.drop(columns=drop_cols, inplace=True)
#     elif output == "human":
#         # 사람 읽기용: 코드(숫자) 제거, 라벨만 유지
#         drop_cols = [c for c in out.columns if c.endswith("_code")]
#         out.drop(columns=drop_cols, inplace=True)
#     # "both"는 둘 다 보존

#     if keep_original:
#         return out

#     # 4) 슬림 반환 (필요 컬럼만)
#     keep_cols = [c for c in out.columns if any(kw in c for kw in [
#         "breakfast_", "nutrition_", "height_m", "oba_bmi",
#         "body_perception_cat", "body_perception_code",
#         "weight_control_attempt_cat", "weight_control_attempt_code",
#         "_bin", "_score", "_code", "healthy_method_ratio",
#         "dental_", "brush_", "oral_hygiene_barrier_cat", "oral_hygiene_barrier_code",
#         "subjective_oral_health_cat", "subjective_oral_health_code",
#         "dental_discomfort_cat", "dental_discomfort_code"
#     ])]
#     return out[keep_cols]
