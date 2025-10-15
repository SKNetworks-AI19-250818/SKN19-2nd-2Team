# pages/01_환자_정보_입력.py
import datetime as dt
import streamlit as st
from utils.state import init_state, go, NAV_COUNSELOR

st.set_page_config(page_title="환자 정보 입력", layout="wide")
init_state()

# ✅ 세션의 date 값을 안전하게 정규화
def _normalize_date_key(key="date"):
    val = st.session_state.get(key, None)
    if val is None:
        st.session_state[key] = dt.date.today()
    elif isinstance(val, str):
        # 예전 코드에서 'today' 같은 문자열이 남아있는 경우 처리
        if val.lower() == "today":
            st.session_state[key] = dt.date.today()
        else:
            # ISO 문자열이면 파싱, 아니면 오늘로
            try:
                st.session_state[key] = dt.date.fromisoformat(val)
            except Exception:
                st.session_state[key] = dt.date.today()

_normalize_date_key("date")


# date 기본값 보정
if not isinstance(st.session_state.get("date"), (dt.date, str)) or st.session_state.get("date") == "":
    st.session_state["date"] = dt.date.today()

st.title("환자 정보 입력")

# -------------------------
# 옵션 & 인코딩 매핑 테이블
# -------------------------
MAP = {
    "성별": {"남자": 1, "여자": 0},
    "marital_stability": {
        "미혼": 0, "기혼-안정": 1, "기혼-불안": 2, "이혼/별거": 3, "사별": 4
    },
    "아침식사빈도": {
        "거의 안 함": 0, "주 1-2회": 1, "주 3-4회": 2, "주 5-6회": 3, "매일": 4
    },
    "weight_control_method": {
        "없음": 0, "운동": 1, "식이": 2, "운동+식이": 3, "약물/기타": 4
    },
    "화장실각성여부": {"아니오": 0, "예": 1},
    "평생 음주 여부": {"아니오": 0, "예": 1},
    "연간 음주 빈도": {
        "안 함": 0, "월 1회 미만": 1, "월 1-3회": 2, "주 1-2회": 3, "주 3-4회": 4, "거의 매일": 5
    },
    "가정내흡연자존재": {"아니오": 0, "예": 1},
    "치매검사여부": {"아니오": 0, "예": 1},
    "occupation_type": {
        "무직": 0, "학생": 1, "자영업": 2, "사무직": 3, "생산/서비스": 4, "전문직": 5, "기타": 6
    },
    "최근 1주일 유연성 운동 실천": {"안 함": 0, "1-2일": 1, "3-4일": 2, "5일 이상": 3},
    "구강건강자기평가": {"매우 나쁨": 1, "나쁨": 2, "보통": 3, "좋음": 4, "매우 좋음": 5},
    # 기존 단순 항목
    "아침식사여부": {"아니오": 0, "예": 1},
}

def enc(cat_name: str, value: str) -> int:
    return MAP[cat_name][value]

# -------------------------
# 입력 폼
# -------------------------
c1, c2, c3 = st.columns([1, 1, 1])
with c1:
    name = st.text_input("환자 이름", key="name")
    age = st.number_input("나이", min_value=0, max_value=120, value=40, step=1, key="age") # ← 모델 미사용, 헤더 노출용
    gender_raw = st.selectbox("성별", list(MAP["성별"].keys()), index=0, key="gender_raw")
    date = st.date_input("상담 날짜", key="date")

with c2:
    marital_raw = st.selectbox("혼인 안정성", list(MAP["marital_stability"].keys()), index=0, key="marital_raw")
    breakfast_freq_raw = st.selectbox("아침식사 빈도", list(MAP["아침식사빈도"].keys()), index=4, key="breakfast_freq_raw")
    wt_ctrl_raw = st.selectbox("체중 조절 방법", list(MAP["weight_control_method"].keys()), index=0, key="wt_ctrl_raw")
    toilet_awake_raw = st.selectbox("밤중 화장실 각성(야간뇨) 여부", list(MAP["화장실각성여부"].keys()), index=0, key="toilet_awake_raw")

