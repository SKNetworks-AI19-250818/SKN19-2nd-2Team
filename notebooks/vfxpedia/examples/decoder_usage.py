# VariableDecoder 사용 예제

"""
이 파일은 VariableDecoder의 사용법을 보여줍니다.
notebooks에서 import해서 사용하세요.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils.variable_decoder import VariableDecoder

# 한글 폰트 설정 (Windows)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False


def example_1_basic_decoding():
    """예제 1: 기본 디코딩"""
    print("\n" + "="*60)
    print("📌 예제 1: 기본 디코딩")
    print("="*60)
    
    decoder = VariableDecoder()
    
    # 단일 값 디코딩
    result1 = decoder.decode_value('smb_09z1', 1.0)
    result2 = decoder.decode_value('smb_09z1', 2.0)
    result3 = decoder.decode_value('sob_01z1', 5.0)
    
    print(f"smb_09z1, 1.0 → {result1}")
    print(f"smb_09z1, 2.0 → {result2}")
    print(f"sob_01z1, 5.0 → {result3}")


def example_2_dataframe_decoding():
    """예제 2: 데이터프레임 컬럼 디코딩"""
    print("\n" + "="*60)
    print("📌 예제 2: 데이터프레임 디코딩")
    print("="*60)
    
    # 샘플 데이터 생성
    df = pd.DataFrame({
        'smb_09z1': [1.0, 2.0, 3.0, 1.0, 2.0],
        'sob_01z1': [5.0, 7.0, 4.0, 5.0, 8.0],
        'churn': [0, 1, 1, 0, 1]
    })
    
    print("\n원본 데이터:")
    print(df.head())
    
    # 디코딩
    decoder = VariableDecoder()
    df_decoded = decoder.decode_multiple_columns(
        df, 
        ['smb_09z1', 'sob_01z1']
    )
    
    print("\n디코딩 후:")
    print(df_decoded.head())


if __name__ == '__main__':
    example_1_basic_decoding()
    example_2_dataframe_decoding()
    
    print("\n✅ 예제 실행 완료!")
