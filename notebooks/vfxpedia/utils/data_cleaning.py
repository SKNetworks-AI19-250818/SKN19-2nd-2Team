"""
데이터 정제 모듈 - 오흥재 (vfxpedia)
교육 및 경제활동에 따른 금연 성공 상관관계 분석용

작성: 2025-10-07
"""

import pandas as pd
import numpy as np


# ============================================================================
# 📋 변수 설명 및 코드 매핑
# ============================================================================

# 경제활동 관련 특수 코드 설명
ECONOMIC_CODES = {
    'soa_06z2': {
        'variable_name': '직업분류',
        'description': '현재 직업 (표준직업분류 대분류)',
        'special_codes': {
            77: '응답거부',
            88: '비경제활동인구',  # ⭐ 중요: 분석적으로 의미 있는 그룹
            99: '모름'
        },
        'note': '88(비경제활동인구)은 정상값으로 유지합니다. 약 35.6%를 차지하는 의미있는 그룹입니다.'
    },
    'soa_07z1': {
        'variable_name': '종사상 지위',
        'description': '근로 형태 및 고용 상태',
        'special_codes': {
            7: '응답거부',
            8: '비경제활동인구',  # ⭐ 중요: 분석적으로 의미 있는 그룹
            9: '모름'
        },
        'note': '8(비경제활동인구)은 정상값으로 유지합니다.'
    }
}


# 경제활동 상태 레이블 매핑
ECONOMIC_STATUS_LABELS = {
    'economically_inactive': '비경제활동인구',
    'economically_active': '경제활동인구'
}


def print_economic_code_info(var_name='soa_06z2'):
    """
    경제활동 관련 변수의 코드 정보 출력
    
    팀원들이 변수 의미를 빠르게 이해할 수 있도록 도와줍니다.
    
    Parameters:
    -----------
    var_name : str
        변수명 ('soa_06z2' 또는 'soa_07z1')
    
    Example:
    --------
    >>> print_economic_code_info('soa_06z2')
    """
    if var_name not in ECONOMIC_CODES:
        print(f"❌ {var_name}은(는) 경제활동 관련 변수가 아닙니다.")
        return
    
    info = ECONOMIC_CODES[var_name]
    
    print("=" * 80)
    print(f"📊 {var_name} - {info['variable_name']}")
    print("=" * 80)
    print(f"\n설명: {info['description']}")
    print(f"\n특수 코드:")
    for code, label in info['special_codes'].items():
        marker = "⭐" if code in [88, 8] else "  "
        print(f"  {marker} {code}: {label}")
    print(f"\n💡 Note: {info['note']}")
    print("=" * 80)


# ============================================================================
# 🔧 Feature Engineering 함수들
# ============================================================================

def add_economic_status_features(df, verbose=True):
    """
    경제활동 상태 관련 Feature 생성
    
    soa_06z2 변수의 88(비경제활동인구) 값을 명확한 변수로 변환합니다.
    팀원들이 코드를 보고 바로 이해할 수 있도록 합니다.
    
    생성되는 Feature:
    -----------------
    1. is_economically_inactive (int): 비경제활동인구 여부 (0/1)
    2. is_economically_active (int): 경제활동인구 여부 (0/1)
    3. economic_status (str): 경제활동 상태 레이블
    
    Parameters:
    -----------
    df : DataFrame
        입력 데이터프레임 (soa_06z2 컬럼 필요)
    verbose : bool
        진행 상황 출력 여부
    
    Returns:
    --------
    df : DataFrame
        Feature가 추가된 데이터프레임
    
    Example:
    --------
    >>> df = pd.read_csv('analy_data.csv')
    >>> df = add_economic_status_features(df)
    >>> 
    >>> # 이제 명확하게 사용 가능:
    >>> non_econ_rate = df['is_economically_inactive'].mean()
    >>> print(f"비경제활동인구 비율: {non_econ_rate*100:.1f}%")
    """
    
    if 'soa_06z2' not in df.columns:
        raise ValueError("❌ 'soa_06z2' 컬럼이 데이터프레임에 없습니다.")
    
    df = df.copy()
    
    # Feature 1: 비경제활동인구 여부 (이진 변수)
    df['is_economically_inactive'] = (df['soa_06z2'] == 88).astype(int)
    
    # Feature 2: 경제활동인구 여부 (이진 변수)
    df['is_economically_active'] = (df['soa_06z2'] != 88).astype(int)
    
    # Feature 3: 경제활동 상태 레이블 (문자열)
    df['economic_status'] = df['soa_06z2'].apply(
        lambda x: ECONOMIC_STATUS_LABELS['economically_inactive'] if x == 88 
        else ECONOMIC_STATUS_LABELS['economically_active']
    )
    
    if verbose:
        print("=" * 80)
        print("✅ 경제활동 상태 Feature 생성 완료")
        print("=" * 80)
        
        print("\n생성된 Feature:")
        print("  1. is_economically_inactive (int): 비경제활동인구 여부")
        print("  2. is_economically_active (int): 경제활동인구 여부")
        print("  3. economic_status (str): 경제활동 상태 레이블")
        
        print("\n📊 분포:")
        inactive_count = df['is_economically_inactive'].sum()
        inactive_rate = inactive_count / len(df) * 100
        active_count = df['is_economically_active'].sum()
        active_rate = active_count / len(df) * 100
        
        print(f"  비경제활동인구: {inactive_count:,}명 ({inactive_rate:.1f}%)")
        print(f"  경제활동인구:   {active_count:,}명 ({active_rate:.1f}%)")
        
        print("\n💡 사용 예시:")
        print("  # 비경제활동인구만 필터링")
        print("  df_inactive = df[df['is_economically_inactive'] == 1]")
        print()
        print("  # 그룹별 금연 성공률 비교")
        print("  df.groupby('economic_status')['churn'].mean()")
        print("=" * 80)
    
    return df


