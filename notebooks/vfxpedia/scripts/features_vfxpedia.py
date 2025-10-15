"""
Feature Engineering: 교육/경제 변수 (vfxpedia)

담당자: vfxpedia (오흥재)
작성일: 2025-10-13
목적: 교육수준, 경제활동, 직업, 혼인에 따른 금연 성공 상관관계 Feature 생성

최종 Feature 목록 (6개):
1. education_group: 교육수준 그룹 (0:저학력/1:중학력/2:고학력) [EDA 06 기반]
2. is_economically_active: 경제활동 여부 (0/1) [EDA 07 기반]
3. job_risk_group: 직업 위험도 (0:저위험/1:중위험/2:고위험/-1:해당없음) [EDA 07 기반]
4. occupation_type: 직업 유형 (화이트칼라/블루칼라/비경제활동) [일반 분류, 보조, 군인 포함]
5. is_employee: 임금근로자 여부 (0/1) [EDA 07 기반]
6. marital_stability: 혼인 안정성 (안정/미혼/불안정, 무응답 포함) [is_married보다 디테일]

변수 설명:
- sob_01z1: 교육수준 (1~8: 무학~대학원)
- soa_01z1: 경제활동 여부 (1:일함, 2:일 안함)
- soa_06z2: 직업분류 (1~10:직업군)
- soa_07z1: 종사상지위 (1:고용주/자영업, 2:임금근로자, 3:무급가족종사자)
- sod_02z3: 혼인상태 (1:유배우 ~ 5:별거)
"""

import numpy as np
import pandas as pd
from typing import Tuple


# ==================================================
# 1. 교육수준 그룹 - EDA 06번 기반
# ==================================================
def feature_education_group(df_merge: pd.DataFrame) -> pd.DataFrame:
    """
    교육수준을 3그룹으로 분류 (EDA 06번 역U자 패턴 기반)
    
    Parameters:
    -----------
    df_merge : DataFrame
        전처리된 데이터프레임
    
    Returns:
    --------
    df_merge : DataFrame
        'education_group' 컬럼이 추가된 데이터프레임
    
    생성 Feature:
    -------------
    education_group (int):
        - 0: 저학력_저위험 (무학~초등) - 흡연율 27.5%
        - 1: 중학력_고위험 (중학~전문대) - 흡연율 44.4%
        - 2: 고학력_중위험 (4년제~대학원) - 흡연율 33.3%
    
    원본 변수:
    ----------
    sob_01z1: 교육수준 (1~8)
        1: 무학, 2: 서당/한학, 3: 초등학교, 4: 중학교
        5: 고등학교, 6: 2~3년제대학, 7: 4년제대학, 8: 대학원이상
    """
    conditions = [
        df_merge['sob_01z1'] <= 3,  # 무학(1), 서당/한학(2), 초등(3)
        df_merge['sob_01z1'] <= 6,  # 중학(4), 고등(5), 전문대(6)
        df_merge['sob_01z1'] >= 7   # 4년제(7), 대학원(8)
    ]
    choices = [0, 1, 2]
    df_merge['education_group'] = np.select(conditions, choices, default=np.nan)
    
    return df_merge


# ==================================================
# 2. 경제활동 여부
# ==================================================
def feature_is_economically_active(df_merge: pd.DataFrame) -> pd.DataFrame:
    """
    경제활동 여부 이진 분류
    
    Parameters:
    -----------
    df_merge : DataFrame
        전처리된 데이터프레임
    
    Returns:
    --------
    df_merge : DataFrame
        'is_economically_active' 컬럼이 추가된 데이터프레임
    
    생성 Feature:
    -------------
    is_economically_active (int):
        - 1: 경제활동 (취업자)
        - 0: 비경제활동
    
    원본 변수:
    ----------
    soa_01z1: 경제활동 여부
        1: 일함 (취업)
        2: 일 안함 (비경제활동)
    
    EDA 근거:
    ---------
    - EDA 07번: 경제활동 여부에 따른 금연 성공률 차이 13.75%p
    """
    df_merge['is_economically_active'] = np.where(
        df_merge['soa_01z1'] == 1, 1, 0
    )
    
    return df_merge


