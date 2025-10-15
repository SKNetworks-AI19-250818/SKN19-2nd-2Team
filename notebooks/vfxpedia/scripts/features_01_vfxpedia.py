"""
==================================================
교육 및 경제활동 Feature Engineering
작성자: vfxpedia
날짜: 2025-10-13
목적: 교육수준, 경제활동, 직업, 혼인 관련 Feature 생성

생성 Feature (6개):
1. education_group: 교육수준 그룹 (0:저학력/1:중학력/2:고학력)
2. is_economically_active: 경제활동 여부 (0/1)
3. job_risk_group: 직업 위험도 (0:저위험/1:중위험/2:고위험/-1:해당없음) [EDA 07 기반]
4. occupation_type: 직업 유형 (화이트칼라/블루칼라/비경제활동) [일반 분류, 보조, 군인 포함]
5. is_employee: 임금근로자 여부 (0/1)
6. marital_stability: 혼인 안정성 (안정/미혼/불안정, 무응답 포함)
==================================================
"""

import numpy as np
import pandas as pd


# ==================================================
# 내용: 교육수준 그룹 (저/중/고 학력) - EDA 06번 기반
# 함수명: feature_education_group
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
def feature_education_group(df_merge):
    """
    교육수준을 3그룹으로 분류 (EDA 06번 역U자 패턴 기반)
    - 0: 저학력_저위험 (무학~초등) - 흡연율 27.5%
    - 1: 중학력_고위험 (중학~전문대) - 흡연율 44.4%
    - 2: 고학력_중위험 (4년제~대학원) - 흡연율 33.3%
    
    변수: sob_01z1 (1~8)
    1: 무학, 2: 서당/한학, 3: 초등학교, 4: 중학교, 
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
# 내용: 경제활동 여부
# 함수명: feature_is_economically_active
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
def feature_is_economically_active(df_merge):
    """
    경제활동 여부 (0/1)
    - 1: 경제활동 (취업자)
    - 0: 비경제활동
    
    변수: soa_01z1
    1: 일함, 2: 일 안함
    """
    df_merge['is_economically_active'] = np.where(
        df_merge['soa_01z1'] == 1, 1, 0
    )
    
    return df_merge


# ==================================================
# 내용: 직업 위험도 그룹 - EDA 07번 기반 (금연 성공률 기준)
# 함수명: feature_job_risk_group
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
def feature_job_risk_group(df_merge):
    """
    직업을 금연 성공률 기반 위험도로 분류 (EDA 07번 기반)
    - 0: 저위험_고성공 (농림어업, 전문가, 관리자) - 53~62%
    - 1: 중위험 (단순노무, 사무, 기계조작, 판매) - 47~52%
    - 2: 고위험_저성공 (서비스, 기능원, 군인) - 40~45%
    - -1: 해당없음 (비경제활동자)
    
    변수: soa_06z2
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
# 내용: 직업 유형 (화이트칼라/블루칼라/비경제활동) - 일반 분류, 보조 변수
# 함수명: feature_occupation_type
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
def feature_occupation_type(df_merge):
    """
    직업을 일반적인 유형으로 분류 (보조 변수)
    - 화이트칼라: 관리자, 전문가, 사무직
    - 블루칼라: 서비스, 판매, 농림어업, 기능원, 장치조작, 단순노무, 군인, 기타
    - 비경제활동: 미취업자
    
    변수: soa_06z2
    1: 농림어업, 2: 전문가, 3: 관리자, 4: 단순노무, 5: 사무
    6: 기계조작, 7: 판매, 8: 서비스, 9: 기능원, 10: 군인, 88: 비경제활동
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
# 내용: 임금근로자 여부 - EDA 07번 기반
# 함수명: feature_is_employee
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
def feature_is_employee(df_merge):
    """
    임금근로자 여부 (0/1) - EDA 07번 기반
    - 0: 자영업/고용주/무급가족 (금연 성공률 55.6%)
    - 1: 임금근로자 (금연 성공률 48.22%)
    
    변수: soa_07z1 (1~3)
    1: 고용주/자영업
    2: 임금근로자
    3: 무급가족종사자
    """
    df_merge['is_employee'] = np.where(
        df_merge['soa_07z1'] == 2, 1, 0
    )
    
    return df_merge


# ==================================================
# 내용: 혼인 안정성
# 함수명: feature_marital_stability
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
def feature_marital_stability(df_merge):
    """
    혼인 상태를 안정성 기준으로 분류
    - 안정: 유배우
    - 미혼: 미혼
    - 불안정: 사별, 이혼, 별거, 기타(무응답)
    
    변수: sod_02z3
    1: 유배우, 2: 미혼, 3: 사별, 4: 이혼, 5: 별거, 7/9: 무응답
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
# 통합 실행 함수 (선택사항)
# ==================================================
def create_all_features(df_merge):
    """
    모든 Feature를 한 번에 생성
    
    Parameters:
    -----------
    df_merge : DataFrame
        전처리된 데이터프레임
    
    Returns:
    --------
    df_merge : DataFrame
        Feature가 추가된 데이터프레임
    """
    df_merge = feature_education_group(df_merge)
    df_merge = feature_is_economically_active(df_merge)
    df_merge = feature_job_risk_group(df_merge)
    df_merge = feature_occupation_type(df_merge)
    df_merge = feature_is_employee(df_merge)
    df_merge = feature_marital_stability(df_merge)
    
    print("✅ 6개 Feature 생성 완료!")
    print(f"   - education_group: {df_merge['education_group'].notna().sum():,}개")
    print(f"   - is_economically_active: {df_merge['is_economically_active'].notna().sum():,}개")
    print(f"   - job_risk_group: {df_merge['job_risk_group'].notna().sum():,}개")
    print(f"   - occupation_type: {df_merge['occupation_type'].notna().sum():,}개")
    print(f"   - is_employee: {df_merge['is_employee'].notna().sum():,}개")
    print(f"   - marital_stability: {df_merge['marital_stability'].notna().sum():,}개")
    
    return df_merge


# ==================================================
# 사용 예시
# ==================================================
if __name__ == "__main__":
    # 예시: 팀 통합 코드에서 사용
    # from features_01_vfxpedia import feature_education_group, feature_is_economically_active, ...
    # 
    # df_merge = feature_education_group(df_merge)
    # df_merge = feature_is_economically_active(df_merge)
    # ...
    
    # 또는 한 번에 실행
    # df_merge = create_all_features(df_merge)
    
    print("features_01_vfxpedia.py 로드 완료!")