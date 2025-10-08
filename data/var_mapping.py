"""
변수명 디코딩 딕셔너리
Community Health Survey 2024 기준

이 파일은 data_explain.csv를 기반으로 자동 생성되었습니다.
'⚠️ PDF 확인 필요' 표시가 있는 변수는 반드시 공식 가이드라인 PDF로 검증 필요합니다.

Usage:
    from data.var_mapping import VAR_DICT, get_var_name, get_var_value
    
    # 변수명 가져오기
    var_name = get_var_name('nua_01z2')  # '아침식사 빈도'
    
    # 코드값 의미 가져오기
    value_meaning = get_var_value('nua_01z2', 1)  # '주 5~7회'
"""

# ========================================
# 전체 변수 딕셔너리
# ========================================
VAR_DICT = {
    # ========================================
    # 기본정보
    # ========================================
    'EXAMIN_YEAR': {
        'name': '조사연도',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'note': '연속형 변수'
    },
    'exmprs_no': {
        'name': '조사대상자번호',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'note': '연속형 변수'
    },
    'age': {
        'name': '만 나이',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'note': '연속형 변수'
    },
    'sex': {
        'name': '성별',
        'category': '기본정보',
        'type': 'categorical',
        'values': {
            1: '남자',
            2: '여자'
        },
        'note': '⚠️ PDF에서 코드값 확인 완료 필요'
    },
    'CTPRVN_CODE': {
        'name': '시도번호',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'note': '코드 변수'
    },
    'PBHLTH_CODE': {
        'name': '보건소번호',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'note': '코드 변수'
    },
    'SPOT_NO': {
        'name': '표본지점번호',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'note': '지역간 중복번호 존재'
    },
    'HSHLD_CODE': {
        'name': '가구번호',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'note': '지역간/표본지점간 중복번호 존재'
    },
    'MBHLD_CODE': {
        'name': '가구원번호',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'note': '지역간/표본지점/가구간 중복번호 존재'
    },
    'DONG_TY_CODE': {
        'name': '동읍면구분',
        'category': '기본정보',
        'type': 'categorical',
        'values': None,
        'note': '⚠️ PDF 확인 필요 - 코드값 정보 없음'
    },
    'HOUSE_TY_CODE': {
        'name': '주택유형',
        'category': '기본정보',
        'type': 'categorical',
        'values': None,
        'note': '⚠️ PDF 확인 필요 - 코드값 정보 없음'
    },
    'signgu_code': {
        'name': '행정기관코드',
        'category': '기본정보',
        'type': 'continuous',
        'values': None
    },
    'kstrata': {
        'name': '층화변수',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'description': '각 동읍면별 주택유형에 따라 나뉘어진 분산추정층'
    },
    'wt_h': {
        'name': '가구가중치',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'description': '가구조사 가중치'
    },
    'wt_p': {
        'name': '개인가중치',
        'category': '기본정보',
        'type': 'continuous',
        'values': None,
        'description': '성/연령별 인구구조(주민등록인구기준)로 보정한 개인 가중치'
    },
    'mbhld_co': {
        'name': '가구원수_전체',
        'category': '기본정보',
        'type': 'continuous',
        'values': None
    },
    'reside_adult_co': {
        'name': '가구원수_만19세이상',
        'category': '기본정보',
        'type': 'continuous',
        'values': None
    },
    
    # ========================================
    # 가구정보
    # ========================================
    'fma_19z3': {
        'name': '세대유형',
        'category': '가구정보',
        'type': 'categorical',
        'values': {
            77: '응답거부',
            99: '모름'
        },
        'note': '⚠️ PDF 확인 필요 - 1~7번 코드값 누락'
    },
    'fma_04z1': {
        'name': '기초생활수급자여부',
        'category': '가구정보',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            9: '모름'
        },
        'note': '⚠️ PDF 확인 필요 - 1, 2번 코드값 누락'
    },
    'fma_12z1': {
        'name': '가구총소득_기준기간',
        'category': '가구정보',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            9: '모름'
        },
        'description': '최근 1년 동안의 가구총소득 설문(단위: 만원)',
        'note': '⚠️ PDF 확인 필요 - 주요 코드값 누락'
    },
    'fma_13z1': {
        'name': '가구총소득_Y금액',
        'category': '가구정보',
        'type': 'continuous',
        'values': None,
        'special_codes': {
            77777: '응답거부',
            99999: '모름'
        }
    },
    'fma_14z1': {
        'name': '가구총소득_M금액',
        'category': '가구정보',
        'type': 'continuous',
        'values': None,
        'special_codes': {
            77777: '응답거부',
            99999: '모름'
        }
    },
    'fma_24z2': {
        'name': '가구총소득_월평균금액',
        'category': '가구정보',
        'type': 'continuous',
        'values': None,
        'special_codes': {
            77: '응답거부',
            88: '비해당',
            99: '모름'
        },
        'description': 'fma_12,13,14 무응답인 경우 응답'
    },
    'nue_01z1': {
        'name': '가구식품안정성여부',
        'category': '가구정보',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            9: '모름'
        },
        'description': '최근 1년 동안의 식생활형편',
        'note': '⚠️ PDF 확인 필요 - 주요 코드값 누락'
    },
    'fma_27z1': {
        'name': '치매환자가구여부',
        'category': '가구정보',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            9: '모름'
        },
        'note': '⚠️ PDF 확인 필요 - 1, 2번 코드값 누락'
    },
    'fma_26z1': {
        'name': '치매환자가족거주여부',
        'category': '가구정보',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            8: '비해당',
            9: '모름'
        },
        'note': '⚠️ PDF 확인 필요 - 1, 2번 코드값 누락'
    },
    
    # ========================================
    # 건강행태 - 흡연
    # ========================================
    'smf_01z1': {
        'name': '평생 담배제품 사용경험',
        'category': '건강행태-흡연',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        },
        'description': '지금까지 모든 종류의 담배 제품(일반담배, 전자담배, 물담배 등) 사용 경험'
    },
    'sma_01z1': {
        'name': '일반담배 평생흡연량',
        'category': '건강행태-흡연',
        'type': 'categorical',
        'values': {
            1: '5갑(100개비) 미만',
            2: '5갑(100개비) 이상',
            3: '피운 적 없음'
        }
    },
    'sma_03z2': {
        'name': '일반담배 현재흡연상태',
        'category': '건강행태-흡연',
        'type': 'categorical',
        'values': {
            1: '매일 피움',
            2: '가끔 피움',
            3: '과거에는 피웠으나 현재 피우지 않음'
        }
    },
    'smb_01z1': {
        'name': '매일흡연자 하루흡연량',
        'category': '건강행태-흡연',
        'type': 'continuous',
        'unit': '개비',
        'values': None,
        'description': '매일 피우는 사람의 하루 평균 담배 개비 수'
    },
    'smb_02z1': {
        'name': '가끔흡연자 월간흡연일수',
        'category': '건강행태-흡연',
        'type': 'continuous',
        'unit': '일',
        'values': None,
        'description': '가끔 피우는 사람의 최근 1달 흡연 일수'
    },
    'smb_03z1': {
        'name': '가끔흡연자 일평균흡연량',
        'category': '건강행태-흡연',
        'type': 'continuous',
        'unit': '개비',
        'values': None,
        'description': '가끔 피우는 날의 하루 평균 개비 수'
    },
    'smb_04z1': {
        'name': '과거흡연자 흡연기간(년)',
        'category': '건강행태-흡연',
        'type': 'continuous',
        'unit': '년',
        'values': None,
        'description': '과거 흡연했던 총 기간 - 년 단위'
    },
    'smb_05z1': {
        'name': '과거흡연자 흡연기간(월)',
        'category': '건강행태-흡연',
        'type': 'continuous',
        'unit': '개월',
        'values': None,
        'description': '과거 흡연했던 총 기간 - 월 단위'
    },
    'smb_06z1': {
        'name': '과거흡연자 하루평균흡연량',
        'category': '건강행태-흡연',
        'type': 'continuous',
        'unit': '개비',
        'values': None,
        'description': '과거 피울 때 하루 평균 개비 수'
    },
    'smb_09z1': {
        'name': '금연유지기간',
        'category': '건강행태-흡연',
        'type': 'categorical',
        'values': {
            1: '1년 미만',
            2: '1년~5년 미만',
            3: '5년~10년 미만',
            4: '10년~15년 미만',
            5: '15년~20년 미만',
            6: '20년 이상'
        },
        'description': '담배를 끊은 지 얼마나 되었는지'
    },
    
    # ========================================
    # 건강행태 - 전자담배
    # ========================================
    'sma_36z1': {
        'name': '궐련형 전자담배 평생사용',
        'category': '건강행태-전자담배',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        },
        'description': '궐련형 전자담배(아이코스, 글로, 릴 등) 평생 사용 경험'
    },
    'sma_37z1': {
        'name': '궐련형 전자담배 현재사용',
        'category': '건강행태-전자담배',
        'type': 'categorical',
        'values': {
            1: '매일 피움',
            2: '가끔 피움',
            3: '과거에는 피웠으나 현재 피우지 않음'
        }
    },
    'smb_11z1': {
        'name': '궐련형 매일사용자 하루사용량',
        'category': '건강행태-전자담배',
        'type': 'continuous',
        'unit': '개비',
        'values': None,
        'description': '매일 피우는 사람의 하루 평균 개비 수'
    },
    'smb_12z1': {
        'name': '궐련형 가끔사용자 월간일수',
        'category': '건강행태-전자담배',
        'type': 'continuous',
        'unit': '일',
        'values': None,
        'description': '가끔 피우는 사람의 최근 1달 사용 일수'
    },
    'smb_13z1': {
        'name': '궐련형 가끔사용자 일평균량',
        'category': '건강행태-전자담배',
        'type': 'continuous',
        'unit': '개비',
        'values': None,
        'description': '가끔 피우는 날의 하루 평균 개비 수'
    },
    'sma_08z1': {
        'name': '액상형 전자담배 평생사용',
        'category': '건강행태-전자담배',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        },
        'description': '니코틴 포함 액상형 전자담배 평생 사용 경험'
    },
    'sma_11z2': {
        'name': '액상형 전자담배 현재사용',
        'category': '건강행태-전자담배',
        'type': 'continuous',
        'unit': '일/월',
        'values': None,
        'description': '최근 1달간 니코틴 포함 액상형 사용 일수'
    },
    'sma_12z2': {
        'name': '기타담배제품 사용경험',
        'category': '건강행태-전자담배',
        'type': 'categorical',
        'values': {
            1: '최근 1달 내',
            2: '과거만',
            3: '없음'
        },
        'description': '물담배, 스누스 등 기타 담배 사용'
    },
    
    # ========================================
    # 건강행태 - 금연의향
    # ========================================
    'smd_02z3': {
        'name': '최근 1년 금연시도 여부',
        'category': '건강행태-금연의향',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        },
        'description': '최근 1년간 24시간 이상 금연 시도 경험'
    },
    'smd_01z3': {
        'name': '금연계획',
        'category': '건강행태-금연의향',
        'type': 'categorical',
        'values': {
            1: '1개월 이내',
            2: '6개월 이내',
            3: '언젠가는 끊을 생각',
            4: '금연 생각 전혀 없음'
        },
        'description': '앞으로 담배를 끊을 계획'
    },
    
    # ========================================
    # 건강행태 - 간접흡연
    # ========================================
    'smc_08z2': {
        'name': '가정 내 흡연자 존재',
        'category': '건강행태-간접흡연',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        },
        'description': '본인 제외 가족 중 가정 실내 흡연자 유무'
    },
    'smc_09z2': {
        'name': '가정 간접흡연 노출',
        'category': '건강행태-간접흡연',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        },
        'description': '최근 1주일 가정 실내 간접흡연 경험'
    },
    'smc_10z2': {
        'name': '직장 간접흡연 노출',
        'category': '건강행태-간접흡연',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            3: '직장 없음'
        },
        'description': '최근 1주일 직장 실내 간접흡연 경험'
    },
    
    # ========================================
    # 건강행태 - 음주
    # ========================================
    'dra_01z1': {
        'name': '평생 음주 여부',
        'category': '건강행태-음주',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            7: '응답거부'
        }
    },
    'drb_01z3': {
        'name': '연간 음주 빈도',
        'category': '건강행태-음주',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            8: '비해당',
            9: '모름'
        },
        'note': '⚠️ PDF 확인 필요 - 1~6번 코드값 누락'
    },
    'drb_03z1': {
        'name': '한 번 섭취 시 음주량',
        'category': '건강행태-음주',
        'type': 'categorical',
        'values': None,
        'note': '⚠️ PDF 확인 필요 - 코드값 정보 없음'
    },
    'drb_16z1': {
        'name': '10잔 이상 섭취 시 음주량',
        'category': '건강행태-음주',
        'type': 'continuous',
        'unit': '잔',
        'values': None
    },
    'drb_04z1': {
        'name': '월간 폭음 경험(남)',
        'category': '건강행태-음주',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            8: '비해당',
            9: '모름'
        },
        'note': '⚠️ PDF 확인 필요 - 주요 코드값 누락'
    },
    'drb_05z1': {
        'name': '월간 폭음 경험(여)',
        'category': '건강행태-음주',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            8: '비해당',
            9: '모름'
        },
        'note': '⚠️ PDF 확인 필요 - 주요 코드값 누락'
    },
    'drg_01z3': {
        'name': '절주 또는 금주계획 여부',
        'category': '건강행태-음주',
        'type': 'categorical',
        'values': {
            7: '응답거부',
            8: '비해당',
            9: '모름'
        },
        'note': '⚠️ PDF 확인 필요 - 주요 코드값 누락'
    },
    'dre_03z1': {
        'name': '음주폐해 예방 또는 절주에 대한 홍보 경험 여부',
        'category': '건강행태-음주',
        'type': 'categorical',
        'values': None,
        'note': '⚠️ PDF 확인 필요 - 코드값 정보 없음'
    },
    'dre_04z1': {
        'name': '음주폐해 예방 또는 절주에 대한 교육 경험 여부',
        'category': '건강행태-음주',
        'type': 'categorical',
        'values': None,
        'note': '⚠️ PDF 확인 필요 - 코드값 정보 없음'
    },
    
    # ========================================
    # 건강행태 - 신체활동
    # ========================================
    'pha_04z1': {
        'name': '고강도 신체활동 일수',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '일',
        'values': None
    },
    'pha_05z1': {
        'name': '고강도 신체활동 시간(시)',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '시간',
        'values': None
    },
    'pha_06z1': {
        'name': '고강도 신체활동 시간(분)',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '분',
        'values': None
    },
    'pha_07z1': {
        'name': '중강도 신체활동 일수',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '일',
        'values': None
    },
    'pha_08z1': {
        'name': '중강도 신체활동 시간(시)',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '시간',
        'values': None
    },
    'pha_09z1': {
        'name': '중강도 신체활동 시간(분)',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '분',
        'values': None
    },
    'phb_01z1': {
        'name': '걷기 실천 일수',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '일',
        'values': None
    },
    'phb_02z1': {
        'name': '걷기 실천 시간(시)',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '시간',
        'values': None
    },
    'phb_03z1': {
        'name': '걷기 실천 시간(분)',
        'category': '건강행태-신체활동',
        'type': 'continuous',
        'unit': '분',
        'values': None
    },
    'pha_11z1': {
        'name': '최근 1주일 유연성 운동 실천',
        'category': '건강행태-신체활동',
        'type': 'categorical',
        'values': None,
        'note': '⚠️ PDF 확인 필요 - 코드값 정보 없음'
    },
    
    # ========================================
    # 건강행태 - 식생활
    # ========================================
    'nua_01z2': {
        'name': '아침식사 빈도',
        'category': '건강행태-식생활',
        'type': 'categorical',
        'values': {
            1: '주 5~7회',
            2: '주 3~4회',
            3: '주 1~2회',
            4: '거의 안함(주 0회)'
        }
    },
    'nuc_02z1': {
        'name': '영양표시 인지여부',
        'category': '건강행태-식생활',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'nuc_01z2': {
        'name': '영양표시 읽기여부',
        'category': '건강행태-식생활',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'nuc_03z1': {
        'name': '영양표시 영향여부',
        'category': '건강행태-식생활',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    
    # ========================================
    # 건강행태 - 비만 및 체중조절
    # ========================================
    'oba_02z1': {
        'name': '신장',
        'category': '건강행태-비만',
        'type': 'continuous',
        'unit': 'cm',
        'values': None
    },
    'oba_03z1': {
        'name': '체중',
        'category': '건강행태-비만',
        'type': 'continuous',
        'unit': 'kg',
        'values': None
    },
    'oba_bmi': {
        'name': '체질량지수(BMI)',
        'category': '건강행태-비만',
        'type': 'continuous',
        'unit': 'kg/m²',
        'values': None,
        'description': '체중(kg) ÷ (신장(cm)/100)², 저체중 <18.5, 정상 18.5–24.9, 과체중 25–29.9, 비만 ≥30'
    },
    'oba_01z1': {
        'name': '체형인지(자기평가)',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '매우 마름',
            2: '약간 마름',
            3: '보통',
            4: '약간 비만',
            5: '매우 비만'
        }
    },
    'obb_01z1': {
        'name': '체중조절시도여부',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02a1': {
        'name': '체중조절방법_운동',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02b1': {
        'name': '체중조절방법_단식',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02c1': {
        'name': '체중조절방법_식사조절',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02k1': {
        'name': '체중조절방법_결식',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02d1': {
        'name': '체중조절방법_무처방약물',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02e1': {
        'name': '체중조절방법_처방약물',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02f1': {
        'name': '체중조절방법_한약',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02g1': {
        'name': '체중조절방법_건강보조제',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02h1': {
        'name': '체중조절방법_원푸드다이어트',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'obb_02i1': {
        'name': '체중조절방법_기타',
        'category': '건강행태-비만',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    
    # ========================================
    # 건강행태 - 구강건강
    # ========================================
    'ora_01z1': {
        'name': '구강건강 자기평가',
        'category': '건강행태-구강',
        'type': 'categorical',
        'values': {
            1: '매우 좋음',
            2: '좋음',
            3: '보통',
            4: '나쁨',
            5: '매우 나쁨'
        }
    },
    'orb_01z1': {
        'name': '저작불편여부',
        'category': '건강행태-구강',
        'type': 'categorical',
        'values': {
            1: '매우 불편',
            2: '불편',
            3: '그저그렇다',
            4: '별로 불편하지 않다',
            5: '전혀 불편하지 않다'
        }
    },
    'ord_01d2': {
        'name': '점심후 양치여부',
        'category': '건강행태-구강',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'ord_05z1': {
        'name': '점심후 양치불가이유',
        'category': '건강행태-구강',
        'type': 'categorical',
        'values': None,
        'note': '⚠️ PDF 확인 필요 - 코드값 정보 없음'
    },
    'ord_01f3': {
        'name': '저녁 양치여부',
        'category': '건강행태-구강',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'ore_02z2': {
        'name': '치과진료 미수진경험',
        'category': '건강행태-구강',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'ore_03z2': {
        'name': '치과 미수진이유',
        'category': '건강행태-구강',
        'type': 'categorical',
        'values': {
            1: '시간없음',
            2: '증상경미',
            3: '경제적이유',
            4: '교통불편/거리멀음',
            5: '대기가길어서',
            6: '몸이불편/예약어려움',
            7: '치료두려움',
            8: '기타'
        }
    },
    'ore_07z1': {
        'name': '스케일링 경험',
        'category': '건강행태-구강',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    
    # ========================================
    # 정신건강 - 수면
    # ========================================
    'mtc_17z1': {
        'name': '일일 수면시간(주중)',
        'category': '정신건강-수면',
        'type': 'continuous',
        'unit': '시간',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_18z1': {
        'name': '일일 수면시간(주말)',
        'category': '정신건강-수면',
        'type': 'continuous',
        'unit': '시간',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    
    # ========================================
    # 정신건강 - 스트레스
    # ========================================
    'mta_01z1': {
        'name': '스트레스 정도',
        'category': '정신건강-스트레스',
        'type': 'categorical',
        'values': {
            1: '대단히 많이 느낀다',
            2: '많이 느끼는 편이다',
            3: '조금 느끼는 편이다',
            4: '거의 느끼지 않는다',
            7: '응답거부',
            9: '모름'
        }
    },
    'mta_02z1': {
        'name': '스트레스로 인한 상담여부',
        'category': '정신건강-스트레스',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            7: '응답거부',
            8: '비해당',
            9: '모름'
        }
    },
    
    # ========================================
    # 정신건강 - 우울/슬픔
    # ========================================
    'mtb_01z1': {
        'name': '슬픔, 절망감 여부',
        'category': '정신건강-우울',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        }
    },
    'mtb_02z1': {
        'name': '슬픔, 절망감 상담여부',
        'category': '정신건강-우울',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07a1': {
        'name': '일의 흥미 여부',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07b1': {
        'name': '가라앉는 느낌, 우울, 절망감 여부',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07c1': {
        'name': '잠들기 어렵거나 많이 잠',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07d1': {
        'name': '피로감, 기력저하',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07e1': {
        'name': '식욕 저하 혹은 과식',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07f1': {
        'name': '본인이 나쁜 사람이라는 느낌',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07g1': {
        'name': '신문, TV 집중 어려움',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07h1': {
        'name': '거동, 언어 느림, 초조하여 안절부절 못함',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtb_07i1': {
        'name': '자살 생각 혹은 스스로에게 상처 주는 생각',
        'category': '정신건강-우울증상',
        'type': 'categorical',
        'values': {
            1: '전혀 아니다',
            2: '여러날 동안',
            3: '일주일 이상',
            4: '거의 매일',
            7: '응답거부',
            9: '모름'
        }
    },
    
    # ========================================
    # 정신건강 - 자살
    # ========================================
    'mtd_01z1': {
        'name': '자살 생각',
        'category': '정신건강-자살',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtd_02z1': {
        'name': '자살 생각으로 인한 상담여부',
        'category': '정신건강-자살',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            7: '응답거부',
            8: '비해당',
            9: '모름'
        }
    },
    
    # ========================================
    # 정신건강 - 수면의 질
    # ========================================
    'edit_mtc_03z1': {
        'name': '언제 잠에 드는지(시간)',
        'category': '정신건강-수면질',
        'type': 'continuous',
        'unit': '시',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_04z1': {
        'name': '언제 잠에 드는지(분)',
        'category': '정신건강-수면질',
        'type': 'continuous',
        'unit': '분',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_05z1': {
        'name': '잠에 드는데 걸리는 시간(시간)',
        'category': '정신건강-수면질',
        'type': 'continuous',
        'unit': '시간',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_06z1': {
        'name': '잠에 드는데 걸리는 시간(분)',
        'category': '정신건강-수면질',
        'type': 'continuous',
        'unit': '분',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_08z1': {
        'name': '몇시에 일어나는지(시간)',
        'category': '정신건강-수면질',
        'type': 'continuous',
        'unit': '시',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_09z1': {
        'name': '몇시에 일어나는지(분)',
        'category': '정신건강-수면질',
        'type': 'continuous',
        'unit': '분',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_10z1': {
        'name': '실제로 잔 시간(시간)',
        'category': '정신건강-수면질',
        'type': 'continuous',
        'unit': '시간',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_11z1': {
        'name': '실제로 잔 시간(분)',
        'category': '정신건강-수면질',
        'type': 'continuous',
        'unit': '분',
        'values': None,
        'special_codes': {
            77: '응답거부',
            99: '모름'
        }
    },
    'mtc_12a1': {
        'name': '30분 이내에 잠들 수 없었는지',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12b1': {
        'name': '중간에 깸',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12c1': {
        'name': '화장실을 가기위해 일어남',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12d1': {
        'name': '편안한 호흡불가',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12e1': {
        'name': '기침 or 코를 곪',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12f1': {
        'name': '잠자는데 추웠다',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12g1': {
        'name': '잠자는데 더웠다',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12h1': {
        'name': '나쁜꿈을 꾸었다',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12i1': {
        'name': '통증이 있었다',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_12j1': {
        'name': '그외 다른 이유가 있었다',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_13z1': {
        'name': '수면의 질',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '매우 좋음',
            2: '상당히 좋음',
            3: '상당히 나쁨',
            4: '매우 나쁨',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_14z1': {
        'name': '잠에 들기 위해 약 복용 여부',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtc_15z1': {
        'name': '운전, 식사, 사회활동중 졸음 여부',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '지난 한 달 동안 없었다',
            2: '주 1회 미만',
            3: '주 1~2회',
            4: '주 3회 이상'
        }
    },
    'mtc_16z1': {
        'name': '일에 열중하는데 문제 여부',
        'category': '정신건강-수면질',
        'type': 'categorical',
        'values': {
            1: '전혀 없었다',
            2: '매우 조금 있었다',
            3: '다소 있었다',
            4: '매우 많이 있었다',
            7: '응답거부',
            9: '모름'
        }
    },
    
    # ========================================
    # 정신건강 - 치매 및 인지장애
    # ========================================
    'mtj_05z2': {
        'name': '정신 혼란 또는 기억력 저하',
        'category': '정신건강-인지',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            7: '응답거부',
            8: '비해당',
            9: '모름'
        }
    },
    'mtj_06z2': {
        'name': '집안일을 못한적이 있는지',
        'category': '정신건강-인지',
        'type': 'categorical',
        'values': {
            1: '항상 못했다',
            2: '대체로 못했다',
            3: '가끔 못했다',
            4: '거의 못한적 없다',
            5: '전혀 못한적 없다',
            7: '응답거부',
            8: '비해당',
            9: '모름'
        }
    },
    'mtj_09z2': {
        'name': '직장생활, 사회생활을 못한적이 있는지',
        'category': '정신건강-인지',
        'type': 'categorical',
        'values': {
            1: '항상 못했다',
            2: '대체로 못했다',
            3: '가끔 못했다',
            4: '거의 못한적 없다',
            5: '전혀 못한적 없다',
            7: '응답거부',
            8: '비해당',
            9: '모름'
        }
    },
    'mtj_10z1': {
        'name': '상담 여부',
        'category': '정신건강-인지',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            7: '응답거부',
            9: '모름'
        }
    },
    'mtj_11z1': {
        'name': '치매선별검사 여부',
        'category': '정신건강-인지',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            8: '비해당',
            9: '모름'
        }
    },
    
    # ========================================
    # 보건기관 이용
    # ========================================
    'hma_01z3': {
        'name': '보건기관 이용여부',
        'category': '보건기관이용',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오',
            9: '모름'
        }
    },
    
    # ========================================
    # 교육 및 경제활동
    # ========================================
    'sob_01z1': {
        'name': '교육수준(최종학력)',
        'category': '교육경제-교육',
        'type': 'categorical',
        'values': {
            1: '무학',
            2: '서당/한학',
            3: '초등학교',
            4: '중학교',
            5: '고등학교',
            6: '2-3년제 대학',
            7: '4년제 대학',
            8: '대학원 이상'
        },
        'note': '⚠️ PDF 확인 필요 - 9번 모름 코드 확인'
    },
    'sob_02z1': {
        'name': '졸업상태',
        'category': '교육경제-교육',
        'type': 'categorical',
        'values': {
            1: '졸업',
            2: '수료',
            3: '중퇴',
            4: '재학/휴학중'
        },
        'note': '⚠️ PDF 확인 필요 - 8, 9번 코드 확인'
    },
    'soa_01z1': {
        'name': '경제활동 여부',
        'category': '교육경제-경제',
        'type': 'categorical',
        'values': {
            1: '예',
            2: '아니오'
        },
        'description': '최근 1주일간 수입목적 1시간 이상 근로 또는 18시간 이상 무급가족종사 여부'
    },
    'soa_06z2': {
        'name': '직업분류(재분류)',
        'category': '교육경제-직업',
        'type': 'categorical',
        'values': {
            1: '관리자',
            2: '전문가 및 관련 종사자',
            3: '사무 종사자',
            4: '서비스 종사자',
            5: '판매 종사자',
            6: '농림어업 숙련 종사자',
            7: '기능원 및 관련 기능 종사자',
            8: '장치/기계조작 및 조립 종사자',
            9: '단순노무 종사자',
            10: '군인'
        },
        'note': '⚠️ PDF 확인 필요 - 88, 99번 코드 확인'
    },
    'soa_07z1': {
        'name': '종사상 지위',
        'category': '교육경제-직업',
        'type': 'categorical',
        'values': {
            1: '고용주 및 자영업자',
            2: '임금근로자',
            3: '무급가족종사자'
        },
        'note': '⚠️ PDF 확인 필요 - 8, 9번 코드 확인'
    },
    'sod_02z3': {
        'name': '혼인상태',
        'category': '교육경제-가족',
        'type': 'categorical',
        'values': {
            1: '배우자와 동거',
            2: '배우자와 별거',
            3: '사별',
            4: '이혼',
            5: '미혼'
        }
    },
    
    # ========================================
    # 타겟 변수
    # ========================================
    'churn': {
        'name': '금연 성공 여부',
        'category': '타겟',
        'type': 'categorical',
        'values': {
            0: '금연 실패(현재 흡연자)',
            1: '금연 성공(과거 흡연자)'
        },
        'description': '과거 흡연 경험이 있고 현재는 금연 중인 상태'
    }
}