with c3:
    lifetime_drink_raw = st.selectbox("평생 음주 여부", list(MAP["평생 음주 여부"].keys()), index=1, key="lifetime_drink_raw")
    year_freq_raw = st.selectbox("연간 음주 빈도", list(MAP["연간 음주 빈도"].keys()), index=2, key="year_freq_raw")
    per_occasion = st.slider("한 번 섭취 시 음주량(잔)", 0, 15, 3, key="per_occasion")
    home_smoker_raw = st.selectbox("가정 내 흡연자 존재", list(MAP["가정내흡연자존재"].keys()), index=0, key="home_smoker_raw")

c4, c5, c6 = st.columns([1, 1, 1])
with c4:
    dementia_raw = st.selectbox("치매검사여부", list(MAP["치매검사여부"].keys()), index=0, key="dementia_raw")
    # job_raw = st.selectbox("직업군", list(MAP["occupation_type"].keys()), index=3, key="job_raw") # 기존
    job_raw = st.selectbox("직업군", list(MAP["occupation_type"].keys()), index=3, key="job_raw")
    sleep_time_h = st.slider("취침 시간(시, 0~23)", 0, 23, 23, key="sleep_time_h")
    flex_ex_raw = st.selectbox("최근 1주일 유연성 운동 실천", list(MAP["최근 1주일 유연성 운동 실천"].keys()), index=1, key="flex_ex_raw")

with c5:
    oral_raw = st.selectbox("구강건강 자기평가", list(MAP["구강건강자기평가"].keys()), index=3, key="oral_raw")
    # sleep_hours = st.number_input("수면 시간(시간)", min_value=0.0, max_value=14.0, value=7.0, step=0.5, key="sleep")
    sleep_hours = st.number_input("수면 시간", value=7.0, key="sleep_input")
    stress = st.slider("스트레스 수준(1~5)", 1, 5, 3, key="stress")
    breakfast_yes_raw = st.selectbox("아침식사 여부", list(MAP["아침식사여부"].keys()), index=1, key="breakfast_yes_raw")

with c6:
    exercise = st.slider("운동 빈도(주당 횟수)", 0, 7, 3, key="exercise")
    weight = st.number_input("체중(kg)", min_value=0.0, max_value=300.0, value=70.0, step=0.1, key="weight")
    height = st.number_input("키(cm)", min_value=0.0, max_value=230.0, value=175.0, step=0.1, key="height")
    weekly_alcohol = st.number_input("주당 총 음주량(잔)", min_value=0, max_value=100, value=0, key="alcohol_week")

# BMI 계산
bmi = round((weight / ((height / 100) ** 2)) if height > 0 else 0, 1)
st.caption(f"BMI 자동계산: {bmi}")

st.write("---")
password = st.text_input("상담자 비밀번호", type="password", key="password")
DEFAULT_PASSWORD = "clinic123"

