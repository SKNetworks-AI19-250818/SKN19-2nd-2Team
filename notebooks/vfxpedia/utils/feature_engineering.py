"""
Feature Engineering for Smoking Cessation Prediction

EDA 06, 07, 08번 노트북의 인사이트를 바탕으로 모델링용 변수 생성

작성일: 2025-10-10
작성자: 오흥재 (vfxpedia)
"""

import pandas as pd
import numpy as np


# 1. 교육수준 그룹화 (06번 노트북 인사이트)
def group_education(sob_01z1):
    """
    역U자 패턴 기반 3그룹 분류
    
    Args:
        sob_01z1 (float): 교육수준 원본 값 (1~8)
    
    Returns:
        int: 그룹 코드 (0: 저학력_저위험, 1: 중학력_고위험, 2: 고학력_중위험)
        
    참고:
        - 저학력_저위험 (0): 무학(1), 서당/한학(2), 초등(3) → 흡연율 27.5%
        - 중학력_고위험 (1): 중학(4), 고등(5), 전문대(6) → 흡연율 44.4%
        - 고학력_중위험 (2): 4년제(7), 대학원(8) → 흡연율 33.3%
    """
    if pd.isna(sob_01z1):
        return np.nan
    
    if sob_01z1 <= 3:  # 무학 ~ 초등
        return 0  # 저학력_저위험
    elif sob_01z1 <= 6:  # 중학 ~ 전문대
        return 1  # 중학력_고위험
    else:  # 4년제 ~ 대학원
        return 2  # 고학력_중위험


# 2. 경제활동 여부 (07번 노트북 인사이트)
def is_economically_active(soa_01z1):
    """
    경제활동 여부 Binary 변수
    
    Args:
        soa_01z1 (float): 경제활동 여부 (1: 경제활동, 2: 비경제활동)
    
    Returns:
        int: 1=경제활동자, 0=비경제활동자
        
    참고:
        - 비경제활동자: 64.76% 금연 성공률
        - 경제활동자: 51.01% 금연 성공률
        - 차이: 13.75%p (매우 큰 효과)
    """
    if pd.isna(soa_01z1):
        return np.nan
    return 1 if soa_01z1 == 1 else 0


# 3. 직업 위험도 그룹화 (07번 노트북 인사이트)
def group_job_risk(soa_06z2):
    """
    직업별 금연 성공률 기반 3그룹 분류
    
    Args:
        soa_06z2 (float): 직업분류 (1~10)
    
    Returns:
        int: 위험도 그룹 (0: 저위험, 1: 중위험, 2: 고위험, -1: 해당없음)
        
    참고:
        - 저위험_고성공 (0): 농림어업(1), 전문가(2), 관리자(3) → 53~62%
        - 중위험 (1): 단순노무(4), 사무(5), 기계조작(6), 판매(7) → 47~52%
        - 고위험_저성공 (2): 서비스(8), 기능원(9), 군인(10) → 40~45%
    """
    if pd.isna(soa_06z2):
        return -1  # 비경제활동자 등
    
    if soa_06z2 in [1, 2, 3]:  # 농림어업, 전문가, 관리자
        return 0  # 저위험_고성공
    elif soa_06z2 in [4, 5, 6, 7]:  # 단순노무, 사무, 기계조작, 판매
        return 1  # 중위험
    else:  # 서비스, 기능원, 군인
        return 2  # 고위험_저성공


# 4. 종사상지위 (07번 노트북 인사이트)
def is_employee(soa_07z1):
    """
    임금근로자 여부 Binary 변수
    
    Args:
        soa_07z1 (float): 종사상지위 (1: 고용주/자영업, 2: 임금근로자, 3: 무급가족종사자)
    
    Returns:
        int: 1=임금근로자, 0=기타
        
    참고:
        - 임금근로자: 48.22% 금연 성공률 (낮음)
        - 고용주/자영업: 55.68% 금연 성공률 (높음)
        - 무급가족종사자: 55.58% 금연 성공률 (높음)
    """
    if pd.isna(soa_07z1):
        return np.nan
    return 1 if soa_07z1 == 2 else 0


# 5. Feature Engineering 일괄 적용
def apply_feature_engineering(df):
    """
    데이터프레임에 모든 Feature Engineering 적용
    
    Args:
        df (pd.DataFrame): 입력 데이터프레임 (analy_data_cleaned.csv)
    
    Returns:
        pd.DataFrame: Feature Engineering 적용된 데이터프레임
    """
    df_fe = df.copy()
    
    # 1. 교육수준 그룹화
    if 'sob_01z1' in df_fe.columns:
        df_fe['education_group'] = df_fe['sob_01z1'].apply(group_education)
    
    # 2. 경제활동 여부
    if 'soa_01z1' in df_fe.columns:
        df_fe['is_economically_active'] = df_fe['soa_01z1'].apply(is_economically_active)
    
    # 3. 직업 위험도
    if 'soa_06z2' in df_fe.columns:
        df_fe['job_risk_group'] = df_fe['soa_06z2'].apply(group_job_risk)
    
    # 4. 임금근로자 여부
    if 'soa_07z1' in df_fe.columns:
        df_fe['is_employee'] = df_fe['soa_07z1'].apply(is_employee)
    
    return df_fe


# 6. 변수 설명 딕셔너리
FEATURE_DESCRIPTIONS = {
    'education_group': {
        'name': '교육수준_그룹',
        'values': {
            0: '저학력_저위험 (무학~초등)',
            1: '중학력_고위험 (중학~전문대)',
            2: '고학력_중위험 (4년제~대학원)'
        },
        'insight': '역U자 패턴: 중학력에서 흡연율 최고 (44.4%)'
    },
    'is_economically_active': {
        'name': '경제활동_여부',
        'values': {
            0: '비경제활동자 (금연 성공률 64.76%)',
            1: '경제활동자 (금연 성공률 51.01%)'
        },
        'insight': '비경제활동자가 13.75%p 높은 금연 성공률'
    },
    'job_risk_group': {
        'name': '직업_위험도',
        'values': {
            -1: '해당없음 (비경제활동자)',
            0: '저위험_고성공 (농림어업, 전문가, 관리자)',
            1: '중위험 (단순노무, 사무, 기계조작, 판매)',
            2: '고위험_저성공 (서비스, 기능원, 군인)'
        },
        'insight': '직업별 금연 성공률 최대 22.71%p 차이'
    },
    'is_employee': {
        'name': '임금근로자_여부',
        'values': {
            0: '자영업/고용주/무급가족 (금연 성공률 55.6%)',
            1: '임금근로자 (금연 성공률 48.22%)'
        },
        'insight': '임금근로자가 7.46%p 낮은 금연 성공률'
    }
}


def print_feature_info():
    """생성된 Feature들의 설명 출력"""
    print("=" * 80)
    print("📊 Feature Engineering 변수 설명")
    print("=" * 80)
    
    for feature, info in FEATURE_DESCRIPTIONS.items():
        print(f"\n🔹 {feature} ({info['name']})")
        print(f"   💡 인사이트: {info['insight']}")
        print(f"   📌 값:")
        for code, description in info['values'].items():
            print(f"      {code}: {description}")
    
    print("\n" + "=" * 80)