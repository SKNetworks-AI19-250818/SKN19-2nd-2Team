import pandas as pd
from pathlib import Path
data_dir = Path(__file__).resolve().parent

data_path = data_dir / "results/model_pred_result_analysis.csv"
df = pd.read_csv(data_path)
print(df.columns)

# 금연 성공자 평균
success_avg = pd.DataFrame({
    '특성': ['수면시간', '아침식사', '운동빈도', '스트레스'],
    '평균값': [7, 1, 4, 3]
})

# 데모 고객들 (원하면 CSV 로드로 바꿔도 됨)
patient_data_all = {
    '홍길동': {'수면시간': 5, '아침식사': 0, '운동빈도': 2, '스트레스': 5},
    '김철수': {'수면시간': 6, '아침식사': 1, '운동빈도': 3, '스트레스': 4}
}
