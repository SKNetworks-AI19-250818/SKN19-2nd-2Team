import pandas as pd
import numpy as np

# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np

# =========================================================
# 0) CODEMAP (코드북) — 중앙 관리
# =========================================================
CODEMAP = {
    # -------------------------
    # 1) 식생활 / 영양
    # -------------------------
    "nua_01z2": {  # 아침식사빈도
        1: "주5~7회",
        2: "주3~4회",
        3: "주1~2회",
        4: "거의안함(주0회)",
    },
    "nuc_01z2": {  # 영양표시 활용여부
        1: "예",
        2: "아니요",
    },
    "nuc_02z1": {  # 영양표시 인지여부
        1: "예",
        2: "아니요",
    },
    "nuc_03z1": {  # 영양관심여부
        1: "예",
        2: "아니요",
    },

    # -------------------------
    # 2) 비만 · 체중조절
    # -------------------------
    "oba_01z1": {  # 체형인지(자기평가)
        1: "매우마름",
        2: "약간마름",
        3: "보통",
        4: "약간비만",
        5: "매우비만",
    },
    "obb_01z1": {  # 체중조절 시도여부
        1: "줄이려했다",
        2: "유지하려했다",
        3: "늘리려했다",
        4: "조절해본적없다",
    },
    # 체중조절 방법(여러 문항) — 1=예, 2=아니요
    "obb_02a1": {1: "예", 2: "아니요"},  # 운동
    "obb_02b1": {1: "예", 2: "아니요"},  # 식이
    "obb_02c1": {1: "예", 2: "아니요"},
    "obb_02d1": {1: "예", 2: "아니요"},  # 단식
    "obb_02e1": {1: "예", 2: "아니요"},
    "obb_02f1": {1: "예", 2: "아니요"},
    "obb_02g1": {1: "예", 2: "아니요"},
    "obb_02h1": {1: "예", 2: "아니요"},
    "obb_02i1": {1: "예", 2: "아니요"},

    # -------------------------
    # 3) 구강/치과
    # -------------------------
    "ore_03z2": {  # 최근치과방문 이유(장벽)
        1: "시간없음",
        2: "증상경미",
        3: "경제적이유",
        4: "교통불편/거리멀음",
        5: "대기가길어서",
        6: "몸이불편/예약어려움",
        7: "치료두려움",
        8: "기타",
    },
    "ord_01d2": {  # 점심 후 양치 여부
        1: "예",
        2: "아니요",
        3: "어제 점심식사 하지 않음",
    },
    "ord_01f3": {  # 양치불가(저녁 기준)
        1: "예",
        2: "아니요",
        3: "어제 저녁식사 또는 잠자지 않음",
    },
    "ord_05z1": {  # 구강건강관리실천(양치불가 이유)
        1: "시간이 없어서",
        2: "칫솔질 할 장소가 없어서",
        3: "주변에 칫솔질을 하는 사람이 없어서",
        4: "필요성을 느끼지 못해서",
    },
    "ora_01z1": {  # 주관적구강건강
        1: "매우좋음",
        2: "좋음",
        3: "보통",
        4: "나쁨",
        5: "매우나쁨",
    },
    "orb_01z1": {  # 치과치료 필요 시 불편도
        1: "매우불편",
        2: "불편",
        3: "그저그렇다",
        4: "별로불편하지않다",
        5: "전혀불편하지않다",
    },
}

# =========================================================
# 1) 유틸
# =========================================================
_BIN_YN = {1: 1, 2: 0}  # 예/아니오 → 1/0

def _as_copy(df, copy=True):
    return df.copy() if copy else df

def _safe_num(s):
    return pd.to_numeric(s, errors="coerce")

def _fill_mode(s):
    try:
        return s.fillna(s.mode().iloc[0])
    except Exception:
        return s.fillna(s.dropna().iloc[0] if s.dropna().size else s)

def _ordered_cat(series, labels, add_unknown=True):
    """
    labels: 카테고리 '라벨 리스트'. 숫자 코드 리스트도 허용.
    - 숫자 코드 리스트가 들어오면, Unknown은 카테고리에 추가하지 않고 NaN으로 남겨서
      뒤 단계에서 unknown_value로 안전하게 치환되도록 함.
    - 문자열 라벨 리스트라면 'Unknown' 카테고리를 추가해도 무방.
    """
    if all(isinstance(x, (int, np.integer)) for x in labels):
        # 숫자 코드 기반 카테고리: Unknown/결측은 NaN으로 둔다.
        s = pd.to_numeric(series, errors="coerce")
        return pd.Categorical(s, categories=labels, ordered=True)
    else:
        cats = labels + (["Unknown"] if add_unknown and "Unknown" not in labels else [])
        s = series.astype("object").where(series.notna(), "Unknown")
        return pd.Categorical(s, categories=cats, ordered=True)

