import streamlit as st
from utils.state import init_state

st.set_page_config(page_title="설정/도움말", page_icon="⚙️", layout="wide")
init_state()

st.title("⚙️ 설정 및 도움말")
st.markdown("""
- **첫 화면은 항상 '홈'**으로 시작합니다.
- 위젯 키와 `st.session_state` 키를 **동일 이름으로 직접 수정하지 마세요.**(콜백에서 변경)
- PDF 한글 폰트를 쓰려면 프로젝트 루트에 `NotoSansKR-Regular.ttf`를 넣으세요.
""")
