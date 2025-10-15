# utils/model_loader.py
from pathlib import Path
import json
import joblib
import pandas as pd

# --- 경로 탐색(스트림릿 내부 우선) ---
ROOT = Path(__file__).resolve().parents[2]
CANDIDATE_DIRS = [
    ROOT / "streamlit" / "results",
    ROOT / "notebooks" / "team" / "results",
]

def _pick_existing_dir():
    for d in CANDIDATE_DIRS:
        if d.exists():
            return d
    return None

ARTIF_DIR = _pick_existing_dir()
if ARTIF_DIR is None:
    raise FileNotFoundError("결과 디렉터리를 찾을 수 없습니다. streamlit/results 또는 notebooks/team/results 확인")

MODEL_FILE = ARTIF_DIR / "model_train_result.pkl"
COLS_FILE  = ARTIF_DIR / "columns.json"

_model = None
_cols = None

def load_model_and_cols():
    global _model, _cols
    if _model is None:
        if not MODEL_FILE.exists():
            raise FileNotFoundError(f"학습 모델 파일을 찾을 수 없습니다: {MODEL_FILE}")
        _model = joblib.load(MODEL_FILE)
    if _cols is None:
        _cols = json.loads(COLS_FILE.read_text(encoding="utf-8")) if COLS_FILE.exists() else None
    return _model, _cols


def predict_proba_from_features(x: dict) -> float:
    """
    x: 이미 숫자로 인코딩된 피처 dict (모델 입력과 가깝게 구성)
    누락 컬럼은 0으로 자동 보정하고, 여분 컬럼은 버립니다.
    """
    model, cols = load_model_and_cols()

    X = pd.DataFrame([x])

    if cols:
        # 1) 누락 컬럼 0 채우기
        missing = [c for c in cols if c not in X.columns]
        if missing:
            for c in missing:
                X[c] = 0
        # 2) 학습 컬럼 순서/집합으로 정렬 (여분 컬럼은 버림)
        X = X.reindex(columns=cols, fill_value=0)

    # 일부 모델은 predict_proba가 없을 수 있으므로 fallback
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0, 1]
    else:
        # decision_function을 0~1로 변환 (간단 스케일)
        import numpy as np
        z = model.decision_function(X)[0]
        proba = 1 / (1 + np.exp(-z))

    return float(proba)



# # utils/model_loader.py
# from pathlib import Path
# import json
# import joblib
# import pandas as pd

# # ---------------------------------------------------
# # 경로 탐색: 프로젝트 루트에서 여러 후보 경로를 순서대로 검사
# # ---------------------------------------------------
# _THIS_FILE = Path(__file__).resolve()
# PROJ_ROOT = _THIS_FILE.parents[2]  # <repo_root>/  (…/SKN19-2nd-2Team)

# CANDIDATE_MODEL_PATHS = [
#     PROJ_ROOT / "notebooks" / "team" / "results" / "model_train_result.pkl",
#     PROJ_ROOT / "notebooks" / "results" / "model_train_result.pkl",
#     PROJ_ROOT / "notebooks" / "team" / "model_train_result.pkl",
# ]

# CANDIDATE_COLS_PATHS = [
#     PROJ_ROOT / "notebooks" / "team" / "results" / "columns.json",
#     PROJ_ROOT / "notebooks" / "results" / "columns.json",
#     PROJ_ROOT / "notebooks" / "team" / "columns.json",
# ]

# def _pick_first_existing(paths):
#     for p in paths:
#         if p.exists():
#             print(f"[model_loader] using: {p}")
#             return p
#     # 디버깅을 돕기 위해 후보 경로들을 모두 출력
#     raise FileNotFoundError(
#         "[model_loader] 학습 모델/컬럼 파일을 찾을 수 없습니다.\n" +
#         "\n".join(f"- {p}" for p in paths)
#     )

# MODEL_FILE = _pick_first_existing(CANDIDATE_MODEL_PATHS)
# COLS_FILE  = _pick_first_existing(CANDIDATE_COLS_PATHS)

# _model = None
# _cols = None

# def load_model_and_cols():
#     global _model, _cols
#     if _model is None:
#         _model = joblib.load(MODEL_FILE)  # pickle로 저장했어도 joblib.load로 로딩 가능
#     if _cols is None:
#         _cols = json.loads(COLS_FILE.read_text(encoding="utf-8"))
#     return _model, _cols

# def predict_proba_from_features(x: dict) -> float:
#     """
#     x: 모델이 학습된 '최종 피처 스키마'의 dict (이미 인코딩/전처리된 값)
#     return: class=1 확률(float)
#     """
#     model, cols = load_model_and_cols()
#     X = pd.DataFrame([x])
#     # 학습 당시 컬럼 순서/집합에 맞춤 (누락은 0으로 채움)
#     X = X.reindex(columns=cols, fill_value=0)
#     proba = model.predict_proba(X)[0, 1]
#     return float(proba)





# # utils/model_loader.py
# from pathlib import Path
# import sys
# import json
# import joblib
# import pandas as pd

# # -----------------------------
# # 경로 설정: notebooks/team 쪽을 import 경로에 추가
# # -----------------------------
# ROOT = Path(__file__).resolve().parents[1]  # 프로젝트 루트 (streamlit/ 상위)
# TEAM_DIR = ROOT / "notebooks" / "team"
# RESULTS_DIR = TEAM_DIR / "results"
# MODULES_DIR = TEAM_DIR / "modules"

# if str(TEAM_DIR) not in sys.path:
#     sys.path.append(str(TEAM_DIR))         # notebooks/team
# if str(MODULES_DIR) not in sys.path:
#     sys.path.append(str(MODULES_DIR))      # notebooks/team/modules

