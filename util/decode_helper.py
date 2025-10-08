"""
변수 디코딩 유틸리티 함수
Community Health Survey 2024

EDA, 시각화, 보고서 작성시 활용할 수 있는 헬퍼 함수들

Usage:
    from util.decode_helper import decode_column, decode_dataframe, get_label
    
    # 단일 값 디코딩
    label = decode_column('nua_01z2', 1)  # '주 5~7회'
    
    # DataFrame의 특정 컬럼 전체 디코딩
    df['아침식사_라벨'] = decode_dataframe(df, 'nua_01z2')
    
    # 시각화용 라벨 생성
    plot_label = get_label('nua_01z2')  # '아침식사 빈도'
"""

import pandas as pd
import numpy as np
from data.var_mapping import VAR_DICT, get_var_name, get_var_value, get_var_info


def decode_column(var_code, value):
    """
    단일 변수 코드와 값을 디코딩
    
    Parameters:
    -----------
    var_code : str
        변수 코드명 (예: 'nua_01z2')
    value : int or float
        코드 값
        
    Returns:
    --------
    str
        디코딩된 의미 문자열
        
    Examples:
    ---------
    >>> decode_column('nua_01z2', 1)
    '주 5~7회'
    
    >>> decode_column('age', 35)
    '35'
    """
    return get_var_value(var_code, value)


def decode_dataframe(df, var_code, new_col_name=None):
    """
    DataFrame의 특정 컬럼 전체를 디코딩
    
    Parameters:
    -----------
    df : pd.DataFrame
        대상 데이터프레임
    var_code : str
        디코딩할 컬럼명 (변수 코드)
    new_col_name : str, optional
        새로 생성할 컬럼명. None이면 '{var_code}_label' 사용
        
    Returns:
    --------
    pd.Series
        디코딩된 값들의 시리즈
        
    Examples:
    ---------
    >>> df['아침식사_라벨'] = decode_dataframe(df, 'nua_01z2')
    >>> df[['nua_01z2', '아침식사_라벨']].head()
    """
    if var_code not in df.columns:
        raise ValueError(f"컬럼 '{var_code}'가 데이터프레임에 없습니다.")
    
    return df[var_code].apply(lambda x: decode_column(var_code, x) if pd.notna(x) else np.nan)


def get_label(var_code, include_unit=False):
    """
    변수의 한글 라벨 조회 (시각화 제목/축 라벨용)
    
    Parameters:
    -----------
    var_code : str
        변수 코드명
    include_unit : bool, default False
        단위 포함 여부
        
    Returns:
    --------
    str
        한글 라벨
        
    Examples:
    ---------
    >>> get_label('nua_01z2')
    '아침식사 빈도'
    
    >>> get_label('oba_02z1', include_unit=True)
    '신장 (cm)'
    """
    var_info = get_var_info(var_code)
    if not var_info:
        return var_code
    
    label = var_info['name']
    
    if include_unit and 'unit' in var_info:
        label = f"{label} ({var_info['unit']})"
    
    return label


def get_value_labels(var_code):
    """
    범주형 변수의 모든 값-라벨 매핑 조회
    
    Parameters:
    -----------
    var_code : str
        변수 코드명
        
    Returns:
    --------
    dict or None
        값-라벨 딕셔너리. 연속형 변수는 None 반환
        
    Examples:
    ---------
    >>> get_value_labels('sex')
    {1: '남자', 2: '여자'}
    """
    var_info = get_var_info(var_code)
    if not var_info or var_info['type'] != 'categorical':
        return None
    
    return var_info.get('values')


def decode_multiple_columns(df, var_codes, suffix='_label'):
    """
    여러 컬럼을 한번에 디코딩
    
    Parameters:
    -----------
    df : pd.DataFrame
        대상 데이터프레임
    var_codes : list of str
        디코딩할 컬럼명 리스트
    suffix : str, default '_label'
        새 컬럼명 접미사
        
    Returns:
    --------
    pd.DataFrame
        디코딩된 컬럼들이 추가된 데이터프레임 복사본
        
    Examples:
    ---------
    >>> df_decoded = decode_multiple_columns(df, ['sex', 'nua_01z2'])
    >>> df_decoded.columns
    ['sex', 'sex_label', 'nua_01z2', 'nua_01z2_label', ...]
    """
    df_copy = df.copy()
    
    for var_code in var_codes:
        if var_code in df_copy.columns:
            new_col = f"{var_code}{suffix}"
            df_copy[new_col] = decode_dataframe(df_copy, var_code)
        else:
            print(f"Warning: 컬럼 '{var_code}'를 찾을 수 없습니다.")
    
    return df_copy


