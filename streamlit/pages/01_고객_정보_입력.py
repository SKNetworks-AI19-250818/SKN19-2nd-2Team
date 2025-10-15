# pages/01_환자_정보_입력.py
import datetime as dt
import streamlit as st

st.set_page_config(page_title="환자 정보 입력", layout="wide")

def _normalize_date_key(key="date"):
    val = st.session_state.get(key)
    if val is None:
        st.session_state[key] = dt.date.today()
    elif isinstance(val, str):
        st.session_state[key] = dt.date.today() if val.lower()=="today" else \
            (dt.date.fromisoformat(val) if "-" in val else dt.date.today())
_normalize_date_key("date")

MAP = {
    "성별": {"남자": 1, "여자": 2},
    "marital_stability": {
        "미혼": 0, "기혼-안정": 1, "기혼-불안": 2, "이혼/별거": 3, "사별": 4
    },
    "아침식사빈도": {
        "주 5~7회": 1, "주 3~4회": 2, "주 1~2회": 3, "거의 안 함": 4
    },
    "weight_control_method": {
        "없음": 0, "운동": 1, "식이": 2, "운동+식이": 3, "약물/기타": 4
    },
    "화장실각성여부": {"아니오": 1, "예": 3},
    "평생 음주 여부": {"아니오": 2, "예": 1},
    "연간 음주 빈도": {
        "안 함": 0, "월 1회 미만": 1, "월 1-3회": 2, "주 1-2회": 3, "주 3-4회": 4, "거의 매일": 5
    },
    "가정내흡연자존재": {"아니오": 2, "예": 1},
    "치매검사여부": {"아니오": 2, "예": 1},
    "occupation_type": {
        "무직": 0, "학생": 1, "자영업": 2, "사무직": 3, "생산/서비스": 4, "전문직": 5, "기타": 6
    },
    "최근 1주일 유연성 운동 실천": {"안 함": 0, "1-2일": 1, "3-4일": 2, "5일 이상": 3},
    "구강건강자기평가": {"매우 나쁨": 1, "나쁨": 2, "보통": 3, "좋음": 4, "매우 좋음": 5}
    # 기존 단순 항목
    # "아침식사여부": {"아니오": 0, "예": 1},
}

# MAP = {
#     "성별": {"남자": 1, "여자": 0},
#     "marital_stability": {"미혼": 0, "기혼-안정": 1, "기혼-불안": 2, "이혼/별거": 3, "사별": 4},
#     "아침식사빈도": {"거의 안 함": 0, "주 1-2회": 1, "주 3-4회": 2, "주 5-6회": 3, "매일": 4},
#     "weight_control_method": {"없음": 0, "운동": 1, "식이": 2, "운동+식이": 3, "약물/기타": 4},
#     "화장실각성여부": {"아니오": 0, "예": 1},
#     "평생 음주 여부": {"아니오": 0, "예": 1},
#     "연간 음주 빈도": {"안 함": 0, "월 1회 미만": 1, "월 1-3회": 2, "주 1-2회": 3, "주 3-4회": 4, "거의 매일": 5},
#     "가정내흡연자존재": {"아니오": 0, "예": 1},
#     "치매검사여부": {"아니오": 0, "예": 1},
#     "occupation_type": {"무직": 0, "학생": 1, "자영업": 2, "사무직": 3, "생산/서비스": 4, "전문직": 5, "기타": 6},
#     "최근 1주일 유연성 운동 실천": {"안 함": 0, "1-2일": 1, "3-4일": 2, "5일 이상": 3},
#     "구강건강자기평가": {"매우 나쁨": 1, "나쁨": 2, "보통": 3, "좋음": 4, "매우 좋음": 5}
#     # "아침식사여부": {"아니오": 0, "예": 1},
# }
def enc(cat, val): return MAP[cat][val]

ctprvn_dict = {
    11: "서울",
    26: "부산",
    27: "대구",
    28: "인천",
    29: "광주",
    30: "대전",
    31: "울산",
    36: "세종",
    41: "경기",
    42: "강원",
    43: "충북",
    44: "충남",
    45: "전북",
    46: "전남",
    47: "경북",
    48: "경남",
    50: "제주"
}