# # 학습 결과 파일
# MODEL_FILE = RESULTS_DIR / "model_train_result.pkl"
# COLS_FILE  = RESULTS_DIR / "columns.json"  # 학습시 사용한 최종 컬럼 순서

# # 피처 엔지니어링 함수
# try:
#     # modules/features_sangmin.py 안의 함수 이름에 맞춰 import
#     from features_sangmin import apply_my_features
#     HAS_PIPELINE = True
# except Exception as e:
#     print(f"[경고] 피처 엔지니어링 모듈을 불러오지 못했습니다: {e}")
#     HAS_PIPELINE = False

# _model = None
# _cols = None

# def load_model_and_cols():
#     """모델과 columns.json 로드"""
#     global _model, _cols
#     if _model is None:
#         if not MODEL_FILE.exists():
#             raise FileNotFoundError(f"학습 모델 파일을 찾을 수 없습니다: {MODEL_FILE}")
#         _model = joblib.load(MODEL_FILE)
#     if _cols is None:
#         if COLS_FILE.exists():
#             _cols = json.loads(COLS_FILE.read_text(encoding="utf-8"))
#         else:
#             print("[경고] columns.json이 없어 있는 컬럼만 사용합니다.")
#             _cols = None
#     return _model, _cols


# # -----------------------------
# # ❶ (권장) 원시 입력(dict) → 전처리 → 예측
# #    학습 때의 파이프라인을 그대로 사용
# # -----------------------------
# def predict_proba_from_raw(user_input_dict: dict) -> float:
#     """
#     user_input_dict: 폼에서 받은 '원시' 입력(데이터프레임 한 행으로 만들 수 있는 딕셔너리, 한글 컬럼명 포함 가능)
#     return: class=1 확률(float)
#     """
#     model, cols = load_model_and_cols()

#     if not HAS_PIPELINE:
#         # 파이프라인을 못 읽는 경우엔 아래 ❷ 함수로 폴백
#         return predict_proba_from_features(user_input_dict)

#     # 1) 폼 입력을 DF로
#     df_input = pd.DataFrame([user_input_dict])

#     # 2) 학습과 동일한 피처 엔지니어링/인코딩
#     df_feat = apply_my_features(df_input)   # <- preprocess.py에서 보신 것과 동일

#     # 3) 학습 컬럼 순서 맞추기(누락컬럼은 0 채우기)
#     if cols:
#         missing = set(cols) - set(df_feat.columns)
#         if missing:
#             print(f"[경고] 누락 컬럼 자동 채움: {missing}")
#         X = df_feat.reindex(columns=cols, fill_value=0)
#     else:
#         X = df_feat

#     # 4) 예측
#     proba = model.predict_proba(X)[0, 1]
#     return float(proba)


# # -----------------------------
# # ❷ (폴백) 이미 인코딩된 dict → reindex → 예측
# #    (파이프라인 없을 때 임시로 사용)
# # -----------------------------
# def predict_proba_from_features(x: dict) -> float:
#     """
#     x: 이미 숫자로 인코딩된 피처 dict (모델 입력과 동일한 컬럼들이 key)
#     return: class=1 확률(float)
#     """
#     model, cols = load_model_and_cols()
#     X = pd.DataFrame([x])
#     if cols:
#         missing = set(cols) - set(X.columns)
#         if missing:
#             print(f"[경고] 누락된 컬럼 자동 채움: {missing}")
#         X = X.reindex(columns=cols, fill_value=0)
#     proba = model.predict_proba(X)[0, 1]
#     return float(proba)


# # utils/model_loader.py
# from pathlib import Path
# import json
# import joblib
# import pandas as pd

# # ======================================
# # 수정된 경로 설정
# # ======================================
# # 현재 파일 기준: SKN19-2nd-2Team/streamlit/utils/model_loader.py
# # → 프로젝트 루트(SKN19-2nd-2Team)로 올라가서 notebooks/team/results로 접근
# ROOT_DIR = Path(__file__).resolve().parents[2]
# ARTIF_DIR = ROOT_DIR / "notebooks" / "team" / "results"

# MODEL_FILE = ARTIF_DIR / "model_train_result.pkl"
# COLS_FILE = ARTIF_DIR / "columns.json"

# _model = None
# _cols = None

# def load_model_and_cols():
#     global _model, _cols
#     if _model is None:
#         if not MODEL_FILE.exists():
#             raise FileNotFoundError(f"학습 모델 파일을 찾을 수 없습니다: {MODEL_FILE}")
#         _model = joblib.load(MODEL_FILE)
#     if _cols is None and COLS_FILE.exists():
#         _cols = json.loads(COLS_FILE.read_text(encoding="utf-8"))
#     return _model, _cols


# def predict_proba_from_features(x: dict) -> float:
#     """
#     x: dict(모델 입력 피처명 -> 값)
#     return: class=1 확률(float)
#     """
#     model, cols = load_model_and_cols()
#     X = pd.DataFrame([x])
    
#     if cols:
#         # 학습 당시 컬럼 순서를 유지하면서 누락된 컬럼은 0으로 채움
#         missing = set(cols) - set(X.columns)
#         if missing:
#             print(f"[경고] 누락된 컬럼 자동 채움: {missing}")
#         X = X.reindex(columns=cols, fill_value=0)
#     else:
#         # 혹시 columns.json이 없으면 그냥 있는 값만 예측
#         print("[경고] columns.json이 없어 있는 값만 사용합니다.")
    
#     proba = model.predict_proba(X)[0, 1]
#     return float(proba)

