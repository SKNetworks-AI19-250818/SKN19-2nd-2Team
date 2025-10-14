# ==================================================
# 내용: 피처생성코드
# 함수명: feature_[변수명]
# input: df_merge(dataframe)
# output: df_merge(dataframe)
# ==================================================
import pandas as pd
import numpy as np

# ==================================================
# 교육 및 경제활동 추가 함수들
# ==================================================

# 교육수준 그룹 (저/중/고 학력)
def feature_education_group(df_merge):
    """
    교육수준을 3그룹으로 분류
    - 0: 저학력 (무학/초졸/중졸)
    - 1: 중학력 (고졸)
    - 2: 고학력 (대졸 이상)
    
    변수: sob_01z1
    0: 무학, 1: 초졸, 2: 중졸, 3: 고졸, 4: 대졸, 5: 대학원졸, 6: 박사
    """
    conditions = [
        df_merge['sob_01z1'] <= 2,  # 무학(0), 초졸(1), 중졸(2)
        df_merge['sob_01z1'] == 3,   # 고졸(3)
        df_merge['sob_01z1'] >= 4    # 대졸 이상(4,5,6)
    ]
    choices = [0, 1, 2]
    df_merge['education_group'] = np.select(conditions, choices, default=np.nan)
    
    return df_merge

# 경제활동 여부
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


# 직업 유형 (화이트칼라/블루칼라/비경제활동)
def feature_occupation_type(df_merge):
    """
    직업을 3가지 유형으로 분류
    - 화이트칼라: 관리자, 전문가, 사무직
    - 블루칼라: 서비스, 판매, 농림어업, 기능원, 장치조작, 단순노무, 군인, 기타
    - 비경제활동: 미취업자
    
    변수: soa_06z2
    1~3: 화이트칼라, 4~10: 블루칼라(군인 포함), 88: 비경제활동, 기타: 블루칼라
    """
    conditions = [
        df_merge['soa_06z2'].isin([1, 2, 3]),    # 화이트칼라
        df_merge['soa_06z2'] == 88                # 비경제활동
    ]
    choices = ['화이트칼라', '비경제활동']
    # 나머지는 모두 블루칼라 (군인, 무응답 포함)
    df_merge['occupation_type'] = np.select(conditions, choices, default='블루칼라')
    
    return df_merge


# 임금근로자 여부
def feature_is_employee(df_merge):
    """
    임금근로자 여부 (0/1)
    - 1: 임금근로자 (상용직, 임시직, 일용직)
    - 0: 자영업자, 고용주, 무급가족종사자
    
    변수: soa_07z1
    1: 상용직, 2: 임시직, 3: 일용직
    4: 고용원 있는 자영업자, 5: 고용원 없는 자영업자, 6: 무급가족종사자
    """
    df_merge['is_employee'] = np.where(
        df_merge['soa_07z1'].isin([1, 2, 3]), 1, 0
    )
    
    return df_merge


# 혼인 안정성
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
    choices = ['안정', '미혼']
    # 나머지는 모두 '불안정'으로 (사별, 이혼, 별거, 무응답 포함)
    df_merge['marital_stability'] = np.select(conditions, choices, default='불안정')
    
    return df_merge