"""
변수 디코딩 유틸리티
Community Health Survey 2024

variable.csv를 기반으로 변수 코드를 의미있는 텍스트로 변환

Author: vfxpedia
Last Updated: 2025-10-09
"""

import pandas as pd
import numpy as np
from pathlib import Path


class VariableDecoder:
    """
    건강조사 변수 코드를 의미있는 텍스트로 디코딩하는 클래스
    
    Attributes:
        df_variables (pd.DataFrame): variable.csv 데이터
        
    Examples:
        >>> decoder = VariableDecoder()
        >>> decoder.decode_value('sob_01z1', 5)
        '고등학교'
        
        >>> df = decoder.decode_column(df, 'sob_01z1')
        >>> df.head()
    """
    
    def __init__(self, csv_path=None, fallback_csv_path=None):
        """
        Args:
            csv_path (str, optional): variable.csv 경로. 
                                      기본값은 'data/variable.csv'
            fallback_csv_path (str, optional): variable_full.csv 경로.
                                               기본값은 'data/variable_full.csv'
        """
        if csv_path is None:
            # 프로젝트 루트 기준 경로
            project_root = Path(__file__).parent.parent
            csv_path = project_root / 'data' / 'variable.csv'
            
        if fallback_csv_path is None:
            project_root = Path(__file__).parent.parent
            fallback_csv_path = project_root / 'data' / 'variable_full.csv'
        
        self.csv_path = csv_path
        self.fallback_csv_path = fallback_csv_path
        self.df_variables = None
        self.df_fallback = None  # variable_full.csv용
        self._cache = {}  # 성능 향상을 위한 캐시
        self._fallback_cache = {}  # fallback용 캐시
        self._load_variables()
    
    def _load_variables(self):
        """variable.csv 및 variable_full.csv 파일 로드"""
        # 1. 메인 variable.csv 로드
        try:
            self.df_variables = pd.read_csv(self.csv_path, encoding='utf-8-sig')
            
            # 컬럼명 확인
            required_cols = ['variable', 'code', 'meaning']
            missing_cols = [col for col in required_cols if col not in self.df_variables.columns]
            
            if missing_cols:
                raise ValueError(f"❌ variable.csv에 필수 컬럼이 없습니다: {missing_cols}")
            
            print(f"✅ variable.csv 로드 완료: {len(self.df_variables)} 개 매핑")
            
            # 캐시 초기화
            self._build_cache()
            
        except FileNotFoundError:
            print(f"❌ variable.csv를 찾을 수 없습니다: {self.csv_path}")
            self.df_variables = pd.DataFrame()
        except Exception as e:
            print(f"❌ variable.csv 로드 실패: {e}")
            self.df_variables = pd.DataFrame()
        
        # 2. Fallback variable_full.csv 로드 (선택적)
        try:
            self.df_fallback = pd.read_csv(self.fallback_csv_path, encoding='utf-8-sig')
            print(f"✅ variable_full.csv 로드 완료: {len(self.df_fallback)} 개 매핑 (fallback)")
            
            # fallback 캐시 초기화
            self._build_fallback_cache()
            
        except FileNotFoundError:
            print(f"ℹ️  variable_full.csv 없음 (fallback 미사용): {self.fallback_csv_path}")
            self.df_fallback = pd.DataFrame()
        except Exception as e:
            print(f"⚠️  variable_full.csv 로드 실패 (fallback 미사용): {e}")
            self.df_fallback = pd.DataFrame()
    
    def _build_cache(self):
        """성능 향상을 위한 캐시 구축 (variable.csv)"""
        if self.df_variables.empty:
            return
        
        for _, row in self.df_variables.iterrows():
            var_name = row['variable']
            code = row['code']
            meaning = row['meaning']
            
            # 변수별 딕셔너리 생성
            if var_name not in self._cache:
                self._cache[var_name] = {
                    'label': row.get('label', var_name),
                    'category': row.get('category', 'Unknown'),
                    'mappings': {}
                }
            
            # 코드 변환 (숫자면 숫자로, 아니면 문자열로)
            try:
                if pd.notna(code):
                    code_key = float(code) if str(code).replace('.', '').isdigit() else str(code)
                    self._cache[var_name]['mappings'][code_key] = meaning
            except:
                pass
    
    def _build_fallback_cache(self):
        """fallback 캐시 구축 (variable_full.csv)"""
        if self.df_fallback.empty:
            return
        
        for _, row in self.df_fallback.iterrows():
            var_name = row['variable']
            code = row['code']
            meaning = row['meaning']
            
            # 변수별 딕셔너리 생성
            if var_name not in self._fallback_cache:
                self._fallback_cache[var_name] = {
                    'label': row.get('label', var_name),
                    'category': row.get('category', 'Unknown'),
                    'mappings': {}
                }
            
            # 코드 변환
            try:
                if pd.notna(code):
                    code_key = float(code) if str(code).replace('.', '').isdigit() else str(code)
                    self._fallback_cache[var_name]['mappings'][code_key] = meaning
            except:
                pass
    
    def decode_value(self, var_name, code, return_code_if_not_found=True):
        """
        단일 값을 의미로 디코딩 (variable.csv → variable_full.csv fallback)
        
        Args:
            var_name (str): 변수명 (예: 'sob_01z1')
            code (float/int/str): 코드 값
            return_code_if_not_found (bool): 매핑 없으면 원래 코드 반환 여부
            
        Returns:
            str: 디코딩된 의미
            
        Examples:
            >>> decoder.decode_value('sob_01z1', 5)
            '고등학교'
            
            >>> decoder.decode_value('sob_01z1', 7)
            '4년제대학'
        """
        if self.df_variables.empty and self.df_fallback.empty:
            return str(code) if return_code_if_not_found else None
        
        # NA 처리
        if pd.isna(code):
            return 'Missing' if return_code_if_not_found else None
        
        # 코드 타입 변환 시도
        search_keys = [code]
        if isinstance(code, (int, float)):
            search_keys.extend([float(code), int(code), str(int(code))])
        
        # 1. 메인 캐시에서 찾기
        if var_name in self._cache:
            mappings = self._cache[var_name]['mappings']
            for key in search_keys:
                if key in mappings:
                    return mappings[key]
        
        # 2. Fallback 캐시에서 찾기
        if var_name in self._fallback_cache:
            mappings = self._fallback_cache[var_name]['mappings']
            for key in search_keys:
                if key in mappings:
                    return mappings[key]
        
        return str(code) if return_code_if_not_found else None
    
    def decode_column(self, df, col_name, suffix='_label', inplace=False):
        """
        데이터프레임의 특정 컬럼을 디코딩
        
        Args:
            df (pd.DataFrame): 데이터프레임
            col_name (str): 디코딩할 컬럼명
            suffix (str): 새 컬럼 접미사 (기본값: '_label')
            inplace (bool): 원본 수정 여부
            
        Returns:
            pd.DataFrame: 디코딩된 컬럼이 추가된 데이터프레임
            
        Examples:
            >>> df = decoder.decode_column(df, 'sob_01z1')
            >>> # df에 'sob_01z1_label' 컬럼 추가됨
        """
        if not inplace:
            df = df.copy()
        
        if col_name not in df.columns:
            print(f"⚠️  컬럼 '{col_name}'이(가) 데이터프레임에 없습니다.")
            return df
        
        new_col_name = f"{col_name}{suffix}"
        df[new_col_name] = df[col_name].apply(
            lambda x: self.decode_value(col_name, x)
        )
        
        return df
    
    def decode_multiple_columns(self, df, col_names, suffix='_label', inplace=False):
        """
        여러 컬럼을 한번에 디코딩
        
        Args:
            df (pd.DataFrame): 데이터프레임
            col_names (list): 디코딩할 컬럼명 리스트
            suffix (str): 새 컬럼 접미사
            inplace (bool): 원본 수정 여부
            
        Returns:
            pd.DataFrame: 디코딩된 데이터프레임
            
        Examples:
            >>> df = decoder.decode_multiple_columns(df, ['sob_01z1', 'sma_03z2'])
        """
        if not inplace:
            df = df.copy()
        
        for col_name in col_names:
            df = self.decode_column(df, col_name, suffix=suffix, inplace=True)
        
        return df
    
    def get_variable_label(self, var_name):
        """
        변수의 한글 라벨 조회 (variable.csv → variable_full.csv fallback)
        
        Args:
            var_name (str): 변수명
            
        Returns:
            str: 변수 라벨
            
        Examples:
            >>> decoder.get_variable_label('sob_01z1')
            '교육수준'
        """
        # 1. 메인 캐시에서 찾기
        if var_name in self._cache:
            return self._cache[var_name]['label']
        
        # 2. Fallback 캐시에서 찾기
        if var_name in self._fallback_cache:
            return self._fallback_cache[var_name]['label']
        
        # 3. 둘 다 없으면 변수명 그대로 반환
        return var_name
    
    def get_variable_info(self, var_name):
        """
        변수에 대한 메타정보 조회 (variable.csv → variable_full.csv fallback)
        
        Args:
            var_name (str): 변수명
            
        Returns:
            dict: {'label': ..., 'category': ..., 'codes': [...]}
            
        Examples:
            >>> info = decoder.get_variable_info('sob_01z1')
            >>> print(info['label'])
            '교육수준'
        """
        # 1. 메인 캐시에서 찾기
        if var_name in self._cache:
            cache_info = self._cache[var_name]
            return {
                'variable': var_name,
                'label': cache_info['label'],
                'category': cache_info['category'],
                'codes': [
                    {'code': code, 'meaning': meaning}
                    for code, meaning in cache_info['mappings'].items()
                ]
            }
        
        # 2. Fallback 캐시에서 찾기
        if var_name in self._fallback_cache:
            cache_info = self._fallback_cache[var_name]
            return {
                'variable': var_name,
                'label': cache_info['label'],
                'category': cache_info['category'],
                'codes': [
                    {'code': code, 'meaning': meaning}
                    for code, meaning in cache_info['mappings'].items()
                ],
                'source': 'fallback'  # fallback에서 가져왔음을 표시
            }
        
        return {}
    
    def get_code_mapping(self, var_name):
        """
        변수의 code → meaning 딕셔너리 반환
        
        Args:
            var_name (str): 변수명
            
        Returns:
            dict: {code: meaning}
            
        Examples:
            >>> mapping = decoder.get_code_mapping('sob_01z1')
            >>> print(mapping)
            {5: '고등학교', 7: '4년제대학', ...}
        """
        if var_name in self._cache:
            return self._cache[var_name]['mappings'].copy()
        return {}
    
    def get_all_variables(self, category=None, include_fallback=True):
        """
        모든 변수 목록 또는 특정 카테고리의 변수 목록 반환
        
        Args:
            category (str, optional): 카테고리 필터
            include_fallback (bool): fallback 데이터도 포함할지 여부
            
        Returns:
            list: 변수명 리스트
        """
        variables = []
        
        # 1. 메인 데이터에서 가져오기
        if not self.df_variables.empty:
            if category:
                filtered = self.df_variables[
                    self.df_variables['category'] == category
                ]['variable'].unique().tolist()
                variables.extend(filtered)
            else:
                variables.extend(self.df_variables['variable'].unique().tolist())
        
        # 2. Fallback 데이터에서 추가로 가져오기
        if include_fallback and not self.df_fallback.empty:
            if category:
                filtered = self.df_fallback[
                    self.df_fallback['category'] == category
                ]['variable'].unique().tolist()
                variables.extend(filtered)
            else:
                variables.extend(self.df_fallback['variable'].unique().tolist())
        
        # 중복 제거 후 반환
        return list(set(variables))
    
    def get_categories(self, include_fallback=True):
        """
        모든 카테고리 목록 반환 (variable.csv + variable_full.csv)
        
        Args:
            include_fallback (bool): fallback 데이터도 포함할지 여부
            
        Returns:
            list: 카테고리 리스트
        """
        categories = []
        
        # 1. 메인 데이터에서 가져오기
        if not self.df_variables.empty and 'category' in self.df_variables.columns:
            categories.extend(self.df_variables['category'].dropna().unique().tolist())
        
        # 2. Fallback 데이터에서 추가로 가져오기
        if include_fallback and not self.df_fallback.empty and 'category' in self.df_fallback.columns:
            categories.extend(self.df_fallback['category'].dropna().unique().tolist())
        
        # 중복 제거 후 반환
        return list(set(categories))
    
    def create_value_counts_decoded(self, df, col_name, dropna=True, normalize=False):
        """
        value_counts()를 디코딩된 라벨로 반환
        
        Args:
            df (pd.DataFrame): 데이터프레임
            col_name (str): 컬럼명
            dropna (bool): NA 제외 여부
            normalize (bool): 비율로 변환 여부
            
        Returns:
            pd.Series: 디코딩된 라벨의 value counts
        """
        if col_name not in df.columns:
            print(f"❌ 컬럼 '{col_name}'이(가) 없습니다.")
            return pd.Series()
        
        # 원본 value_counts
        vc = df[col_name].value_counts(dropna=dropna, normalize=normalize)
        
        # 인덱스를 디코딩
        decoded_index = [self.decode_value(col_name, code) for code in vc.index]
        vc.index = decoded_index
        
        return vc
    
    def print_variable_summary(self, var_name):
        """
        변수 정보를 보기 좋게 출력
        
        Args:
            var_name (str): 변수명
        """
        info = self.get_variable_info(var_name)
        
        if not info:
            print(f"❌ 변수 '{var_name}'을(를) 찾을 수 없습니다.")
            return
        
        print(f"\n{'='*60}")
        print(f"📊 변수: {info['variable']}")
        print(f"🏷️  라벨: {info['label']}")
        print(f"📁 카테고리: {info['category']}")
        print(f"{'='*60}")
        print(f"\n코드 매핑 ({len(info['codes'])}개):")
        
        for code_info in sorted(info['codes'], key=lambda x: str(x['code'])):
            print(f"  {str(code_info['code']):>6} → {code_info['meaning']}")
        
        print(f"{'='*60}\n")


