from pathlib import Path

# 프로젝트 최상위 디렉토리
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# 데이터 경로
DATA_DIR = ROOT_DIR / "data"

# 모델 경로
MODEL_DIR = ROOT_DIR / "smoke_churn_model" / "resource"
