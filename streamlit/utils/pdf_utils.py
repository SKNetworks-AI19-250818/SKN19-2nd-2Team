# utils/pdf_utils.py
from pathlib import Path
from fpdf import FPDF
import streamlit as st

# ✅ 새로 추가: 윈도우 시스템 폰트 경로 포함
_FONT_CANDIDATES = [
    # 프로젝트 내 폰트 경로 (있으면 사용)
    Path(__file__).resolve().parents[1] / "assets" / "fonts" / "NotoSansKR-Regular.ttf",
    Path.cwd() / "streamlit" / "assets" / "fonts" / "NotoSansKR-Regular.ttf",
    Path.cwd() / "assets" / "fonts" / "NotoSansKR-Regular.ttf",
    Path(__file__).resolve().parents[2] / "streamlit" / "assets" / "fonts" / "NotoSansKR-Regular.ttf",
    # ✅ 새로 추가: 윈도우 11 시스템 폰트 (맑은 고딕)
    Path("C:/Windows/Fonts/malgun.ttf"),      # 맑은 고딕
    Path("C:/Windows/Fonts/gulim.ttc"),       # 굴림 (대체)
]

def _pick_font_path():
    """사용 가능한 한글 폰트 경로를 찾아 반환"""
    for p in _FONT_CANDIDATES:
        if p.exists():
            return p
    return None

def _latin1(s) -> str:
    """한글 등 비지원 문자를 대체문자로 바꾸어 라틴-1 폰트로도 출력 가능하게."""
    return str(s).encode("latin-1", "replace").decode("latin-1")

# ✅ 새로 추가: PDF에 포함할 상세 정보 생성 함수
def _build_report_content(name: str) -> list[str]:
    """
    세션에서 환자 정보를 읽어 PDF 내용 생성
    
    ✅ 수정: 세션 데이터 디버깅 추가, 실제 입력 데이터 반영
    """
    lines = []
    
    # ✅ 수정: 세션 상태 디버깅
    print(f"[PDF 생성] 환자명: {name}")
    print(f"[PDF 생성] 세션 키들: {list(st.session_state.keys())}")
    
    # 환자 기본 정보
    patient = st.session_state.get("patient", {})
    print(f"[PDF 생성] patient 데이터: {patient}")
    
    lines.append(f"환자명: {name}")
    lines.append(f"나이: {patient.get('나이', '-')}세")
    lines.append(f"성별: {patient.get('성별', '-')}")
    lines.append(f"방문일: {patient.get('날짜', '-')}")
    lines.append(f"BMI: {patient.get('BMI', '-')}")
    lines.append("")
    
    # ✅ 수정: features_raw와 features_enc 모두 확인
    features_raw = st.session_state.get("features_raw", {})
    features_enc = st.session_state.get("features_enc", {})
    
    print(f"[PDF 생성] features_raw 키들: {list(features_raw.keys()) if features_raw else 'None'}")
    print(f"[PDF 생성] features_enc 키들: {list(features_enc.keys()) if features_enc else 'None'}")
    
    if features_raw:
        lines.append("[ 입력 정보 ]")
        lines.append("")
        
        # ✅ 수정: 더 많은 정보 포함
        if "아침식사빈도" in features_raw:
            val = str(features_raw['아침식사빈도'])[:20]
            lines.append(f"아침식사 빈도: {val}")
        if "연간 음주 빈도" in features_raw:
            val = str(features_raw['연간 음주 빈도'])[:20]
            lines.append(f"연간 음주 빈도: {val}")
        if "한 번 섭취 시 음주량" in features_raw:
            val = features_raw['한 번 섭취 시 음주량']
            lines.append(f"1회 음주량: {val}잔")
        if "스트레스" in features_raw:
            val = features_raw['스트레스']
            lines.append(f"스트레스 수준: {val}/5")
        if "구강건강자기평가" in features_raw:
            val = str(features_raw['구강건강자기평가'])[:15]
            lines.append(f"구강건강: {val}")
        if "최근 1주일 유연성 운동 실천" in features_raw:
            val = str(features_raw['최근 1주일 유연성 운동 실천'])[:15]
            lines.append(f"유연성운동: {val}")
        if "가정내흡연자존재" in features_raw:
            val = str(features_raw['가정내흡연자존재'])[:10]
            lines.append(f"가정흡연자: {val}")
        if "occupation_type" in features_raw:
            val = str(features_raw['occupation_type'])[:10]
            lines.append(f"직업: {val}")
        
        lines.append("")
    else:
        lines.append("[ 입력 정보 없음 - 세션 데이터 확인 필요 ]")
        lines.append("")
    
    # 예측 결과 (세션에서 가져오기)
    pred_prob = st.session_state.get("_prediction_probability")
    print(f"[PDF 생성] 예측 확률: {pred_prob}")
    
    if pred_prob is not None:
        lines.append("[ 예측 결과 ]")
        lines.append("")
        lines.append(f"금연 성공 확률: {pred_prob:.1f}%")
        
        if pred_prob >= 70:
            status = "높음"
            desc = "금연 성공 가능성이 높습니다."
        elif pred_prob >= 50:
            status = "보통"
            desc = "적절한 관리가 필요합니다."
        else:
            status = "낮음"
            desc = "집중 관리가 필요합니다."
        
        lines.append(f"성공 가능성: {status}")
        lines.append(desc)
        lines.append("")
    else:
        lines.append("[ 예측 결과 없음 ]")
        lines.append("")
    
    # 권장사항 (더 구체적으로)
    lines.append("[ 권장사항 ]")
    lines.append("")
    lines.append("1. 규칙적인 운동 (주 3-5회 유산소)")
    lines.append("2. 스트레스 관리 (명상, 호흡법)")
    lines.append("3. 규칙적 아침식사 (단백질, 섬유질)")
    lines.append("4. 적정 음주량 유지")
    lines.append("5. 정기 구강 관리 (양치, 치실)")
    lines.append("")
    lines.append("전문가와 정기적인 상담을 권장합니다.")
    
    return lines

