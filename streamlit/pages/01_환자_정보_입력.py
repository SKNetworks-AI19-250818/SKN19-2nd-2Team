# pages/01_환자_정보_입력.py
import datetime as dt
import streamlit as st
from utils.state import init_state, go, NAV_COUNSELOR

st.set_page_config(page_title="환자 정보 입력", layout="wide")
init_state()

# ✅ date 세션 값이 비정상일 경우 바로 교정
if not isinstance(st.session_state.get("date"), (dt.date, str)) or st.session_state.get("date") == "":
    st.session_state["date"] = "today"

st.title("환자 정보 입력")

# ------------------------
# 입력 폼 (토스풍: 간격 넓게, 3열)
# ------------------------
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    st.text_input("환자 이름", key="name")
    st.selectbox("성별", ["남자", "여자"], key="gender")
    st.date_input("상담 날짜", key="date")

with col2:
    st.number_input("수면 시간 (시간)", min_value=0, max_value=12, value=7, key="sleep")
    st.selectbox("아침식사 여부", ["예", "아니오"], key="breakfast")
    st.slider("운동 빈도 (주당 횟수)", min_value=0, max_value=7, value=3, key="exercise")

with col3:
    st.slider("스트레스 수준 (1~5)", min_value=1, max_value=5, value=3, key="stress")
    st.number_input("체중 (kg)", min_value=0.0, max_value=300.0, value=70.0, step=0.1, key="weight")
    st.number_input("키 (cm)", min_value=0.0, max_value=230.0, value=175.0, step=0.1, key="height")

st.number_input("음주량 (주당 잔 수 등 단위 자유)", min_value=0, max_value=50, value=0, key="alcohol")

st.write("---")
st.text_input("상담자 비밀번호", type="password", key="password")

DEFAULT_PASSWORD = "clinic123"

def try_login():
    name = st.session_state.get("name", "").strip()
    if not name:
        st.session_state["_login_error"] = "이름을 입력해주세요."
        return
    if st.session_state.get("password") != DEFAULT_PASSWORD:
        st.session_state["_login_error"] = "비밀번호가 올바르지 않습니다."
        return

    # 저장: 상담자 전용 페이지에서 BMI 계산/표시
    st.session_state["patient"] = {
        "이름": name,
        "성별": st.session_state.get("gender", "남자"),
        "날짜": str(st.session_state.get("date", "")),
        "수면시간": st.session_state.get("sleep", 7),
        "아침식사": 1 if st.session_state.get("breakfast", "예") == "예" else 0,
        "운동빈도": st.session_state.get("exercise", 3),
        "스트레스": st.session_state.get("stress", 3),
        "체중": float(st.session_state.get("weight", 70.0)),
        "키": float(st.session_state.get("height", 175.0)),
        "음주량": int(st.session_state.get("alcohol", 0)),
    }
    st.session_state["_login_error"] = ""
    st.session_state["_pdf_bytes"] = None
    go(NAV_COUNSELOR)

st.button("상담자 전용 화면으로 이동", on_click=try_login)

if st.session_state.get("_login_error"):
    st.error(st.session_state["_login_error"])