with st.expander("필수 입력 항목", expanded=True):
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        name = st.text_input("환자 이름", key="name")
        age = st.number_input("나이", min_value=0, max_value=120, value=40, step=1, key="age")
        gender_raw = st.selectbox("성별", list(MAP["성별"].keys()), index=0, key="gender_raw")
        date = st.date_input("상담 날짜", key="date")
        ctprvn_name = st.selectbox("거주지역을 선택하세요", options=list(ctprvn_dict.values()))
        ctprvn_code = [k for k, v in ctprvn_dict.items() if v == ctprvn_name][0]

    with c2:
        breakfast_freq_raw = st.selectbox("아침식사 빈도", list(MAP["아침식사빈도"].keys()), index=0, key="breakfast_freq_raw")
        year_freq_raw = st.selectbox("연간 음주 빈도", list(MAP["연간 음주 빈도"].keys()), index=2, key="year_freq_raw")
        is_economically_active = st.selectbox("경제활동 여부", options=["경제활동 중", "비경제활동"])
        is_economically_active_code = {"경제활동 중": 1, "비경제활동": 0}[is_economically_active]
        activity_display = st.selectbox("신체활동 수준을 선택하세요", options=["활동량이 많음", "보통", "적음", "없음"])
        activity_score = {"활동량이 많음": "high_activity", "보통": "normal_activity", "적음": "low_activity", "없음": "no_activity"}[activity_display]
        oral_raw = st.selectbox("구강건강 자기평가", list(MAP["구강건강자기평가"].keys()), index=3, key="oral_raw")

    with c3:
        lifetime_drink_raw = st.selectbox("평생 음주 여부", list(MAP["평생 음주 여부"].keys()), index=1, key="lifetime_drink_raw")
        per_occasion = st.slider("한 번 섭취 시 음주량(잔)", 0, 15, 3, key="per_occasion")
        flex_ex_raw = st.selectbox("최근 1주일 유연성 운동 실천", list(MAP["최근 1주일 유연성 운동 실천"].keys()), index=1, key="flex_ex_raw")
        stress = st.slider("스트레스 수준(1~5)", 1, 5, 3, key="stress")
        home_smoker_raw = st.selectbox("가정 내 흡연자 존재", list(MAP["가정내흡연자존재"].keys()), index=0, key="home_smoker_raw")
        work_smoker = st.selectbox("직장 간접흡연 노출 여부", options=["예", "아니오", "직장 없음"])
        work_smoker_raw = {"예": 1, "아니오": 2, "직장 없음": 3}[work_smoker]

with st.expander("추가 입력 항목", expanded=False):
    c4, c5, c6 = st.columns([1, 1, 1])
    with c4:
        dementia_raw = st.selectbox("치매검사여부", list(MAP["치매검사여부"].keys()), index=0, key="dementia_raw")
        # job_raw = st.selectbox("직업군", list(MAP["occupation_type"].keys()), index=3, key="job_raw") # 기존
        job_raw = st.selectbox("직업군", list(MAP["occupation_type"].keys()), index=3, key="job_raw")
        sleep_time_h = st.slider("취침 시간(시, 0~23)", 0, 23, 23, key="sleep_time_h")

    
    with c5:
        # sleep_hours = st.number_input("수면 시간(시간)", min_value=0.0, max_value=14.0, value=7.0, step=0.5, key="sleep")
        toilet_awake_raw = st.selectbox("밤중 화장실 각성(야간뇨) 여부", list(MAP["화장실각성여부"].keys()), index=0, key="toilet_awake_raw")
        # sleep_hours = st.number_input("수면 시간", value=7.0, key="sleep_input")
        # breakfast_yes_raw = st.selectbox("아침식사 여부", list(MAP["아침식사여부"].keys()), index=1, key="breakfast_yes_raw")
        wt_ctrl_raw = st.selectbox("체중 조절 방법", list(MAP["weight_control_method"].keys()), index=0, key="wt_ctrl_raw")

    with c6:
        # exercise = st.slider("운동 빈도(주당 횟수)", 0, 7, 3, key="exercise")
        weight = st.number_input("체중(kg)", min_value=0.0, max_value=300.0, value=70.0, step=0.1, key="weight")
        height = st.number_input("키(cm)", min_value=0.0, max_value=230.0, value=175.0, step=0.1, key="height")
        # weekly_alcohol = st.number_input("주당 총 음주량(잔)", min_value=0, max_value=100, value=0, key="alcohol_week")
        marital_raw = st.selectbox("혼인 안정성", list(MAP["marital_stability"].keys()), index=0, key="marital_raw")