# ========================================
# 편의 함수 (클래스 없이 직접 사용)
# ========================================

# 전역 인스턴스 (싱글톤 패턴)
_global_decoder = None


def get_decoder():
    """전역 디코더 인스턴스 반환 (싱글톤 패턴)"""
    global _global_decoder
    if _global_decoder is None:
        _global_decoder = VariableDecoder()
    return _global_decoder


def decode_value(var_name, code):
    """
    단일 값 디코딩 (간편 함수)
    
    Examples:
        >>> from util.variable_decoder import decode_value
        >>> decode_value('sob_01z1', 5)
        '고등학교'
    """
    decoder = get_decoder()
    return decoder.decode_value(var_name, code)


def decode_column(df, col_name, suffix='_label'):
    """
    컬럼 디코딩 (간편 함수)
    
    Examples:
        >>> from util.variable_decoder import decode_column
        >>> df = decode_column(df, 'sob_01z1')
    """
    decoder = get_decoder()
    return decoder.decode_column(df, col_name, suffix=suffix)


def print_var_info(var_name):
    """
    변수 정보 출력 (간편 함수)
    
    Examples:
        >>> from util.variable_decoder import print_var_info
        >>> print_var_info('sob_01z1')
    """
    decoder = get_decoder()
    decoder.print_variable_summary(var_name)