# ==================================================
# 3. 직업 위험도 - EDA 07번 기반 (금연 성공률 기준)
# ==================================================
def feature_job_risk_group(df_merge: pd.DataFrame) -> pd.DataFrame:
    """
    직업을 금연 성공률 기반 위험도로 분류 (EDA 07번 기반)
    
    Parameters:
    -----------
    df_merge : DataFrame
        전처리된 데이터프레임
    
    Returns:
    --------
    df_merge : DataFrame
        'job_risk_group' 컬럼이 추가된 데이터프레임
    
    생성 Feature:
    -------------
    job_risk_group (int):
        - 0: 저위험_고성공 (농림어업, 전문가, 관리자) - 53~62%
        - 1: 중위험 (단순노무, 사무, 기계조작, 판매) - 47~52%
        - 2: 고위험_저성공 (서비스, 기능원, 군인) - 40~45%
        - -1: 해당없음 (비경제활동자)
    
    원본 변수:
    ----------
    soa_06z2: 직업분류 (1~10)
        1: 농림어업, 2: 전문가, 3: 관리자, 4: 단순노무, 5: 사무
        6: 기계조작, 7: 판매, 8: 서비스, 9: 기능원, 10: 군인
    
    EDA 근거:
    ---------
    - EDA 07번: 직업별 금연 성공률 최대 22.71%p 차이
    """
    conditions = [
        df_merge['soa_06z2'].isin([1, 2, 3]),      # 농림어업, 전문가, 관리자
        df_merge['soa_06z2'].isin([4, 5, 6, 7]),   # 단순노무, 사무, 기계조작, 판매
        df_merge['soa_06z2'].isin([8, 9, 10])      # 서비스, 기능원, 군인
    ]
    choices = [0, 1, 2]
    df_merge['job_risk_group'] = np.select(conditions, choices, default=-1)
    
    return df_merge


# ==================================================
# 4. 직업 유형 - 일반 분류 (보조 변수)
# ==================================================
def feature_occupation_type(df_merge: pd.DataFrame) -> pd.DataFrame:
    """
    직업을 일반적인 유형으로 분류 (보조 변수)
    
    Parameters:
    -----------
    df_merge : DataFrame
        전처리된 데이터프레임
    
    Returns:
    --------
    df_merge : DataFrame
        'occupation_type' 컬럼이 추가된 데이터프레임
    
    생성 Feature:
    -------------
    occupation_type (str):
        - '화이트칼라': 관리자, 전문가, 사무직
        - '블루칼라': 서비스, 판매, 농림어업, 기능원, 장치조작, 단순노무, 군인, 기타
        - '비경제활동': 미취업자
    
    원본 변수:
    ----------
    soa_06z2: 직업분류 (1~10)
        1: 농림어업, 2: 전문가, 3: 관리자, 4: 단순노무, 5: 사무
        6: 기계조작, 7: 판매, 8: 서비스, 9: 기능원, 10: 군인
        88: 비경제활동
    
    분류 근거:
    ----------
    - 화이트칼라: 주로 사무 환경, 정신 노동 중심
    - 블루칼라: 주로 육체 노동, 서비스 노동 중심 (군인, 무응답 포함)
    - 비경제활동: 직업 없음
    """
    conditions = [
        df_merge['soa_06z2'].isin([2, 3, 5]),    # 전문가, 관리자, 사무직
        df_merge['soa_06z2'] == 88                # 비경제활동
    ]
    choices = ['white_color', 'inactive']
    # 나머지는 모두 blue_color (군인, 무응답 포함)
    df_merge['occupation_type'] = np.select(conditions, choices, default='blue_color')
    
    return df_merge


# ==================================================
# 5. 임금근로자 여부 - EDA 07번 기반
# ==================================================
def feature_is_employee(df_merge: pd.DataFrame) -> pd.DataFrame:
    """
    임금근로자 여부 이진 분류 (EDA 07번 기반)
    
    Parameters:
    -----------
    df_merge : DataFrame
        전처리된 데이터프레임
    
    Returns:
    --------
    df_merge : DataFrame
        'is_employee' 컬럼이 추가된 데이터프레임
    
    생성 Feature:
    -------------
    is_employee (int):
        - 0: 자영업/고용주/무급가족 (금연 성공률 55.6%)
        - 1: 임금근로자 (금연 성공률 48.22%)
    
    원본 변수:
    ----------
    soa_07z1: 종사상지위 (1~3)
        1: 고용주/자영업
        2: 임금근로자
        3: 무급가족종사자
    
    EDA 근거:
    ---------
    - EDA 07번: 임금근로자와 비임금근로자 간 금연 성공률 차이 7.46%p
    """
    df_merge['is_employee'] = np.where(
        df_merge['soa_07z1'] == 2, 1, 0
    )
    
    return df_merge