def _codes_for(src_col):
    return sorted(CODEMAP[src_col].keys()) if src_col in CODEMAP else None

def _cat_from_codebook(df, src_col, out_cat_col, make_label=False):
    """
    CODEMAP을 사용하여:
      - out_cat_col: '코드(숫자)' 값 기반 Ordered Categorical 생성
      - make_label=True면 *_label 문자열 라벨도 추가 생성
    """
    if src_col not in df.columns or src_col not in CODEMAP:
        return df
    codes = _codes_for(src_col)
    df[out_cat_col] = _ordered_cat(df[src_col], codes, add_unknown=False)
    if make_label:
        df[out_cat_col.replace("_cat", "_label")] = df[src_col].map(CODEMAP[src_col]).fillna("Unknown")
    return df

# =========================================================
# 2) 식생활
# =========================================================
def _feature_diet(df):
    df = df.copy()

    # 아침식사빈도 (CODEMAP 사용)
    if "nua_01z2" in df.columns and "nua_01z2" in CODEMAP:
        df = _cat_from_codebook(df, "nua_01z2", "breakfast_freq_cat", make_label=False)
        # 점수(높을수록 바람직): 주5~7회=3 … 거의안함=0
        df["breakfast_freq_score"] = df["nua_01z2"].replace({1: 3, 2: 2, 3: 1, 4: 0})
        df["breakfast_freq_score"] = df["breakfast_freq_score"].fillna(df["breakfast_freq_score"].median())

    # 영양표시 인지/활용/관심 (1/2 → 1/0)
    for raw, out in {
        "nuc_02z1": "nutrition_awareness_bin",
        "nuc_01z2": "nutrition_usage_bin",
        "nuc_03z1": "nutrition_interest_bin",
    }.items():
        if raw in df.columns:
            df[out] = df[raw].map(_BIN_YN)
            df[out] = _fill_mode(df[out])

    return df

# =========================================================
# 3) 비만·체중조절
# =========================================================
def _feature_obesity_weight(df, weight_col: str | None = None):
    """
    weight_col: BMI가 없고 체중이 따로 있을 때 체중 컬럼명 (예: 'oba_03z1' or 'weight_kg')
    """
    df = df.copy()

    # 신장(cm) → m
    if "oba_02z1" in df.columns:
        df["height_m"] = _safe_num(df["oba_02z1"]) / 100

    # BMI (있으면 median 대체, 없고 키/체중 있으면 계산)
    if "oba_bmi" in df.columns:
        df["oba_bmi"] = _safe_num(df["oba_bmi"])
        df["oba_bmi"] = df["oba_bmi"].fillna(df["oba_bmi"].median())
    else:
        if weight_col and weight_col in df.columns and "height_m" in df.columns:
            w = _safe_num(df[weight_col])
            h = _safe_num(df["height_m"])
            bmi = w / (h ** 2)
            df["oba_bmi"] = bmi
            df["oba_bmi"] = df["oba_bmi"].fillna(df["oba_bmi"].median())

    # 체형인지(자기평가) → CODEMAP 사용
    if "oba_01z1" in df.columns and "oba_01z1" in CODEMAP:
        df = _cat_from_codebook(df, "oba_01z1", "body_perception_cat", make_label=False)
        df["oba_01z1"] = _fill_mode(_safe_num(df["oba_01z1"]))

    # 체중조절 시도여부 → CODEMAP 사용
    if "obb_01z1" in df.columns and "obb_01z1" in CODEMAP:
        df = _cat_from_codebook(df, "obb_01z1", "weight_control_attempt_cat", make_label=False)
        df["obb_01z1"] = _fill_mode(_safe_num(df["obb_01z1"]))

    # 체중조절 방법(운동/식이/단식… 1/2 → 1/0) + 건강한 방법 비율
    weight_methods = [
        "obb_02a1", "obb_02b1", "obb_02c1", "obb_02d1",
        "obb_02e1", "obb_02f1", "obb_02g1", "obb_02h1", "obb_02i1",
    ]
    exist_bins = []
    for c in weight_methods:
        if c in df.columns:
            out = c + "_bin"
            df[out] = df[c].map(_BIN_YN)
            df[out] = _fill_mode(df[out])
            exist_bins.append(out)

    if exist_bins:
        # '건강한 방법'(운동+식이)을 단순 지표로
        healthy = [x for x in exist_bins if x.startswith("obb_02a1") or x.startswith("obb_02b1")]
        if healthy:
            df["healthy_method_ratio"] = df[healthy].sum(axis=1) / len(healthy)

    return df