def build_pdf_bytes(name: str, comments: list[str]) -> bytes:
    """
    환자 금연 상담 리포트 PDF 생성
    
    ✅ 개선사항:
    - 윈도우 11 시스템 폰트(맑은 고딕) 사용으로 한글 깨짐 해결
    - 세션 상태에서 환자 정보를 자동으로 읽어와 상세 리포트 생성
    - 예측 결과와 권장사항 포함
    
    ✅ 수정: 페이지 마진 넉넉히 설정, 짧은 텍스트만 사용
    """
    try:
        # ✅ 수정: 마진을 더 넉넉하게 설정 (20mm)
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(left=20, top=20, right=20)
        pdf.set_auto_page_break(auto=True, margin=20)
        pdf.add_page()

        font_path = _pick_font_path()
        
        if font_path is not None:
            # ✅ 한글 폰트를 찾은 경우: 정상 한글 출력
            try:
                print(f"[PDF 생성] 폰트 경로: {font_path}")
                pdf.add_font("KoreanFont", "", str(font_path), uni=True)
                pdf.set_font("KoreanFont", size=14)
                
                # 제목
                pdf.cell(0, 10, txt="금연 상담 리포트", ln=True, align="C")
                pdf.ln(8)
                
                # 내용
                pdf.set_font("KoreanFont", size=10)
                
                # ✅ 새로 추가: 세션에서 상세 정보 생성
                content_lines = _build_report_content(name)
                print(f"[PDF 생성] 생성된 라인 수: {len(content_lines)}")
                
                # ✅ 수정: 한 줄씩 안전하게 출력 (에러 발생 시 해당 줄만 스킵)
                for i, line in enumerate(content_lines):
                    try:
                        if line.strip() == "":
                            pdf.ln(4)  # 빈 줄은 간격만 추가
                        else:
                            # ✅ 수정: 더 안전한 출력 방식
                            clean_line = str(line).replace("\n", " ").replace("\r", " ")
                            pdf.multi_cell(w=0, h=6, txt=clean_line, border=0, align='L')
                    except Exception as line_error:
                        # 특정 줄에서 에러 발생 시 해당 줄만 스킵
                        print(f"라인 {i} 출력 실패: {line[:30]}... - {line_error}")
                        continue
                
                # 사용자 제공 코멘트 추가
                if comments:
                    pdf.ln(5)
                    pdf.set_font("KoreanFont", size=10)
                    for line in comments:
                        try:
                            if line.strip() != "":
                                clean_line = str(line).replace("\n", " ").replace("\r", " ")
                                pdf.multi_cell(w=0, h=6, txt=clean_line, border=0, align='L')
                        except:
                            continue
                
                print("[PDF 생성] 한글 폰트로 PDF 생성 완료")
                return pdf.output(dest="S").encode("latin-1", "replace")
            
            except Exception as e:
                # ✅ 수정: 에러 발생 시 상세 정보 출력
                import traceback
                error_msg = f"한글 폰트 PDF 생성 중 에러: {str(e)}"
                print(error_msg)
                print(traceback.format_exc())
                # 간단한 버전으로 폴백

        # ❗ 폰트를 못 찾았거나 에러 발생 시: 간단한 버전 (더 많은 정보 포함)
        print("[PDF 생성] 폴백 모드: 한글 폰트 없이 영문으로 생성")
        
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        pdf.set_margins(left=20, top=20, right=20)
        pdf.add_page()
        
        pdf.set_font("helvetica", size=12)
        pdf.cell(0, 10, txt="Smoking Cessation Report", ln=True, align="C")
        pdf.ln(5)
        
        pdf.set_font("helvetica", size=10)
        pdf.cell(0, 8, txt=f"Name: {_latin1(name)}", ln=True)
        
        patient = st.session_state.get("patient", {})
        pdf.cell(0, 8, txt=f"Age: {patient.get('나이', '-')}", ln=True)
        pdf.cell(0, 8, txt=f"Gender: {_latin1(patient.get('성별', '-'))}", ln=True)
        pdf.cell(0, 8, txt=f"Date: {patient.get('날짜', '-')}", ln=True)
        pdf.cell(0, 8, txt=f"BMI: {patient.get('BMI', '-')}", ln=True)
        pdf.ln(3)
        
        # ✅ 수정: 입력 정보도 포함
        features_raw = st.session_state.get("features_raw", {})
        if features_raw:
            pdf.cell(0, 8, txt="[ Input Information ]", ln=True)
            pdf.ln(2)
            
            if "스트레스" in features_raw:
                pdf.cell(0, 6, txt=f"Stress Level: {features_raw['스트레스']}/5", ln=True)
            if "한 번 섭취 시 음주량" in features_raw:
                pdf.cell(0, 6, txt=f"Drink per Occasion: {features_raw['한 번 섭취 시 음주량']} glasses", ln=True)
            if "연간 음주 빈도" in features_raw:
                pdf.cell(0, 6, txt=f"Annual Drinking Freq: {_latin1(str(features_raw['연간 음주 빈도'])[:15])}", ln=True)
            if "아침식사빈도" in features_raw:
                pdf.cell(0, 6, txt=f"Breakfast Freq: {_latin1(str(features_raw['아침식사빈도'])[:15])}", ln=True)
            if "구강건강자기평가" in features_raw:
                pdf.cell(0, 6, txt=f"Oral Health: {_latin1(str(features_raw['구강건강자기평가'])[:15])}", ln=True)
            pdf.ln(3)
        
        pred_prob = st.session_state.get("_prediction_probability")
        if pred_prob:
            pdf.cell(0, 8, txt="[ Prediction Results ]", ln=True)
            pdf.ln(2)
            pdf.cell(0, 8, txt=f"Success Rate: {pred_prob:.1f}%", ln=True)
            
            if pred_prob >= 70:
                status = "High"
            elif pred_prob >= 50:
                status = "Medium"
            else:
                status = "Low"
            
            pdf.cell(0, 8, txt=f"Success Possibility: {status}", ln=True)
            pdf.ln(3)
        
        pdf.cell(0, 8, txt="[ Recommendations ]", ln=True)
        pdf.ln(2)
        pdf.cell(0, 6, txt="1. Regular exercise (3-5 times/week)", ln=True)
        pdf.cell(0, 6, txt="2. Stress management (meditation, breathing)", ln=True)
        pdf.cell(0, 6, txt="3. Regular breakfast", ln=True)
        pdf.cell(0, 6, txt="4. Moderate alcohol consumption", ln=True)
        pdf.cell(0, 6, txt="5. Regular oral hygiene", ln=True)
        
        print("[PDF 생성] 폴백 PDF 생성 완료")
        return bytes(pdf.output(dest="S"))
        
    except Exception as e:
        # ✅ 최후의 폴백: 에러 메시지를 streamlit에 표시하기 위해 다시 raise
        import traceback
        print(f"치명적 PDF 생성 에러: {str(e)}")
        print(traceback.format_exc())
        raise Exception(f"PDF 생성 실패: {str(e)}")




