import pandas as pd

# 두 파일 로드
full_df = pd.read_csv('CHS_Variable_full_table.csv', encoding='utf-8-sig')
current_df = pd.read_csv('variable.csv', encoding='utf-8-sig')

print(f"CHS_Variable_full_table.csv: {len(full_df)}행")
print(f"현재 variable.csv: {len(current_df)}행")

# 변수별로 그룹화하여 비교
full_vars = set(full_df['variable'].unique())
current_vars = set(current_df['variable'].unique())

print(f"\nCHS_Variable_full_table의 고유 변수: {len(full_vars)}개")
print(f"현재 variable.csv의 고유 변수: {len(current_vars)}개")

all_missing_rows = []

# 1. 현재 variable.csv에 없는 변수 전체 추가
missing_vars = full_vars - current_vars
print(f"\n1단계: 누락된 변수 {len(missing_vars)}개 추가")
if missing_vars:
    missing_var_rows = full_df[full_df['variable'].isin(missing_vars)]
    print(f"  추가할 행: {len(missing_var_rows)}행")
    all_missing_rows.extend(missing_var_rows.to_dict('records'))

# CHS_Variable_full_table에서 현재 variable.csv에 있는 변수만 필터링
filtered_full_df = full_df[full_df['variable'].isin(current_vars)]

print(f"\n필터링 후 CHS_Variable_full_table: {len(filtered_full_df)}행")

# 2. 기존 변수들의 누락된 코드 추가
print(f"\n2단계: 기존 변수들의 누락된 코드 확인")

for var in current_vars:
    full_rows = full_df[full_df['variable'] == var]
    current_rows = current_df[current_df['variable'] == var]
    
    # code 기준으로 비교
    full_codes = set(full_rows['code'].astype(str))
    current_codes = set(current_rows['code'].astype(str))
    
    missing_codes = full_codes - current_codes
    
    if missing_codes:
        print(f"  {var}: {len(missing_codes)}개 코드 누락")
        for missing_code in missing_codes:
            missing_row = full_rows[full_rows['code'].astype(str) == missing_code]
            if not missing_row.empty:
                all_missing_rows.append(missing_row.iloc[0].to_dict())

if all_missing_rows:
    print(f"\n총 추가할 행: {len(all_missing_rows)}개")
    
    # 누락된 행들을 현재 variable.csv에 추가
    missing_df = pd.DataFrame(all_missing_rows)
    updated_df = pd.concat([current_df, missing_df], ignore_index=True)
    
    # variable, code 기준으로 정렬
    updated_df = updated_df.sort_values(['variable', 'code'])
    
    # 중복 제거
    updated_df = updated_df.drop_duplicates(subset=['variable', 'code'], keep='first')
    
    # 저장
    updated_df.to_csv('variable.csv', index=False, encoding='utf-8-sig')
    
    print(f"\n[OK] variable.csv 업데이트 완료!")
    print(f"   업데이트 전: {len(current_df)}행")
    print(f"   업데이트 후: {len(updated_df)}행")
    print(f"   추가된 행: {len(all_missing_rows)}행")
else:
    print("\n[OK] 누락된 행 없음. variable.csv는 최신 상태입니다!")