# =========================================================
# 4) 구강/치과
# =========================================================
def _feature_oral(df):
    df = df.copy()

    # 최근치과방문 이유 → CODEMAP 사용
    if "ore_03z2" in df.columns and "ore_03z2" in CODEMAP:
        df = _cat_from_codebook(df, "ore_03z2", "dental_visit_barrier_cat", make_label=False)

    # 점심 후 양치 여부 → CODEMAP 사용 + 이진 파생 유지
    if "ord_01d2" in df.columns and "ord_01d2" in CODEMAP:
        df = _cat_from_codebook(df, "ord_01d2", "brush_after_lunch_cat", make_label=False)
        df["brush_after_lunch_bin"] = df["ord_01d2"].map({1: 1, 2: 0, 3: 0})
        df["brush_after_lunch_bin"] = _fill_mode(df["brush_after_lunch_bin"])

    # 양치불가(저녁) → CODEMAP 사용
    if "ord_01f3" in df.columns and "ord_01f3" in CODEMAP:
        df = _cat_from_codebook(df, "ord_01f3", "brush_impossible_evening_cat", make_label=False)

    # 구강건강관리 실천(양치불가 이유) → CODEMAP 사용
    if "ord_05z1" in df.columns and "ord_05z1" in CODEMAP:
        df = _cat_from_codebook(df, "ord_05z1", "oral_hygiene_barrier_cat", make_label=False)

    # 주관적 구강건강 1~5 → CODEMAP 사용
    if "ora_01z1" in df.columns and "ora_01z1" in CODEMAP:
        df = _cat_from_codebook(df, "ora_01z1", "subjective_oral_health_cat", make_label=False)
        df["ora_01z1"] = _fill_mode(_safe_num(df["ora_01z1"]))

    # 치과치료 불편도 1~5 → CODEMAP 사용
    if "orb_01z1" in df.columns and "orb_01z1" in CODEMAP:
        df = _cat_from_codebook(df, "orb_01z1", "dental_discomfort_cat", make_label=False)
        df["orb_01z1"] = _fill_mode(_safe_num(df["orb_01z1"]))

    return df

# =========================================================
# 5) 통합 엔트리포인트
# =========================================================
def apply_my_features(
    df: pd.DataFrame,
    *,
    weight_col: str | None = None,   # BMI 직접 계산 시 체중 컬럼명
    copy: bool = True,
    keep_original: bool = True,
    output: str = "both",            # "both" | "model" | "human"
    unknown_value: int = 0           # 라벨 미일치/결측 시 코딩값
) -> pd.DataFrame:
    """
    - 식생활/비만·체중조절/구강 파생 생성
    - *_cat → *_code (원본 '코드값' 보존, Unknown=unknown_value) 자동 인코딩
    - output 모드:
        * "both"  : *_cat + *_code 모두 보존
        * "model" : *_code(숫자)만 남기고 *_cat 제거
        * "human" : *_cat(라벨)만 남기고 *_code 제거
    """
    base = _as_copy(df, copy)
    out = base.copy()

    # 1) 파생 생성
    out = _feature_diet(out)
    out = _feature_obesity_weight(out, weight_col=weight_col)
    out = _feature_oral(out)

    # 2) 카테고리 → 코드 인코딩 (모든 *_cat에 대해)
    for c in [col for col in out.columns if col.endswith("_cat")]:
        s = out[c]
        # 범주형 보장
        if s.dtype.name != "category":
            s = s.astype("category")
        # s.cat.categories 가 숫자 코드 리스트(예: [1,2,3,4])이므로
        # cat.codes 는 0..K-1 이고, +1 하면 원본 코드값과 동일해짐 (카테고리 순서를 코드값 순서로 만들었기 때문)
        codes = s.cat.codes.replace(-1, np.nan)   # NaN/미지정은 -1 → NaN
        out[c.replace("_cat", "_code")] = (codes + 1).fillna(unknown_value).astype("int16")

    # 3) 출력 모드 제어
    if output == "model":
        drop_cols = [c for c in out.columns if c.endswith("_cat")]
        out.drop(columns=drop_cols, inplace=True)
    elif output == "human":
        drop_cols = [c for c in out.columns if c.endswith("_code")]
        out.drop(columns=drop_cols, inplace=True)
    # "both"는 둘 다 보존

    if keep_original:
        return out

    # 4) 슬림 반환 (필요 컬럼만)
    keep_cols = [c for c in out.columns if any(kw in c for kw in [
        "breakfast_", "nutrition_", "height_m", "oba_bmi",
        "body_perception_cat", "body_perception_code",
        "weight_control_attempt_cat", "weight_control_attempt_code",
        "_bin", "_score", "_code", "healthy_method_ratio",
        "dental_", "brush_", "oral_hygiene_barrier_cat", "oral_hygiene_barrier_code",
        "subjective_oral_health_cat", "subjective_oral_health_code",
        "dental_discomfort_cat", "dental_discomfort_code",
    ])]
    return out[keep_cols]