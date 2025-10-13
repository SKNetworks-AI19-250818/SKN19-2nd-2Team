"""
흡연 설문조사 Skip Logic 분석

목적:
1. 설문조사 skip logic 검증
2. churn 타겟과 변수들의 관계 파악
3. 논리적 결측값 vs 진짜 결측값 구분
4. 각 변수가 어떤 그룹에 유효한지 확인

작성자: vfxpedia (오흥재)
작성일: 2025-10-12
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# ============================================================
# 데이터 로딩
# ============================================================
def load_data():
    """데이터 로딩"""
    data_path = '../../../data/analy_data.csv'
    df = pd.read_csv(data_path)
    print(f"✅ 데이터 로딩 완료: {df.shape}")
    return df

# ============================================================
# 1. churn 타겟 분석
# ============================================================
def analyze_churn_target(df):
    """churn 타겟 분포 및 정의 확인"""
    print("\n" + "="*70)
    print("🎯 TARGET: churn 분포 분석")
    print("="*70)
    
    churn_dist = df['churn'].value_counts().sort_index()
    print("\n[churn 분포]")
    print(churn_dist)
    print(f"\n✅ 금연 성공 (churn=1): {(df['churn']==1).sum():,}명 ({(df['churn']==1).mean()*100:.2f}%)")
    print(f"❌ 금연 실패 (churn=0): {(df['churn']==0).sum():,}명 ({(df['churn']==0).mean()*100:.2f}%)")
    
    return churn_dist

# ============================================================
# 2. 흡연 상태 변수 분석
# ============================================================
def analyze_smoking_status(df):
    """
    핵심 변수 분석:
    - smf_01z1: 평생 담배 경험
    - sma_03z2: 현재 흡연 상태 ⭐
    """
    print("\n" + "="*70)
    print("🚬 흡연 상태 변수 분석")
    print("="*70)
    
    # Q1: 평생 담배 경험
    if 'smf_01z1' in df.columns:
        print("\n[Q1: smf_01z1] 평생 담배 제품 사용 경험")
        print("-" * 50)
        smf_dist = df['smf_01z1'].value_counts(dropna=False).sort_index()
        print(smf_dist)
        print(f"\n  1(예): {(df['smf_01z1']==1).sum():,}명 - Q2로 이동")
        print(f"  2(아니오): {(df['smf_01z1']==2).sum():,}명 - Q8로 건너뛰기 ⚠️")
        print(f"  결측값: {df['smf_01z1'].isna().sum():,}명")
    
    # Q2-1: 현재 흡연 상태 (핵심!)
    if 'sma_03z2' in df.columns:
        print("\n[Q2-1: sma_03z2] 일반담배 현재 흡연 상태 ⭐⭐⭐")
        print("-" * 50)
        sma_dist = df['sma_03z2'].value_counts(dropna=False).sort_index()
        print(sma_dist)
        print(f"\n  1(매일 피운다): {(df['sma_03z2']==1).sum():,}명")
        print(f"  2(가끔 피운다): {(df['sma_03z2']==2).sum():,}명")
        print(f"  3(과거 흡연, 현재 안 피움): {(df['sma_03z2']==3).sum():,}명 ⭐ 금연 성공!")
        print(f"  결측값: {df['sma_03z2'].isna().sum():,}명")
    
    return smf_dist if 'smf_01z1' in df.columns else None, \
           sma_dist if 'sma_03z2' in df.columns else None

# ============================================================
# 3. churn과 sma_03z2의 관계 (핵심!)
# ============================================================
def analyze_churn_vs_smoking_status(df):
    """
    churn 타겟이 어떻게 생성되었는지 확인
    가설: sma_03z2 == 3 → churn = 1
    """
    print("\n" + "="*70)
    print("🔍 churn vs sma_03z2 교차 분석 (핵심!)")
    print("="*70)
    
    if 'sma_03z2' not in df.columns:
        print("❌ sma_03z2 변수가 없습니다")
        return None
    
    # 교차표
    crosstab = pd.crosstab(
        df['sma_03z2'], 
        df['churn'], 
        dropna=False,
        margins=True
    )
    print("\n[교차표: sma_03z2 vs churn]")
    print(crosstab)
    
    # 비율 계산
    print("\n[금연 성공률 (churn=1 비율)]")
    for status in [1, 2, 3]:
        if status in df['sma_03z2'].values:
            subset = df[df['sma_03z2'] == status]
            success_rate = (subset['churn'] == 1).mean() * 100
            status_name = {1: "매일 피운다", 2: "가끔 피운다", 3: "과거 흡연, 현재 안 피움"}
            print(f"  sma_03z2={status} ({status_name[status]}): {success_rate:.2f}%")
    
    # 결측값의 금연 성공률
    na_subset = df[df['sma_03z2'].isna()]
    if len(na_subset) > 0:
        na_success_rate = (na_subset['churn'] == 1).mean() * 100
        print(f"  sma_03z2=결측값 (비흡연자?): {na_success_rate:.2f}%")
    
    return crosstab

# ============================================================
# 4. 금연 관련 변수들의 Skip Logic
# ============================================================
def analyze_quit_smoking_variables(df):
    """
    금연 관련 변수들이 어떤 그룹에만 유효한지 확인
    - smd_01z3: 금연계획 (현재 흡연자만)
    - smd_02z3: 금연시도 (현재 흡연자만)
    - smb_09z1: 금연기간 (과거 흡연자만)
    """
    print("\n" + "="*70)
    print("📊 금연 관련 변수 Skip Logic 분석")
    print("="*70)
    
    # smd_01z3: 금연계획
    if 'smd_01z3' in df.columns:
        print("\n[smd_01z3] 금연계획 (현재 흡연자만 답변)")
        print("-" * 50)
        
        # 현재 흡연자 vs 과거 흡연자
        current_smokers = df[df['sma_03z2'].isin([1, 2])]  # 매일 or 가끔
        past_smokers = df[df['sma_03z2'] == 3]  # 과거 흡연, 현재 안 피움
        
        print(f"  현재 흡연자 (sma_03z2=1,2): {len(current_smokers):,}명")
        print(f"    - smd_01z3 응답: {current_smokers['smd_01z3'].notna().sum():,}명")
        print(f"    - smd_01z3 결측: {current_smokers['smd_01z3'].isna().sum():,}명")
        
        print(f"\n  과거 흡연자 (sma_03z2=3): {len(past_smokers):,}명")
        print(f"    - smd_01z3 응답: {past_smokers['smd_01z3'].notna().sum():,}명")
        print(f"    - smd_01z3 결측: {past_smokers['smd_01z3'].isna().sum():,}명 ⚠️ 논리적 결측!")
        
        print("\n  💡 해석: 과거 흡연자는 이미 금연했으므로 '금연계획' 질문에 답하지 않음")
        print("  → 이 결측값은 '응답 안 함'이 아니라 '질문 대상이 아님'을 의미!")
    
    # smb_09z1: 금연기간
    if 'smb_09z1' in df.columns:
        print("\n[smb_09z1] 금연기간 (과거 흡연자만 답변) ⭐")
        print("-" * 50)
        
        print(f"  현재 흡연자 (sma_03z2=1,2): {len(current_smokers):,}명")
        print(f"    - smb_09z1 응답: {current_smokers['smb_09z1'].notna().sum():,}명")
        print(f"    - smb_09z1 결측: {current_smokers['smb_09z1'].isna().sum():,}명 ⚠️ 논리적 결측!")
        
        print(f"\n  과거 흡연자 (sma_03z2=3): {len(past_smokers):,}명")
        print(f"    - smb_09z1 응답: {past_smokers['smb_09z1'].notna().sum():,}명 ⭐")
        print(f"    - smb_09z1 결측: {past_smokers['smb_09z1'].isna().sum():,}명")
        
        print("\n  💡 해석: 현재 흡연자는 금연한 적이 없으므로 '금연기간' 질문에 답하지 않음")
        print("  → smb_09z1은 churn=1 (금연 성공자)에게만 의미 있는 변수!")
        
        # 금연기간별 분포
        if past_smokers['smb_09z1'].notna().sum() > 0:
            print("\n  [금연기간 분포]")
            quit_period = past_smokers['smb_09z1'].value_counts().sort_index()
            labels = {
                1: "1년 미만",
                2: "1-5년",
                3: "5-10년",
                4: "10-15년",
                5: "15-20년",
                6: "20년 이상"
            }
            for period, count in quit_period.items():
                print(f"    {int(period)}: {labels.get(period, '알 수 없음')} - {count:,}명")

# ============================================================
# 5. 변수 그룹핑 (논리적 유효성)
# ============================================================
def group_variables_by_validity(df):
    """
    각 변수가 어떤 그룹에 유효한지 정리
    """
    print("\n" + "="*70)
    print("📋 변수별 유효성 그룹핑")
    print("="*70)
    
    groups = {
        "모든 사람에게 유효": [
            "smf_01z1 (평생 담배 경험)",
            "sma_01z1 (평생 흡연량)",
            "smc_08z2 (가정 간접흡연)",
            "smc_10z2 (직장 간접흡연)",
            # 교육/경제 변수
            "sob_01z1 (교육수준)",
            "soa_01z1 (경제활동여부)",
            "soa_06z2 (직업분류)",
            "soa_07z1 (종사상지위)",
            "sod_02z3 (혼인상태)"
        ],
        
        "현재 흡연자에게만 유효 (sma_03z2=1,2)": [
            "smb_01z1 (매일흡연자 하루흡연량)",
            "smb_02z1 (가끔흡연자 월간일수)",
            "smb_03z1 (가끔흡연자 일평균흡연량)",
            "smd_01z3 (금연계획) ⭐",
            "smd_02z3 (금연시도) ⭐"
        ],
        
        "과거 흡연자에게만 유효 (sma_03z2=3)": [
            "smb_04z1 (과거 흡연기간_년)",
            "smb_05z1 (과거 흡연기간_월)",
            "smb_06z1 (과거 하루평균흡연량)",
            "smb_09z1 (금연기간) ⭐⭐⭐"
        ]
    }
    
    for group_name, variables in groups.items():
        print(f"\n[{group_name}]")
        for var in variables:
            print(f"  - {var}")
    
    print("\n" + "="*70)
    print("💡 핵심 인사이트")
    print("="*70)
    print("""