def get_korean_label(var_name):
    """
    단일 변수의 한글 라벨을 반환
    
    Args:
        var_name (str): 변수명
        
    Returns:
        str: 한글 라벨
    
    Example:
        >>> label = get_korean_label('sob_01z1')
        >>> print(label)  # '교육수준'
    """
    decoder = get_decoder()
    return decoder.get_variable_label(var_name)


def get_korean_labels(variable_names, format_type='simple'):
    """
    변수명 리스트를 한글 라벨 리스트로 변환
    
    Args:
        variable_names (list): 변수명 리스트
        format_type (str): 출력 형식
            - 'simple': 한글 라벨만 (예: '교육수준')
            - 'with_var': 변수명 + 한글 (예: 'sob_01z1 (교육수준)')
            - 'newline': 변수명과 한글을 줄바꿈 (예: 'sob_01z1\n(교육수준)')
        
    Returns:
        list: 한글 라벨 리스트
    
    Example:
        >>> labels = get_korean_labels(['age', 'sob_01z1'], format_type='simple')
        >>> print(labels)  # ['만나이', '교육수준']
    """
    decoder = get_decoder()
    labels = []
    
    for var in variable_names:
        label = decoder.get_variable_label(var)
        
        if format_type == 'simple':
            labels.append(label)
        elif format_type == 'with_var':
            if label == var:
                labels.append(var)
            else:
                labels.append(f"{var} ({label})")
        elif format_type == 'newline':
            if label == var:
                labels.append(var)
            else:
                labels.append(f"{var}\n({label})")
        else:
            labels.append(label)
    
    return labels


def create_korean_labels_dict(variable_names):
    """
    변수명 리스트를 한글 라벨 딕셔너리로 변환
    
    Args:
        variable_names (list): 변수명 리스트
        
    Returns:
        dict: {변수명: 한글라벨} 딕셔너리
    
    Example:
        >>> labels_dict = create_korean_labels_dict(['age', 'sob_01z1'])
        >>> print(labels_dict)  # {'age': '만나이', 'sob_01z1': '교육수준'}
    """
    decoder = get_decoder()
    return {var: decoder.get_variable_label(var) for var in variable_names}


if __name__ == '__main__':
    # 테스트 코드
    print("=" * 60)
    print("Variable Decoder 테스트")
    print("=" * 60)
    
    decoder = VariableDecoder()
    
    # 단일 값 테스트
    print("\n1. 단일 값 디코딩:")
    print(f"sob_01z1, 5 → {decoder.decode_value('sob_01z1', 5)}")
    print(f"sob_01z1, 7 → {decoder.decode_value('sob_01z1', 7)}")
    
    # 변수 정보 테스트
    print("\n2. 변수 정보:")
    decoder.print_variable_summary('sob_01z1')
