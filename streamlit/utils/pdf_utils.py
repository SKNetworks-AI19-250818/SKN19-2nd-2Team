import os
from fpdf import FPDF

# 프로젝트 루트에 폰트를 두면 상대경로로 접근 가능
FONT_PATH = "NotoSansKR-Regular.ttf"

def build_pdf_bytes(name: str, comments: list[str]) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    # 폰트 등록
    if os.path.exists(FONT_PATH):
        pdf.add_font("Noto", "", FONT_PATH, uni=True)
        pdf.set_font("Noto", size=14)
    else:
        pdf.set_font("Helvetica", size=14)  # 영문 안전, 한글은 깨짐 가능

    pdf.cell(0, 10, txt=f"금연 상담 리포트 - {name}", ln=True)
    pdf.ln(5)

    if comments:
        for c in comments:
            pdf.multi_cell(0, 8, txt=c)
    else:
        pdf.multi_cell(0, 8, txt="모든 항목이 평균 이상입니다!")

    # fpdf2는 dest='S'로 문자열 반환 → bytes 변환
    return (pdf.output(dest="S")
            .encode("utf-8" if os.path.exists(FONT_PATH) else "latin1", "ignore"))