def try_login():
    if not name.strip():
        st.session_state["_login_error"] = "이름을 입력하세요."
        return
    if st.session_state.get("password") != DEFAULT_PASSWORD:
        st.session_state["_login_error"] = "비밀번호가 올바르지 않습니다."
        return

    # raw & enc 동시 저장 (모델 컬럼 매칭용)
    features_raw = {
        "성별": gender_raw,
        "marital_stability": marital_raw,
        "아침식사빈도": breakfast_freq_raw,
        "weight_control_method": wt_ctrl_raw,
        "화장실각성여부": toilet_awake_raw,
        "평생 음주 여부": lifetime_drink_raw,
        "연간 음주 빈도": year_freq_raw,
        "한 번 섭취 시 음주량": per_occasion,
        "가정내흡연자존재": home_smoker_raw,
        "치매검사여부": dementia_raw,
        "occupation_type": job_raw,
        "취침시간": sleep_time_h,
        "최근 1주일 유연성 운동 실천": flex_ex_raw,
        "구강건강자기평가": oral_raw,
        # 보조 지표
        "수면시간": float(sleep_hours),
        "스트레스": int(stress),
        "운동빈도": int(exercise),
        "아침식사여부": breakfast_yes_raw,
        "주당 총 음주량": int(weekly_alcohol),
        "BMI": float(bmi),
    }
    # 정수 인코딩
    features_enc = {
        "sex": enc("성별", gender_raw),
        "marital_stability": enc("marital_stability", marital_raw),
        "breakfast_freq": enc("아침식사빈도", breakfast_freq_raw),
        "weight_control_method": enc("weight_control_method", wt_ctrl_raw),
        "toilet_awake": enc("화장실각성여부", toilet_awake_raw),
        "ever_drink": enc("평생 음주 여부", lifetime_drink_raw),
        "year_drink_freq": enc("연간 음주 빈도", year_freq_raw),
        "drink_per_occasion": int(per_occasion),
        "home_smoker": enc("가정내흡연자존재", home_smoker_raw),
        "dementia_test": enc("치매검사여부", dementia_raw),
        "occupation_type": enc("occupation_type", job_raw),
        "sleep_time_hour": int(sleep_time_h),
        "flex_ex_week": enc("최근 1주일 유연성 운동 실천", flex_ex_raw),
        "oral_health_self": enc("구강건강자기평가", oral_raw),
        # 보조 지표
        "sleep_hours": float(sleep_hours),
        "stress_score": int(stress),
        "exercise_per_week": int(exercise),
        "breakfast_yes": enc("아침식사여부", breakfast_yes_raw),
        "alcohol_weekly": int(weekly_alcohol),
        "bmi": float(bmi),
    }

    # 세션 저장: 환자(헤더용), 피처(raw/enc)
    st.session_state["patient"] = {
        "이름": name,
        "나이": int(age),            # ← 모델 미사용, 헤더 노출용
        "성별": gender_raw,
        "날짜": str(date),
        "BMI": float(bmi),
    }
    st.session_state["features_raw"] = features_raw
    st.session_state["features_enc"] = features_enc
    st.session_state["_login_error"] = ""
    go(NAV_COUNSELOR)

st.button("상담자 전용 화면으로 이동", on_click=try_login)

if st.session_state.get("_login_error"):
    st.error(st.session_state["_login_error"])


# st.set_page_config(page_title="환자 정보 입력", layout="wide")
# init_state()

# # 날짜 세션 값 보정
# if not isinstance(st.session_state.get("date"), (dt.date, str)) or st.session_state.get("date") == "":
#     st.session_state["date"] = "today"

# st.title("환자 정보 입력")

# # 입력 폼 (3열)
# col1, col2, col3 = st.columns([1, 1, 1])

# with col1:
#     st.text_input("환자 이름", key="name")
#     st.selectbox("성별", ["남자", "여자"], key="gender")
#     st.date_input("상담 날짜", key="date")

# with col2:
#     st.number_input("수면 시간 (시간)", min_value=0, max_value=12, value=7, key="sleep")
#     st.selectbox("아침식사 여부", ["예", "아니오"], key="breakfast")
#     st.slider("운동 빈도 (주당 횟수)", min_value=0, max_value=7, value=3, key="exercise")

# with col3:
#     st.slider("스트레스 수준 (1~5)", min_value=1, max_value=5, value=3, key="stress")
#     st.number_input("체중 (kg)", min_value=0.0, max_value=300.0, value=70.0, step=0.1, key="weight")
#     st.number_input("키 (cm)", min_value=0.0, max_value=230.0, value=175.0, step=0.1, key="height")

# st.number_input("음주량 (주당 잔 수)", min_value=0, max_value=50, value=0, key="alcohol")

# st.write("---")
# st.text_input("상담자 비밀번호", type="password", key="password")

# DEFAULT_PASSWORD = "clinic123"

# def try_login():
#     name = st.session_state.get("name", "").strip()
#     if not name:
#         st.session_state["_login_error"] = "이름을 입력해주세요."
#         return
#     if st.session_state.get("password") != DEFAULT_PASSWORD:
#         st.session_state["_login_error"] = "비밀번호가 올바르지 않습니다."
#         return