def create_value_mapping_dict(var_code):
    """
    Pandas의 map() 함수에 사용할 딕셔너리 생성
    
    Parameters:
    -----------
    var_code : str
        변수 코드명
        
    Returns:
    --------
    dict
        값-라벨 매핑 딕셔너리
        
    Examples:
    ---------
    >>> mapping = create_value_mapping_dict('sex')
    >>> df['sex_label'] = df['sex'].map(mapping)
    """
    return get_value_labels(var_code) or {}


def print_var_info(var_code, show_values=True):
    """
    변수 정보를 보기 좋게 출력
    
    Parameters:
    -----------
    var_code : str
        변수 코드명
    show_values : bool, default True
        코드값 목록 출력 여부
        
    Examples:
    ---------
    >>> print_var_info('nua_01z2')
    ==========================================
    변수코드: nua_01z2
    변수명: 아침식사 빈도
    카테고리: 건강행태-식생활
    타입: categorical
    ------------------------------------------
    코드값:
      1: 주 5~7회
      2: 주 3~4회
      3: 주 1~2회
      4: 거의 안함(주 0회)
    ==========================================
    """
    var_info = get_var_info(var_code)
    if not var_info:
        print(f"❌ 변수 '{var_code}'를 찾을 수 없습니다.")
        return
    
    print("=" * 50)
    print(f"변수코드: {var_code}")
    print(f"변수명: {var_info['name']}")
    print(f"카테고리: {var_info.get('category', 'N/A')}")
    print(f"타입: {var_info['type']}")
    
    if 'unit' in var_info:
        print(f"단위: {var_info['unit']}")
    
    if 'description' in var_info:
        print(f"설명: {var_info['description']}")
    
    if 'note' in var_info:
        print(f"⚠️ 주의: {var_info['note']}")
    
    if show_values and var_info['type'] == 'categorical' and var_info.get('values'):
        print("-" * 50)
        print("코드값:")
        for code, label in sorted(var_info['values'].items()):
            print(f"  {code}: {label}")
    
    if 'special_codes' in var_info:
        print("-" * 50)
        print("특수코드:")
        for code, label in sorted(var_info['special_codes'].items()):
            print(f"  {code}: {label}")
    
    print("=" * 50)


def create_crosstab_with_labels(df, var1, var2, **kwargs):
    """
    라벨이 포함된 교차표 생성
    
    Parameters:
    -----------
    df : pd.DataFrame
        대상 데이터프레임
    var1, var2 : str
        교차표를 만들 두 변수 코드
    **kwargs : 
        pd.crosstab에 전달할 추가 인자
        
    Returns:
    --------
    pd.DataFrame
        라벨이 적용된 교차표
        
    Examples:
    ---------
    >>> ct = create_crosstab_with_labels(df, 'sex', 'churn', normalize='index')
    """
    # 임시 라벨 컬럼 생성
    df_temp = df.copy()
    df_temp[f'{var1}_label'] = decode_dataframe(df_temp, var1)
    df_temp[f'{var2}_label'] = decode_dataframe(df_temp, var2)
    
    # 교차표 생성
    ct = pd.crosstab(
        df_temp[f'{var1}_label'], 
        df_temp[f'{var2}_label'],
        **kwargs
    )
    
    return ct


def filter_special_codes(df, var_code, drop=True):
    """
    특수 코드(응답거부, 모름 등) 필터링
    
    Parameters:
    -----------
    df : pd.DataFrame
        대상 데이터프레임
    var_code : str
        변수 코드명
    drop : bool, default True
        True면 특수코드 제거, False면 특수코드만 선택
        
    Returns:
    --------
    pd.DataFrame
        필터링된 데이터프레임
        
    Examples:
    ---------
    >>> # 응답거부, 모름 제거
    >>> df_clean = filter_special_codes(df, 'mta_01z1', drop=True)
    """
    var_info = get_var_info(var_code)
    if not var_info:
        return df
    
    special_codes = []
    
    # 특수 코드 수집
    if 'special_codes' in var_info:
        special_codes.extend(var_info['special_codes'].keys())
    
    if var_info['type'] == 'categorical' and var_info.get('values'):
        # 일반적인 특수 코드 패턴
        for code, label in var_info['values'].items():
            if any(keyword in label for keyword in ['응답거부', '모름', '비해당']):
                special_codes.append(code)
    
    if not special_codes:
        return df
    
    if drop:
        return df[~df[var_code].isin(special_codes)]
    else:
        return df[df[var_code].isin(special_codes)]


