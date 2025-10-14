# utils/pdf_utils.py
from pathlib import Path
from fpdf import FPDF

# 폰트 경로 (프로젝트 구조에 맞춰 조정)
FONT_PATH = Path(__file__).resolve().parents[1] / "assets" / "fonts" / "NotoSansKR-Regular.ttf"

def _strip_emoji(s: str) -> str:
    # 이모지는 PDF 폰트가 없으면 문제라 제거 권장 (원하면 pass로 바꿔도 됨)
    try:
        import re
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F1E0-\U0001F1FF"  # flags
            "\U00002700-\U000027BF"  # dingbats
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U00002600-\U000026FF"  # Misc symbols
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub("", s)
    except Exception:
        return s  # 문제가 생기면 그냥 원문 반환

def build_pdf_bytes(name: str, comments: list[str]) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ✅ 유니코드 폰트 등록 + 설정
    if not FONT_PATH.exists():
        raise FileNotFoundError(f"한글 폰트 파일을 찾을 수 없습니다: {FONT_PATH}")

    pdf.add_font("NotoKR", "", str(FONT_PATH), uni=True)
    pdf.set_font("NotoKR", size=16)

    # 타이틀
    title = f"금연 상담 리포트 - {name}"
    pdf.cell(0, 10, txt=_strip_emoji(title), ln=True)

    pdf.ln(5)
    pdf.set_font("NotoKR", size=12)

    if comments:
        for c in comments:
            pdf.multi_cell(0, 8, txt=_strip_emoji(c))
    else:
        pdf.multi_cell(0, 8, txt="모든 항목이 평균 이상입니다.")

    # ✅ fpdf2 권장 방식: 문자열 반환 후 latin-1 인코딩
    # (내부는 바이너리 스트림이지만 fpdf2는 str을 리턴하므로 latin-1로 안전 인코딩)
    return pdf.output(dest="S").encode("latin-1")