1. churn=1 (금연 성공)의 핵심 변수: smb_09z1 (금연기간)
   → 금연 성공자들의 특성을 가장 잘 나타냄

2. churn=0 (현재 흡연자)의 예측 변수:
   → smd_01z3 (금연계획), smd_02z3 (금연시도)
   → 이 사람들이 미래에 금연할지 예측 가능

3. 논리적 결측값 주의!
   → 결측값 = 응답 안 함 OR skip logic으로 질문 안 받음
   → 단순 fillna()는 위험! 그룹별로 다르게 처리 필요
""")

# ============================================================
# 6. 교육/경제 변수와 금연의 관계 (귀하의 담당!)
# ============================================================
def analyze_education_economy_smoking(df):
    """
    교육수준, 경제활동과 금연 성공의 관계
    """
    print("\n" + "="*70)
    print("📚 교육/경제 변수와 금연 성공의 관계")
    print("="*70)
    
    # sob_01z1: 교육수준
    if 'sob_01z1' in df.columns:
        print("\n[sob_01z1] 교육수준별 금연 성공률")
        print("-" * 50)
        edu_churn = df.groupby('sob_01z1')['churn'].agg(['count', 'sum', 'mean'])
        edu_churn.columns = ['총인원', '금연성공', '성공률']
        edu_churn['성공률'] = edu_churn['성공률'] * 100
        print(edu_churn)
        
        print("\n  💡 가설: 교육 수준이 높을수록 금연 성공률이 높다?")
    
    # soa_01z1: 경제활동 여부
    if 'soa_01z1' in df.columns:
        print("\n[soa_01z1] 경제활동 여부별 금연 성공률")
        print("-" * 50)
        econ_churn = df.groupby('soa_01z1')['churn'].agg(['count', 'sum', 'mean'])
        econ_churn.columns = ['총인원', '금연성공', '성공률']
        econ_churn['성공률'] = econ_churn['성공률'] * 100
        print(econ_churn)
        
        print("\n  💡 가설: 경제활동 안정성이 높을수록 금연 성공률이 높다?")

# ============================================================
# 메인 실행
# ============================================================
if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚬 흡연 설문조사 Skip Logic 분석 시작")
    print("="*70)
    
    # 데이터 로딩
    df = load_data()
    
    # 분석 실행
    analyze_churn_target(df)
    analyze_smoking_status(df)
    analyze_churn_vs_smoking_status(df)
    analyze_quit_smoking_variables(df)
    group_variables_by_validity(df)
    analyze_education_economy_smoking(df)
    
    print("\n" + "="*70)
    print("✅ 분석 완료!")
    print("="*70)
    print("""
다음 단계:
1. 교육/경제 변수 심층 분석
2. Feature Engineering (논리적 결측값 처리)
3. 모델링 (그룹별 예측 모델)
""")