# BMI
h, w = float(st.session_state["height"]), float(st.session_state["weight"])
bmi = round((w / ((h/100)**2)) if h > 0 else 0, 1)
st.caption(f"BMI 자동계산: {bmi}")

st.write("---")
st.text_input("상담자 비밀번호", type="password", key="password")
DEFAULT_PASSWORD = "clinic123"

def try_login():
    name = (st.session_state.get("name") or "").strip()
    if not name:
        st.session_state["_login_error"] = "이름을 입력하세요."
        return
    if st.session_state.get("password") != DEFAULT_PASSWORD:
        st.session_state["_login_error"] = "비밀번호가 올바르지 않습니다."
        return

    # features_raw = {
    #     "성별": st.session_state["gender_raw"],
    #     "marital_stability": st.session_state["marital_raw"],
    #     "아침식사빈도": st.session_state["breakfast_freq_raw"],
    #     "weight_control_method": st.session_state["wt_ctrl_raw"],
    #     "화장실각성여부": st.session_state["toilet_awake_raw"],
    #     "평생 음주 여부": st.session_state["lifetime_drink_raw"],
    #     "연간 음주 빈도": st.session_state["year_freq_raw"],
    #     "한 번 섭취 시 음주량": int(st.session_state["per_occasion"]),
    #     "가정내흡연자존재": st.session_state["home_smoker_raw"],
    #     "치매검사여부": st.session_state["dementia_raw"],
    #     "occupation_type": st.session_state["job_raw"],
    #     "취침시간": int(st.session_state["sleep_time_h"]),
    #     "최근 1주일 유연성 운동 실천": st.session_state["flex_ex_raw"],
    #     "구강건강자기평가": st.session_state["oral_raw"],
    #     "수면시간": float(st.session_state["sleep_input"]),
    #     "스트레스": int(st.session_state["stress"]),
    #     "운동빈도": int(st.session_state["exercise"]),
    #     "아침식사여부": st.session_state["breakfast_yes_raw"],
    #     "주당 총 음주량": int(st.session_state["alcohol_week"]),
    #     "BMI": float(bmi),
    # }
    # features_enc = {
    #     "sex": MAP["성별"][st.session_state["gender_raw"]],
    #     "marital_stability": MAP["marital_stability"][st.session_state["marital_raw"]],
    #     "breakfast_freq": MAP["아침식사빈도"][st.session_state["breakfast_freq_raw"]],
    #     "weight_control_method": MAP["weight_control_method"][st.session_state["wt_ctrl_raw"]],
    #     "toilet_awake": MAP["화장실각성여부"][st.session_state["toilet_awake_raw"]],
    #     "ever_drink": MAP["평생 음주 여부"][st.session_state["lifetime_drink_raw"]],
    #     "year_drink_freq": MAP["연간 음주 빈도"][st.session_state["year_freq_raw"]],
    #     "drink_per_occasion": int(st.session_state["per_occasion"]),
    #     "home_smoker": MAP["가정내흡연자존재"][st.session_state["home_smoker_raw"]],
    #     "dementia_test": MAP["치매검사여부"][st.session_state["dementia_raw"]],
    #     "occupation_type": MAP["occupation_type"][st.session_state["job_raw"]],
    #     "sleep_time_hour": int(st.session_state["sleep_time_h"]),
    #     "flex_ex_week": MAP["최근 1주일 유연성 운동 실천"][st.session_state["flex_ex_raw"]],
    #     "oral_health_self": MAP["구강건강자기평가"][st.session_state["oral_raw"]],
    #     "sleep_hours": float(st.session_state["sleep_input"]),
    #     "stress_score": int(st.session_state["stress"]),
    #     "exercise_per_week": int(st.session_state["exercise"]),
    #     "breakfast_yes": MAP["아침식사여부"][st.session_state["breakfast_yes_raw"]],
    #     "alcohol_weekly": int(st.session_state["alcohol_week"]),
    #     "bmi": float(bmi),
    # }

    # raw & enc 동시 저장 (모델 컬럼 매칭용)
    features_raw = {
        #필수입력
        "성별": gender_raw,
        "시도번호": ctprvn_code,
        "아침식사빈도": breakfast_freq_raw,
        "연간 음주 빈도": year_freq_raw,
        "한 번 섭취 시 음주량": per_occasion,
        "최근 1주일 유연성 운동 실천": flex_ex_raw,
        "스트레스": int(stress),
        "가정내흡연자존재": home_smoker_raw,
        "직장간접흡연노출": work_smoker_raw,
        "age_group": age,
        "is_economically_active": is_economically_active_code,
        "weight_control_method": wt_ctrl_raw,
        "activity_score": activity_score,
        "구강건강자기평가": oral_raw,

        #선택입력
        # "수면시간": float(sleep_hours),
        #가구원수_전체
        #기초생활수급자여부
        #가구식품안정성여부
        # "아침식사여부": breakfast_yes_raw,
        #영양표시설인지여부
        #영향표시영향여부
        #저작불편여부
        #저녁양치여부
        "평생 음주 여부": lifetime_drink_raw,
        #절주 또는 금주계획 여부
        #스트레스상담여부        
        "취침시간": sleep_time_h,
        #기상시간
        "화장실각성여부": toilet_awake_raw,
        #악몽경험여부
        #기억력저하여부
        #상담여부
        "치매검사여부": dementia_raw,
        #졸업상태
        #is_single
        #house_income_grp
        #fma_dementia_case
        #education_group
        "occupation_type": job_raw,
        #is_employee
        #activity_score_weight
        "marital_stability": marital_raw,
        
        #보조지표
        # "운동빈도": int(exercise),        
        # "주당 총 음주량": int(weekly_alcohol),
        "BMI": float(bmi),
    }
    # 정수 인코딩
    features_enc = {
        "age_group": int(age)//10*10,
        "성별": enc("성별", gender_raw),
        "marital_stability": enc("marital_stability", marital_raw),
        "아침식사빈도": enc("아침식사빈도", breakfast_freq_raw),
        "weight_control_method": enc("weight_control_method", wt_ctrl_raw),
        "화장실각성여부": enc("화장실각성여부", toilet_awake_raw),
        "평생 음주 여부": enc("평생 음주 여부", lifetime_drink_raw),
        "연간 음주 빈도": enc("연간 음주 빈도", year_freq_raw),
        "한 번 섭취 시 음주량": int(per_occasion),
        "가정내흡연자존재": enc("가정내흡연자존재", home_smoker_raw),
        "치매검사여부": enc("치매검사여부", dementia_raw),
        "occupation_type": enc("occupation_type", job_raw),
        #"sleep_time_hour": int(sleep_time_h),
        "최근 1주일 유연성 운동 실천": enc("최근 1주일 유연성 운동 실천", flex_ex_raw),
        "구강건강자기평가": enc("구강건강자기평가", oral_raw),
        "bmi": float(bmi),
        "스트레스": int(stress),
        "시도번호": int(ctprvn_code),
        "직장간접흡연노출": int(work_smoker_raw),
        "activity_score": activity_score,
        "is_economically_active": int(is_economically_active_code),
    }

    # 세션 저장: 환자(헤더용), 피처(raw/enc)
    st.session_state["patient"] = {
        "이름": name,
        "나이": int(age),           
        "성별": gender_raw,
        "날짜": str(date),
        "BMI": float(bmi),
    }
    st.session_state["patient"] = {
        "이름": name,
        "나이": int(st.session_state.get("age", 0)),
        "성별": st.session_state["gender_raw"],
        "날짜": str(st.session_state.get("date")),
        "BMI": float(bmi),
    }
    st.session_state["features_raw"] = features_raw
    st.session_state["features_enc"] = features_enc
    st.session_state["_login_error"] = ""

    # ❌ 기존 코드: callback 내에서 st.switch_page() 호출 시 작동 안 함
    # st.switch_page("pages/02_상담자_전용.py")
    
    # ✅ 수정된 코드: callback에서는 flag만 설정, 페이지 전환은 밖에서 처리
    st.session_state["_should_switch_page"] = True

