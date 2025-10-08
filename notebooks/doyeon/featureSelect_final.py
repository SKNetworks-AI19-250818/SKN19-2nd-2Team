import numpy as np
import pandas as pd

# 데이터 로드
df = pd.read_csv('../../data/analy_data.csv')

# 맡은 카테고리 안에서 드랍할 칼럼
drop_columns = [
    'drb_16z1', 'dre_03z1', 'dre_04z1',
    'pha_05z1', 'pha_06z1', 'pha_08z1', 'pha_09z1', 'phb_02z1', 'phb_03z1'
]

# 맡은 카테고리 안에서 사용할 칼럼 (결측치 제거 전) 지정
columns = {
    'dra_01z1':	'평생 음주 여부',
    'drb_01z3':	'연간 음주 빈도',
    'drb_03z1':	'한 번 섭취 시 음주량',
    'drb_04z1':	'월간 폭음 경험(남)',
    'drb_05z1':	'월간 폭음 경험(여)',
    'drg_01z3':	'절주 또는 금주계획 여부',
    'pha_04z1':	'고강도 신체활동 일수',
    'pha_07z1':	'중강도 신체활동 일수',
    'phb_01z1':	'걷기 실천 일수',
    'pha_11z1':	'최근 1주일 유연성 운동 실천',
    'churn': '금연 성공 여부'
}

dr_ph_columns = list(columns.keys())
dr_ph_df = df[dr_ph_columns]

# 피쳐 엔지니어링 - 피쳐 생성
# '월간 폭음 경험(남)', '월간 폭음 경험(여)' ['drb_04z1', 'drb_05z1'] -> '월간 폭음 경험' ['drb_binge_monthly'] 통합
dr_ph_df['sex'] = df['sex']
dr_ph_df['drb_binge_monthly'] = np.where(
    dr_ph_df['sex'] == 1, dr_ph_df['drb_04z1'], dr_ph_df['drb_05z1']
)
dr_ph_df.drop(['drb_04z1', 'drb_05z1', 'sex'], axis=1, inplace=True)

# 값변경
dr_ph_df['drb_01z3'] = dr_ph_df['drb_01z3'].replace(8, 1)
dr_ph_df['drb_03z1'] = dr_ph_df['drb_03z1'].replace(8, -1)
dr_ph_df['drb_binge_monthly'] = dr_ph_df['drb_binge_monthly'].replace(8, -1)

# NaN 변경
dr_ph_df.loc[dr_ph_df['drb_01z3'] >= 7, 'drb_01z3'] = np.nan
dr_ph_df.loc[dr_ph_df['drb_03z1'] >= 7, 'drb_03z1'] = np.nan
dr_ph_df.loc[dr_ph_df['drg_01z3'] >= 7, 'drg_01z3'] = np.nan
dr_ph_df.loc[dr_ph_df['pha_04z1'] >= 77, 'pha_04z1'] = np.nan
dr_ph_df.loc[dr_ph_df['pha_07z1'] >= 77, 'pha_07z1'] = np.nan
dr_ph_df.loc[dr_ph_df['phb_01z1'] >= 77, 'phb_01z1'] = np.nan
dr_ph_df.loc[dr_ph_df['pha_11z1'] >= 9, 'pha_11z1'] = np.nan
dr_ph_df.loc[dr_ph_df['drb_binge_monthly'] >= 7, 'drb_binge_monthly'] = np.nan

# 범주형 칼럼 object형 변환
dr_ph_df['dra_01z1'] = dr_ph_df['dra_01z1'].astype('object')