def get_economic_status_summary(df, group_var='economic_status', target_var='churn'):
    """
    경제활동 상태별 요약 통계
    
    Parameters:
    -----------
    df : DataFrame
        분석 데이터 (economic_status 또는 is_economically_inactive 필요)
    group_var : str
        그룹 변수 ('economic_status' 또는 'is_economically_inactive')
    target_var : str
        타겟 변수 (기본값: 'churn')
    
    Returns:
    --------
    summary : DataFrame
        그룹별 요약 통계
    
    Example:
    --------
    >>> summary = get_economic_status_summary(df)
    >>> print(summary)
    """
    
    if group_var not in df.columns:
        raise ValueError(f"❌ '{group_var}' 컬럼이 데이터프레임에 없습니다.")
    
    if target_var not in df.columns:
        raise ValueError(f"❌ '{target_var}' 컬럼이 데이터프레임에 없습니다.")
    
    summary = df.groupby(group_var).agg({
        target_var: ['count', 'mean', 'std']
    }).round(4)
    
    summary.columns = ['샘플수', '금연성공률', '표준편차']
    summary['금연성공률(%)'] = (summary['금연성공률'] * 100).round(2)
    
    return summary


def clean_data_for_analysis(input_path, output_path=None, verbose=True):
    """
    데이터 정제 함수
    
    처리 내용:
    1. churn 결측값 제거
    2. 응답거부/모름 제거 (모든 변수)
    3. sob_02z1 제외 (Skip Logic 때문)
    4. soa_06z2, soa_07z1의 비해당(88, 8)은 유지 (비경제활동인구)
    5. 나머지 결측값 제거
    
    Parameters:
    -----------
    input_path : str
        입력 파일 경로 (예: '../../data/analy_data.csv')
    output_path : str, optional
        출력 파일 경로 (예: './output/analy_data_cleaned.csv')
        None이면 저장하지 않음
    verbose : bool
        진행 상황 출력 여부
        
    Returns:
    --------
    df_clean : DataFrame
        정제된 데이터프레임
    report : dict
        정제 결과 보고서
    """
    
    # 데이터 로드
    df = pd.read_csv(input_path)
    df_original = df.copy()
    df_clean = df.copy()
    
    report = {
        'original_count': len(df_original),
        'steps': []
    }
    
    if verbose:
        print("=" * 80)
        print("🔧 데이터 정제 시작")
        print("=" * 80)
        print(f"\n원본 데이터: {len(df_original):,}건")
    
    # ========================================================================
    # Step 1: churn 결측값 제거
    # ========================================================================
    before = len(df_clean)
    df_clean = df_clean[df_clean['churn'].notna()]
    removed = before - len(df_clean)
    
    report['steps'].append({
        'step': 'Step 1: churn 결측값 제거',
        'removed': removed,
        'remaining': len(df_clean)
    })
    
    if verbose:
        print(f"\nStep 1: churn 결측값 제거")
        print(f"  제거: {removed:,}건")
        print(f"  현재: {len(df_clean):,}건")
    
    # ========================================================================
    # Step 2: 응답거부/모름 제거
    # ========================================================================
    refuse_unknown_codes = {
        'sob_01z1': [77, 99],
        'soa_01z1': [7, 9],
        'soa_06z2': [77, 99],
        'soa_07z1': [7, 9],
        'sod_02z3': [7, 9]
    }
    
    before = len(df_clean)
    removed_by_var = {}
    
    for var, codes in refuse_unknown_codes.items():
        var_removed = 0
        for code in codes:
            count = (df_clean[var] == code).sum()
            df_clean = df_clean[df_clean[var] != code]
            var_removed += count
        
        if var_removed > 0:
            removed_by_var[var] = var_removed
    
    total_removed = before - len(df_clean)
    
    report['steps'].append({
        'step': 'Step 2: 응답거부/모름 제거',
        'removed': total_removed,
        'remaining': len(df_clean),
        'details': removed_by_var
    })
    
    if verbose:
        print(f"\nStep 2: 응답거부/모름 제거")
        if removed_by_var:
            for var, count in removed_by_var.items():
                print(f"  {var}: {count:,}건")
        print(f"  총 제거: {total_removed:,}건")
        print(f"  현재: {len(df_clean):,}건")
    
    # ========================================================================
    # Step 3: sob_02z1 처리 - Skip Logic 때문에 분석에서 제외
    # ========================================================================
    if verbose:
        print(f"\nStep 3: sob_02z1 처리")
        print(f"  처리 방법: 분석 변수에서 제외 (Skip Logic)")
        print(f"  이유: sob_01z1이 1(무학) 또는 2(서당/한학)인 경우 비해당(8)이 정상값")
        sob_02z1_na = (df_clean['sob_01z1'].isin([1, 2])).sum()
        print(f"  해당 케이스: {sob_02z1_na:,}건")
    
    # ========================================================================
    # Step 4: soa_06z2, soa_07z1 비해당 유지 (비경제활동인구)
    # ========================================================================
    non_econ_count = (df_clean['soa_06z2'] == 88).sum()
    
    if verbose:
        print(f"\nStep 4: 직업/종사상지위 비해당 처리")
        print(f"  처리 방법: '비경제활동인구'로 유지 (제거하지 않음)")
        print(f"  비경제활동인구: {non_econ_count:,}건 ({non_econ_count/len(df_clean)*100:.1f}%)")
        print(f"  이유: 분석적으로 의미 있는 그룹")
    
    report['non_economic_count'] = non_econ_count
    
    # ========================================================================
    # Step 5: 나머지 결측값 제거
    # ========================================================================
    analysis_vars = ['sob_01z1', 'soa_01z1', 'soa_06z2', 'soa_07z1', 'sod_02z3']
    
    before = len(df_clean)
    df_clean = df_clean.dropna(subset=analysis_vars)
    removed = before - len(df_clean)
    
    report['steps'].append({
        'step': 'Step 5: 결측값 제거',
        'removed': removed,
        'remaining': len(df_clean)
    })
    
    if verbose:
        print(f"\nStep 5: 결측값 제거")
        print(f"  대상 변수: {', '.join(analysis_vars)}")
        print(f"  제거: {removed:,}건")
        print(f"  현재: {len(df_clean):,}건")
    
    # ========================================================================
    # 정제 완료
    # ========================================================================
    report['final_count'] = len(df_clean)
    report['total_removed'] = len(df_original) - len(df_clean)
    report['removal_rate'] = report['total_removed'] / len(df_original) * 100
    report['original_success_rate'] = df_original['churn'].mean() * 100
    report['cleaned_success_rate'] = df_clean['churn'].mean() * 100
    report['analysis_vars'] = analysis_vars
    
    if verbose:
        print("\n" + "=" * 80)
        print("✅ 데이터 정제 완료")
        print("=" * 80)
        print(f"\n원본 데이터:     {len(df_original):,}건")
        print(f"정제 데이터:     {len(df_clean):,}건")
        print(f"제거된 데이터:   {report['total_removed']:,}건 ({report['removal_rate']:.1f}%)")
        print(f"\n금연 성공률 (원본): {report['original_success_rate']:.2f}%")
        print(f"금연 성공률 (정제): {report['cleaned_success_rate']:.2f}%")
        
        print(f"\n✅ 최종 분석 변수 ({len(analysis_vars)}개):")
        var_names = {
            'sob_01z1': '교육수준(최종학력)',
            'soa_01z1': '경제활동 여부',
            'soa_06z2': '직업분류',
            'soa_07z1': '종사상 지위',
            'sod_02z3': '혼인상태'
        }
        for var in analysis_vars:
            print(f"  - {var}: {var_names[var]}")
        
        print(f"\n⚠️ 제외된 변수:")
        print(f"  - sob_02z1: 졸업상태 (Skip Logic)")
        
        print("\n" + "=" * 80)
    
    # 저장
    if output_path:
        df_clean.to_csv(output_path, index=False, encoding='utf-8-sig')
        if verbose:
            print(f"💾 저장 완료: {output_path}")
            print("=" * 80)
    
    return df_clean, report


def get_analysis_summary(report):
    """
    정제 결과 요약 출력
    
    Parameters:
    -----------
    report : dict
        clean_data_for_analysis() 함수의 반환값
    """
    print("\n" + "=" * 80)
    print("📊 데이터 정제 요약")
    print("=" * 80)
    
    print(f"\n원본 → 정제:")
    print(f"  {report['original_count']:,}건 → {report['final_count']:,}건")
    print(f"  제거율: {report['removal_rate']:.1f}%")
    
    print(f"\n금연 성공률:")
    print(f"  원본: {report['original_success_rate']:.2f}%")
    print(f"  정제: {report['cleaned_success_rate']:.2f}%")
    
    print(f"\n비경제활동인구:")
    print(f"  {report['non_economic_count']:,}건")
    print(f"  ({report['non_economic_count']/report['final_count']*100:.1f}%)")
    
    print(f"\n분석 변수:")
    for var in report['analysis_vars']:
        print(f"  ✓ {var}")
    
    print("\n" + "=" * 80)