st.button("상담자 전용 화면으로 이동", on_click=try_login)

if st.session_state.get("_login_error"):
    st.error(st.session_state["_login_error"])

# ✅ 새로 추가된 코드: callback 밖에서 페이지 전환 처리
if st.session_state.get("_should_switch_page"):
    st.session_state["_should_switch_page"] = False  # flag 초기화
    st.switch_page("pages/02_상담자_전용.py")


# # pages/01_환자_정보_입력.py
# import datetime as dt
# import streamlit as st
# from utils.state import init_state  # go는 안 씀: switch_page로 이동

# st.set_page_config(page_title="환자 정보 입력", layout="wide")
# init_state()

# # ---------- 날짜 키 정규화 ----------
# def _normalize_date_key(key="date"):
#     val = st.session_state.get(key, None)
#     if val is None:
#         st.session_state[key] = dt.date.today()
#     elif isinstance(val, str):
#         if val.lower() == "today":
#             st.session_state[key] = dt.date.today()
#         else:
#             try:
#                 st.session_state[key] = dt.date.fromisoformat(val)
#             except Exception:
#                 st.session_state[key] = dt.date.today()
# _normalize_date_key("date")

# # ---------- 매핑/인코딩 ----------
# MAP = {
#     "성별": {"남자": 1, "여자": 0},
#     "marital_stability": {"미혼": 0, "기혼-안정": 1, "기혼-불안": 2, "이혼/별거": 3, "사별": 4},
#     "아침식사빈도": {"거의 안 함": 0, "주 1-2회": 1, "주 3-4회": 2, "주 5-6회": 3, "매일": 4},
#     "weight_control_method": {"없음": 0, "운동": 1, "식이": 2, "운동+식이": 3, "약물/기타": 4},
#     "화장실각성여부": {"아니오": 0, "예": 1},
#     "평생 음주 여부": {"아니오": 0, "예": 1},
#     "연간 음주 빈도": {"안 함": 0, "월 1회 미만": 1, "월 1-3회": 2, "주 1-2회": 3, "주 3-4회": 4, "거의 매일": 5},
#     "가정내흡연자존재": {"아니오": 0, "예": 1},
#     "치매검사여부": {"아니오": 0, "예": 1},
#     "occupation_type": {"무직": 0, "학생": 1, "자영업": 2, "사무직": 3, "생산/서비스": 4, "전문직": 5, "기타": 6},
#     "최근 1주일 유연성 운동 실천": {"안 함": 0, "1-2일": 1, "3-4일": 2, "5일 이상": 3},
#     "구강건강자기평가": {"매우 나쁨": 1, "나쁨": 2, "보통": 3, "좋음": 4, "매우 좋음": 5},
#     "아침식사여부": {"아니오": 0, "예": 1},
# }
# def enc(cat_name: str, value: str) -> int:
#     return MAP[cat_name][value]

