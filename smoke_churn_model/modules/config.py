from pathlib import Path

# 프로젝트 최상위 디렉토리
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# 데이터 경로
DATA_DIR = ROOT_DIR / "data"

# 모델 경로
MODEL_DIR = ROOT_DIR / "ml" / "models"

print(f"ROOT_DIR: {ROOT_DIR}")
print(f"DATA_DIR: {DATA_DIR}")
print(f"MODEL_DIR: {MODEL_DIR}")
