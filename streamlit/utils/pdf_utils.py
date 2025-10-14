import os
from fpdf import FPDF

# 우선순위: 로컬 TTF(동일 디렉토리) → Windows 맑은고딕 → 기본 헬베티카(영문만)
LOCAL_FONT = os.path.join(os.path.dirname(__file__), "NotoSansKR-Regular.ttf")
WIN_FONT = r"C:\\Windows\\Fonts\\malgun.ttf"

def build_pdf_bytes(name: str, comments: list[str]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    # 폰트 등록 (유니코드 지원)
    if os.path.exists(LOCAL_FONT):
        pdf.add_font("Noto", "", LOCAL_FONT, uni=True)
        pdf.set_font("Noto", size=14)
        current_font = "unicode"
    elif os.path.exists(WIN_FONT):
        pdf.add_font("Malgun", "", WIN_FONT, uni=True)
        pdf.set_font("Malgun", size=14)
        current_font = "unicode"
    else:
        pdf.set_font("Helvetica", size=14)
        current_font = "latin"

    pdf.cell(0, 10, txt=f"금연 상담 리포트 - {name}", ln=True)
    pdf.ln(5)

    if comments:
        for c in comments:
            # 텍스트 길이 제한 및 안전한 처리
            safe_text = str(c)[:200] if len(str(c)) > 200 else str(c)
            pdf.multi_cell(0, 8, txt=safe_text)
    else:
        pdf.multi_cell(0, 8, txt="모든 항목이 평균 이상입니다!")

    # fpdf2는 dest='S'로 bytes/bytearray/str를 반환할 수 있음 → 항상 bytes로 변환
    out = pdf.output(dest="S")
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    # 일부 구버전에서 str을 반환하는 경우 대비
    encoding = "utf-8" if current_font == "unicode" else "latin1"
    return out.encode(encoding, "ignore")