# ========================================
# 헬퍼 함수
# ========================================
def get_var_name(var_code):
    """변수 코드로 변수명 조회"""
    if var_code in VAR_DICT:
        return VAR_DICT[var_code]['name']
    return f"Unknown variable: {var_code}"


def get_var_value(var_code, value):
    """변수 코드와 값으로 의미 조회"""
    if var_code not in VAR_DICT:
        return f"Unknown variable: {var_code}"
    
    var_info = VAR_DICT[var_code]
    
    # 연속형 변수
    if var_info['type'] == 'continuous':
        if 'special_codes' in var_info and value in var_info['special_codes']:
            return var_info['special_codes'][value]
        unit = var_info.get('unit', '')
        return f"{value} {unit}".strip()
    
    # 범주형 변수
    if var_info['values'] is None:
        return f"{value} (코드값 정보 없음)"
    
    if value in var_info['values']:
        return var_info['values'][value]
    
    return f"{value} (정의되지 않은 코드)"


def get_var_info(var_code):
    """변수의 전체 정보 조회"""
    if var_code not in VAR_DICT:
        return None
    return VAR_DICT[var_code]


def list_vars_by_category(category):
    """카테고리별 변수 목록 조회"""
    return [
        var_code for var_code, info in VAR_DICT.items() 
        if info.get('category') == category
    ]


def get_all_categories():
    """모든 카테고리 목록 조회"""
    categories = set()
    for info in VAR_DICT.values():
        if 'category' in info:
            categories.add(info['category'])
    return sorted(list(categories))


# ========================================
# PDF 확인 필요한 변수 리스트
# ========================================
NEEDS_PDF_VERIFICATION = [
    var_code for var_code, info in VAR_DICT.items() 
    if 'note' in info and 'PDF 확인 필요' in info['note']
]