#     st.session_state["patient"] = {
#         "이름": name,
#         "성별": st.session_state.get("gender", "남자"),
#         "날짜": str(st.session_state.get("date", "")),
#         "수면시간": st.session_state.get("sleep", 7),
#         "아침식사": 1 if st.session_state.get("breakfast", "예") == "예" else 0,
#         "운동빈도": st.session_state.get("exercise", 3),
#         "스트레스": st.session_state.get("stress", 3),
#         "체중": float(st.session_state.get("weight", 70.0)),
#         "키": float(st.session_state.get("height", 175.0)),
#         "음주량": int(st.session_state.get("alcohol", 0)),
#     }
#     st.session_state["_login_error"] = ""
#     st.session_state["_pdf_bytes"] = None
#     go(NAV_COUNSELOR)

# st.button("상담자 전용 화면으로 이동", on_click=try_login)

# if st.session_state.get("_login_error"):
#     st.error(st.session_state["_login_error"])
#=========================

# # pages/01_환자_정보_입력.py
# import datetime as dt
# import streamlit as st
# from utils.state import init_state, go, NAV_COUNSELOR

# st.set_page_config(page_title="환자 정보 입력", layout="wide")
# init_state()

# # ✅ date 세션 값이 비정상일 경우 바로 교정
# if not isinstance(st.session_state.get("date"), (dt.date, str)) or st.session_state.get("date") == "":
#     st.session_state["date"] = "today"

# st.title("환자 정보 입력")

# # ------------------------
# # 입력 폼 (토스풍: 간격 넓게, 3열)
# # ------------------------
# col1, col2, col3 = st.columns([1, 1, 1])

# with col1:
#     st.text_input("환자 이름", key="name")
#     st.selectbox("성별", ["남자", "여자"], key="gender")
#     st.date_input("상담 날짜", key="date")

# with col2:
#     st.number_input("수면 시간 (시간)", min_value=0, max_value=12, value=7, key="sleep")
#     st.selectbox("아침식사 여부", ["예", "아니오"], key="breakfast")
#     st.slider("운동 빈도 (주당 횟수)", min_value=0, max_value=7, value=3, key="exercise")

# with col3:
#     st.slider("스트레스 수준 (1~5)", min_value=1, max_value=5, value=3, key="stress")
#     st.number_input("체중 (kg)", min_value=0.0, max_value=300.0, value=70.0, step=0.1, key="weight")
#     st.number_input("키 (cm)", min_value=0.0, max_value=230.0, value=175.0, step=0.1, key="height")

# st.number_input("음주량 (주당 잔 수 등 단위 자유)", min_value=0, max_value=50, value=0, key="alcohol")

# st.write("---")
# st.text_input("상담자 비밀번호", type="password", key="password")

# DEFAULT_PASSWORD = "clinic123"

# def try_login():
#     name = st.session_state.get("name", "").strip()
#     if not name:
#         st.session_state["_login_error"] = "이름을 입력해주세요."
#         return
#     if st.session_state.get("password") != DEFAULT_PASSWORD:
#         st.session_state["_login_error"] = "비밀번호가 올바르지 않습니다."
#         return

#     # 저장: 상담자 전용 페이지에서 BMI 계산/표시
#     st.session_state["patient"] = {
#         "이름": name,
#         "성별": st.session_state.get("gender", "남자"),
#         "날짜": str(st.session_state.get("date", "")),
#         "수면시간": st.session_state.get("sleep", 7),
#         "아침식사": 1 if st.session_state.get("breakfast", "예") == "예" else 0,
#         "운동빈도": st.session_state.get("exercise", 3),
#         "스트레스": st.session_state.get("stress", 3),
#         "체중": float(st.session_state.get("weight", 70.0)),
#         "키": float(st.session_state.get("height", 175.0)),
#         "음주량": int(st.session_state.get("alcohol", 0)),
#     }
#     st.session_state["_login_error"] = ""
#     st.session_state["_pdf_bytes"] = None
#     go(NAV_COUNSELOR)

# st.button("상담자 전용 화면으로 이동", on_click=try_login)

# if st.session_state.get("_login_error"):
#     st.error(st.session_state["_login_error"])