# ==================================================
# 6. 혼인 안정성
# ==================================================
def feature_marital_stability(df_merge: pd.DataFrame) -> pd.DataFrame:
    """
    혼인 상태를 안정성 기준으로 분류
    
    Parameters:
    -----------
    df_merge : DataFrame
        전처리된 데이터프레임
    
    Returns:
    --------
    df_merge : DataFrame
        'marital_stability' 컬럼이 추가된 데이터프레임
    
    생성 Feature:
    -------------
    marital_stability (str):
        - '안정': 유배우 (배우자와 함께 생활)
        - '미혼': 미혼 (결혼 경험 없음)
        - '불안정': 사별, 이혼, 별거, 기타(무응답) (배우자와 분리)
    
    원본 변수:
    ----------
    sod_02z3: 혼인상태
        1: 유배우, 2: 미혼, 3: 사별, 4: 이혼, 5: 별거, 7/9: 무응답
    
    분류 근거:
    ----------
    - 안정: 배우자의 사회적 지지 가능
    - 미혼: 배우자 없음, 다른 사회적 네트워크 의존
    - 불안정: 배우자와의 분리로 인한 스트레스 가능성 (무응답 포함)
    """
    conditions = [
        df_merge['sod_02z3'] == 1,                # 유배우
        df_merge['sod_02z3'] == 2                 # 미혼
    ]
    choices = ['stable', 'single']
    # 나머지는 모두 'unstable'으로 (사별, 이혼, 별거, 무응답 포함)
    df_merge['marital_stability'] = np.select(conditions, choices, default='unstable')
    
    return df_merge


# ==================================================
# 통합 실행 함수
# ==================================================
def create_vfxpedia_features(df_merge: pd.DataFrame, verbose: bool = True) -> Tuple[pd.DataFrame, dict]:
    """
    모든 Feature를 한 번에 생성하고 통계 정보 반환
    
    Parameters:
    -----------
    df_merge : DataFrame
        전처리된 데이터프레임
    verbose : bool, default=True
        생성 정보 출력 여부
    
    Returns:
    --------
    df_merge : DataFrame
        Feature가 추가된 데이터프레임
    stats : dict
        각 Feature의 통계 정보
    """
    # Feature 생성
    df_merge = feature_education_group(df_merge)
    df_merge = feature_is_economically_active(df_merge)
    df_merge = feature_job_risk_group(df_merge)
    df_merge = feature_occupation_type(df_merge)
    df_merge = feature_is_employee(df_merge)
    df_merge = feature_marital_stability(df_merge)
    
    # 통계 정보 수집
    stats = {
        'education_group': {
            'count': df_merge['education_group'].notna().sum(),
            'distribution': df_merge['education_group'].value_counts().to_dict()
        },
        'is_economically_active': {
            'count': df_merge['is_economically_active'].notna().sum(),
            'distribution': df_merge['is_economically_active'].value_counts().to_dict()
        },
        'job_risk_group': {
            'count': df_merge['job_risk_group'].notna().sum(),
            'distribution': df_merge['job_risk_group'].value_counts().to_dict()
        },
        'occupation_type': {
            'count': df_merge['occupation_type'].notna().sum(),
            'distribution': df_merge['occupation_type'].value_counts().to_dict()
        },
        'is_employee': {
            'count': df_merge['is_employee'].notna().sum(),
            'distribution': df_merge['is_employee'].value_counts().to_dict()
        },
        'marital_stability': {
            'count': df_merge['marital_stability'].notna().sum(),
            'distribution': df_merge['marital_stability'].value_counts().to_dict()
        }
    }
    
    if verbose:
        print("=" * 60)
        print("✅ vfxpedia Feature 생성 완료!")
        print("=" * 60)
        print(f"총 6개 Feature 생성:")
        for feature_name, feature_stats in stats.items():
            print(f"  - {feature_name}: {feature_stats['count']:,}개")
        print("=" * 60)
    
    return df_merge, stats


# ==================================================
# 사용 예시
# ==================================================
if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════╗
║  vfxpedia Feature Engineering Module                   ║
╚════════════════════════════════════════════════════════╝

📌 담당자: 오흥재 (vfxpedia)

📊 생성 Feature (6개):
  1. education_group          : 교육수준 (0:저/1:중/2:고) [EDA 06]
  2. is_economically_active   : 경제활동 (0/1) [EDA 07]
  3. job_risk_group           : 직업 위험도 (0:저/1:중/2:고/-1:해당없음) [EDA 07]
  4. occupation_type          : 직업 유형 (화이트칼라/블루칼라/비경제활동) [보조]
  5. is_employee              : 임금근로자 (0/1) [EDA 07]
  6. marital_stability        : 혼인 안정성 (안정/미혼/불안정)

💻 사용법:
  # 방법 1: 통합 함수로 한번에 생성
  from features_vfxpedia import create_vfxpedia_features
  df = create_vfxpedia_features(df)
  
  # 방법 2: 개별 함수로 하나씩 생성
  from features_vfxpedia import feature_education_group
  df = feature_education_group(df)

🎯 목적:
  - 교육수준에 따른 흡연율 상관관계 분석
  - 경제활동에 따른 금연 성공 상관관계 분석
  - 각 Feature의 독립적 영향력 및 조합 효과 분석
  
📈 분석 방향:
  - 개별 Feature의 금연 성공률 차이
  - 2-way, 3-way 조합 패턴 발견
  - Decision Tree/Random Forest로 최적 조합 탐색
""")