# st.title("환자 정보 입력")

# # ---------- 입력 폼 ----------
# c1, c2, c3 = st.columns(3)
# with c1:
#     st.text_input("환자 이름", key="name")
#     st.number_input("나이", 0, 120, 40, 1, key="age")  # 모델 미사용, 표시용
#     st.selectbox("성별", list(MAP["성별"].keys()), index=0, key="gender_raw")
#     st.date_input("상담 날짜", key="date")

# with c2:
#     st.selectbox("혼인 안정성", list(MAP["marital_stability"].keys()), index=0, key="marital_raw")
#     st.selectbox("아침식사 빈도", list(MAP["아침식사빈도"].keys()), index=4, key="breakfast_freq_raw")
#     st.selectbox("체중 조절 방법", list(MAP["weight_control_method"].keys()), index=0, key="wt_ctrl_raw")
#     st.selectbox("밤중 화장실 각성(야간뇨) 여부", list(MAP["화장실각성여부"].keys()), index=0, key="toilet_awake_raw")

# with c3:
#     st.selectbox("평생 음주 여부", list(MAP["평생 음주 여부"].keys()), index=1, key="lifetime_drink_raw")
#     st.selectbox("연간 음주 빈도", list(MAP["연간 음주 빈도"].keys()), index=2, key="year_freq_raw")
#     st.slider("한 번 섭취 시 음주량(잔)", 0, 15, 3, key="per_occasion")
#     st.selectbox("가정 내 흡연자 존재", list(MAP["가정내흡연자존재"].keys()), index=0, key="home_smoker_raw")

