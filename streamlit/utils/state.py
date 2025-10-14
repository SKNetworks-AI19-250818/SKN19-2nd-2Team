import streamlit as st

NAV_HOME = "홈"
NAV_INPUT = "환자 정보 입력"
NAV_COUNSELOR = "상담자 전용"

DEFAULTS = {
    "nav": NAV_HOME,
    "patient": None,
    "_pdf_bytes": None,
    "_login_error": "",
    # 입력값
    "name": "",
    "gender": "남자",
    "date": "today",      # ✅ 빈 문자열 대신 today 또는 date.today() 사용 가능
    "sleep": 7,
    "breakfast": "예",
    "exercise": 3,
    "stress": 3,
    "weight": 70.0,
    "height": 175.0,
    "alcohol": 0,
    "password": "",
}

def init_state():
    for k, v in DEFAULTS.items():
        st.session_state.setdefault(k, v)

def go(to: str):
    st.session_state["nav"] = to