# # utils/pdf_utils.py
# from pathlib import Path
# from fpdf import FPDF

# # 폰트 경로 (프로젝트 구조에 맞춰 조정)
# FONT_PATH = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "NotoSansKR-Regular.ttf"

# def _strip_emoji(s: str) -> str:
#     # 이모지는 PDF 폰트가 없으면 문제라 제거 권장 (원하면 pass로 바꿔도 됨)
#     try:
#         import re
#         emoji_pattern = re.compile(
#             "["
#             "\U0001F600-\U0001F64F"  # emoticons
#             "\U0001F300-\U0001F5FF"  # symbols & pictographs
#             "\U0001F680-\U0001F6FF"  # transport & map symbols
#             "\U0001F1E0-\U0001F1FF"  # flags
#             "\U00002700-\U000027BF"  # dingbats
#             "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
#             "\U00002600-\U000026FF"  # Misc symbols
#             "]+",
#             flags=re.UNICODE,
#         )
#         return emoji_pattern.sub("", s)
#     except Exception:
#         return s  # 문제가 생기면 그냥 원문 반환

# def build_pdf_bytes(name: str, comments: list[str]) -> bytes:
#     pdf = FPDF()
#     pdf.set_auto_page_break(auto=True, margin=15)
#     pdf.add_page()