# c4, c5, c6 = st.columns(3)
# with c4:
#     st.selectbox("치매검사여부", list(MAP["치매검사여부"].keys()), index=0, key="dementia_raw")
#     st.selectbox("직업군", list(MAP["occupation_type"].keys()), index=3, key="job_raw")
#     st.slider("취침 시간(시, 0~23)", 0, 23, 23, key="sleep_time_h")
#     st.selectbox("최근 1주일 유연성 운동 실천", list(MAP["최근 1주일 유연성 운동 실천"].keys()), index=1, key="flex_ex_raw")

# with c5:
#     st.selectbox("구강건강 자기평가", list(MAP["구강건강자기평가"].keys()), index=3, key="oral_raw")
#     st.number_input("수면 시간(시간)", 0.0, 14.0, 7.0, 0.5, key="sleep_input")
#     st.slider("스트레스 수준(1~5)", 1, 5, 3, key="stress")
#     st.selectbox("아침식사 여부", list(MAP["아침식사여부"].keys()), index=1, key="breakfast_yes_raw")

# with c6:
#     st.slider("운동 빈도(주당 횟수)", 0, 7, 3, key="exercise")
#     st.number_input("체중(kg)", 0.0, 300.0, 70.0, 0.1, key="weight")
#     st.number_input("키(cm)", 0.0, 230.0, 175.0, 0.1, key="height")
#     st.number_input("주당 총 음주량(잔)", 0, 100, 0, key="alcohol_week")

# # BMI
# height = float(st.session_state.get("height", 0))
# weight = float(st.session_state.get("weight", 0))
# bmi = round((weight / ((height / 100) ** 2)) if height > 0 else 0, 1)
# st.caption(f"BMI 자동계산: {bmi}")

# st.write("---")
# st.text_input("상담자 비밀번호", type="password", key="password")
# DEFAULT_PASSWORD = "clinic123"

# # ---------- 단일 try_login ----------
# def try_login():
#     name = (st.session_state.get("name") or "").strip()
#     if not name:
#         st.session_state["_login_error"] = "이름을 입력하세요."
#         return
#     if st.session_state.get("password") != DEFAULT_PASSWORD:
#         st.session_state["_login_error"] = "비밀번호가 올바르지 않습니다."
#         return