def get_summary_stats(df, var_code):
    """
    변수 타입에 맞는 요약 통계 출력
    
    Parameters:
    -----------
    df : pd.DataFrame
        대상 데이터프레임
    var_code : str
        변수 코드명
        
    Examples:
    ---------
    >>> get_summary_stats(df, 'age')
    >>> get_summary_stats(df, 'sex')
    """
    var_info = get_var_info(var_code)
    if not var_info:
        print(f"❌ 변수 '{var_code}'를 찾을 수 없습니다.")
        return
    
    print("=" * 50)
    print(f"📊 {var_info['name']} ({var_code}) 요약 통계")
    print("=" * 50)
    
    data = df[var_code]
    print(f"전체 데이터 수: {len(data)}")
    print(f"결측값: {data.isna().sum()} ({data.isna().mean()*100:.2f}%)")
    
    if var_info['type'] == 'continuous':
        print("\n[연속형 변수 통계]")
        print(data.describe())
        
    elif var_info['type'] == 'categorical':
        print("\n[범주형 변수 빈도]")
        freq = data.value_counts().sort_index()
        freq_pct = data.value_counts(normalize=True).sort_index() * 100
        
        print(f"\n{'코드':<10} {'라벨':<30} {'빈도':<10} {'비율(%)':<10}")
        print("-" * 60)
        for code in freq.index:
            label = decode_column(var_code, code)
            count = freq[code]
            pct = freq_pct[code]
            print(f"{code:<10} {label:<30} {count:<10} {pct:<10.2f}")
    
    print("=" * 50)


# ========================================
# 시각화 관련 유틸리티
# ========================================

def prepare_plot_data(df, var_code, sort_by='code', remove_special=True):
    """
    시각화를 위한 데이터 준비
    
    Parameters:
    -----------
    df : pd.DataFrame
        대상 데이터프레임
    var_code : str
        변수 코드명
    sort_by : str, default 'code'
        정렬 기준 ('code', 'freq', 'label')
    remove_special : bool, default True
        특수 코드 제거 여부
        
    Returns:
    --------
    pd.DataFrame
        시각화용 정리된 데이터 (code, label, count, percentage 컬럼)
    """
    # 특수 코드 제거
    if remove_special:
        df_clean = filter_special_codes(df, var_code, drop=True)
    else:
        df_clean = df
    
    # 빈도 계산
    freq = df_clean[var_code].value_counts()
    freq_pct = df_clean[var_code].value_counts(normalize=True) * 100
    
    # 데이터프레임 생성
    plot_df = pd.DataFrame({
        'code': freq.index,
        'label': [decode_column(var_code, code) for code in freq.index],
        'count': freq.values,
        'percentage': [freq_pct[code] for code in freq.index]
    })
    
    # 정렬
    if sort_by == 'code':
        plot_df = plot_df.sort_values('code')
    elif sort_by == 'freq':
        plot_df = plot_df.sort_values('count', ascending=False)
    elif sort_by == 'label':
        plot_df = plot_df.sort_values('label')
    
    return plot_df.reset_index(drop=True)


if __name__ == '__main__':
    # 사용 예시
    print("=" * 50)
    print("변수 디코딩 유틸리티 사용 예시")
    print("=" * 50)
    
    # 예시 데이터 생성
    sample_data = pd.DataFrame({
        'sex': [1, 2, 1, 2, 1],
        'nua_01z2': [1, 2, 3, 4, 1],
        'age': [25, 35, 45, 55, 65]
    })
    
    print("\n1. 단일 값 디코딩")
    print(f"sex=1 -> {decode_column('sex', 1)}")
    print(f"nua_01z2=2 -> {decode_column('nua_01z2', 2)}")
    
    print("\n2. 변수 정보 출력")
    print_var_info('nua_01z2')
    
    print("\n3. DataFrame 컬럼 디코딩")
    sample_data['sex_label'] = decode_dataframe(sample_data, 'sex')
    print(sample_data[['sex', 'sex_label']])