#     # ✅ 유니코드 폰트 등록 + 설정
#     if not FONT_PATH.exists():
#         raise FileNotFoundError(f"한글 폰트 파일을 찾을 수 없습니다: {FONT_PATH}")

#     pdf.add_font("NotoKR", "", str(FONT_PATH), uni=True)
#     pdf.set_font("NotoKR", size=16)

#     # 타이틀
#     title = f"금연 상담 리포트 - {name}"
#     pdf.cell(0, 10, txt=_strip_emoji(title), ln=True)

#     pdf.ln(5)
#     pdf.set_font("NotoKR", size=12)

#     if comments:
#         for c in comments:
#             pdf.multi_cell(0, 8, txt=_strip_emoji(c))
#     else:
#         pdf.multi_cell(0, 8, txt="모든 항목이 평균 이상입니다.")

#     # ✅ fpdf2 권장 방식: 문자열 반환 후 latin-1 인코딩
#     # (내부는 바이너리 스트림이지만 fpdf2는 str을 리턴하므로 latin-1로 안전 인코딩)
#     return pdf.output(dest="S").encode("latin-1")


# def build_pdf_bytes(name, comments):
#     pdf = FPDF()
#     pdf.add_page()

#     # ✅ 폰트 등록
#     pdf.add_font("NotoSansKR", "", str(FONT_PATH), uni=True)
#     pdf.set_font("NotoSansKR", size=14)

#     pdf.cell(200, 10, txt=f"{name} 금연 상담 리포트", ln=True, align="C")

#     for line in comments:
#         pdf.multi_cell(0, 10, txt=line)

#     return pdf.output(dest="S").encode("latin1", "replace")