#     # 세션에서 바로 읽어 안전하게 dict 구성
#     features_raw = {
#         "성별": st.session_state["gender_raw"],
#         "marital_stability": st.session_state["marital_raw"],
#         "아침식사빈도": st.session_state["breakfast_freq_raw"],
#         "weight_control_method": st.session_state["wt_ctrl_raw"],
#         "화장실각성여부": st.session_state["toilet_awake_raw"],
#         "평생 음주 여부": st.session_state["lifetime_drink_raw"],
#         "연간 음주 빈도": st.session_state["year_freq_raw"],
#         "한 번 섭취 시 음주량": int(st.session_state["per_occasion"]),
#         "가정내흡연자존재": st.session_state["home_smoker_raw"],
#         "치매검사여부": st.session_state["dementia_raw"],
#         "occupation_type": st.session_state["job_raw"],
#         "취침시간": int(st.session_state["sleep_time_h"]),
#         "최근 1주일 유연성 운동 실천": st.session_state["flex_ex_raw"],
#         "구강건강자기평가": st.session_state["oral_raw"],
#         # 표시/보조
#         "수면시간": float(st.session_state["sleep_input"]),
#         "스트레스": int(st.session_state["stress"]),
#         "운동빈도": int(st.session_state["exercise"]),
#         "아침식사여부": st.session_state["breakfast_yes_raw"],
#         "주당 총 음주량": int(st.session_state["alcohol_week"]),
#         "BMI": float(bmi),
#     }

#     features_enc = {
#         "sex": enc("성별", st.session_state["gender_raw"]),
#         "marital_stability": enc("marital_stability", st.session_state["marital_raw"]),
#         "breakfast_freq": enc("아침식사빈도", st.session_state["breakfast_freq_raw"]),
#         "weight_control_method": enc("weight_control_method", st.session_state["wt_ctrl_raw"]),
#         "toilet_awake": enc("화장실각성여부", st.session_state["toilet_awake_raw"]),
#         "ever_drink": enc("평생 음주 여부", st.session_state["lifetime_drink_raw"]),
#         "year_drink_freq": enc("연간 음주 빈도", st.session_state["year_freq_raw"]),
#         "drink_per_occasion": int(st.session_state["per_occasion"]),
#         "home_smoker": enc("가정내흡연자존재", st.session_state["home_smoker_raw"]),
#         "dementia_test": enc("치매검사여부", st.session_state["dementia_raw"]),
#         "occupation_type": enc("occupation_type", st.session_state["job_raw"]),
#         "sleep_time_hour": int(st.session_state["sleep_time_h"]),
#         "flex_ex_week": enc("최근 1주일 유연성 운동 실천", st.session_state["flex_ex_raw"]),
#         "oral_health_self": enc("구강건강자기평가", st.session_state["oral_raw"]),
#         # 보조(모델에 없으면 무시)
#         "sleep_hours": float(st.session_state["sleep_input"]),
#         "stress_score": int(st.session_state["stress"]),
#         "exercise_per_week": int(st.session_state["exercise"]),
#         "breakfast_yes": enc("아침식사여부", st.session_state["breakfast_yes_raw"]),
#         "alcohol_weekly": int(st.session_state["alcohol_week"]),
#         "bmi": float(bmi),
#     }

#     st.session_state["patient"] = {
#         "이름": name,
#         "나이": int(st.session_state.get("age", 0)),
#         "성별": st.session_state["gender_raw"],
#         "날짜": str(st.session_state.get("date")),
#         "BMI": float(bmi),
#     }
#     st.session_state["features_raw"] = features_raw
#     st.session_state["features_enc"] = features_enc
#     st.session_state["_login_error"] = ""

#     # 페이지 이동
#     st.switch_page("pages/02_상담자_전용.py")

# st.button("상담자 전용 화면으로 이동", on_click=try_login)

# if st.session_state.get("_login_error"):
#     st.error(st.session_state["_login_error"])


#     # 세션 저장: 환자(헤더용), 피처(raw/enc)
#     st.session_state["patient"] = {
#         "이름": name,
#         "나이": int(age),            # ← 모델 미사용, 헤더 노출용
#         "성별": gender_raw,
#         "날짜": str(date),
#         "BMI": float(bmi),
#     }
#     st.session_state["features_raw"] = features_raw
#     st.session_state["features_enc"] = features_enc
#     st.session_state["_login_error"] = ""
#     # go(NAV_COUNSELOR)
# st.switch_page("pages/02_상담자_전용.py")
# # st.button("상담자 전용 화면으로 이동", on_click=try_login)

# if st.session_state.get("_login_error"):
#     st.error(st.session_state["_login_error"])


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
