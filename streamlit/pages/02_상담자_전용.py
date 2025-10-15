# pages/02_상담자_전용.py
import streamlit as st
import pandas as pd

# ❌ 기존 코드: go 함수와 plotly.graph_objects의 이름 충돌 발생
# from utils.state import init_state, NAV_INPUT, go

# ✅ 수정된 코드: go 함수를 import하지 않고 state 초기화만 사용
from utils.state import init_state
from utils.pdf_utils import build_pdf_bytes
from utils.model_loader import predict_proba_from_features
from data.defaults import success_avg

import plotly.graph_objects as go
import plotly.express as px

# =========================
# 기본 설정 / 테마 색
# =========================
st.set_page_config(page_title="상담자 전용", layout="wide")
init_state()

PRIMARY = "#78D8A5"
INK = "#0F172A"
MUTED = "#64748B"

# =========================
# 가드: 입력 확인
# =========================
if not st.session_state.get("patient") or not st.session_state.get("features_enc"):
    st.warning("먼저 '환자 정보 입력' 페이지에서 정보를 저장하세요.")
    
    # ❌ 기존 코드: go 함수 사용 (이름 충돌로 인해 오류 발생)
    # st.button("환자 정보 입력으로 이동", on_click=go, args=(NAV_INPUT,))
    
    # ✅ 수정된 코드: 버튼 클릭 시 직접 페이지 전환
    if st.button("환자 정보 입력으로 이동"):
        st.switch_page("pages/01_고객_정보_입력.py")
    st.stop()

patient = st.session_state["patient"]
name = patient.get("이름", "-")
age = patient.get("나이", "-")
visit_date = patient.get("날짜", "-")
bmi = patient.get("BMI", None)

features_raw = st.session_state.get("features_raw", {})
features_enc = st.session_state["features_enc"]

# =========================
# 헤더
# =========================
st.subheader(f"환자: {name} (만 {age}세) | 방문일: {visit_date}")

st.markdown(
    f"""
    <div style="
      border:1px solid #E5E7EB;border-radius:12px;padding:16px 20px;
      background:linear-gradient(180deg,#EAF8F0 0%,#FFFFFF 100%);
      display:flex;align-items:center;justify-content:space-between;">
      <div style="font-weight:700;color:{INK}">{name} 고객님</div>
      <div style="color:{MUTED}">BMI: <span style="color:{INK};font-weight:700">{bmi if bmi is not None else '-'}</span></div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# =========================
# 예측 확률 계산 (모델→실패 시 더미)
# =========================
USE_MODEL = True
def build_model_features(enc: dict) -> dict:
    keys = [
        '성별', '시도번호', '가구원수_전체', '기초생활수급자여부', '가구식품안정성여부', '아침식사빈도',
       '영양표시설인지여부', '영양표시영향여부', '구강건강자기평가', '저작불편여부', '점심후양치여부', '저녁양치여부',
       '평생 음주 여부', '연간 음주 빈도', '한 번 섭취 시 음주량', '절주 또는 금주계획 여부',
       '최근 1주일 유연성 운동 실천', '스트레스정도', '스트레스상담여부', '취침시간', '기상시간',
       '화장실각성여부', '악몽경험여부', '기억력저하여부', '상담여부', '치매검사여부', '가정내흡연자존재',
       '직장간접흡연노출', '졸업상태', 'age_group', 'is_single', 'house_income_grp',
       'fma_dementia_case', 'education_group', 'is_economically_active',
       'occupation_type', 'is_employee', 'weight_control_method',
       'activity_score_weight', 'activity_score', 'marital_stability'
    ]
    out = {k: enc[k] for k in keys if k in enc}
    return out

# def build_model_features(enc: dict) -> dict:
#     keys = [
#         "sex", "marital_stability", "breakfast_freq", "weight_control_method",
#         "toilet_awake", "ever_drink", "year_drink_freq", "drink_per_occasion",
#         "home_smoker", "dementia_test", "occupation_type", "sleep_time_hour",
#         "flex_ex_week", "oral_health_self", "exercise_per_week",
#         "breakfast_yes", "alcohol_weekly", "stress_score",
#     ]
#     return {k: enc[k] if k in enc else 0 for k in keys}

def mirror_kor_feature_for_model(d: dict) -> dict:
    d = dict(d)
    if "oral_health_self" in d and "구강건강자기평가" not in d:
        d["구강건강자기평가"] = d["oral_health_self"]
    return d

def dummy_score_for_fallback(raw: dict, enc: dict) -> float:
    ex = enc.get("exercise_per_week", 0)
    bf_yes = enc.get("breakfast_yes", 0)
    drink = enc.get("drink_per_occasion", 0)
    stress = enc.get("stress_score", 3)
    oral = enc.get("oral_health_self", 3)
    s = (
        (ex / 7) * 0.30 +
        bf_yes * 0.15 +
        (max(0, 6 - drink) / 6) * 0.20 +
        ((6 - stress) / 5) * 0.20 +
        (oral / 5) * 0.15
    )
    return max(0.0, min(1.0, s))

try:
    model_features = build_model_features(features_enc)
    model_features = mirror_kor_feature_for_model(model_features)
    if USE_MODEL:
        success_probability = predict_proba_from_features(model_features) * 100.0
    else:
        success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0
except Exception:
    success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0

# ✅ 새로 추가: PDF 생성을 위해 예측 확률을 세션에 저장
st.session_state["_prediction_probability"] = success_probability

# =========================
# 성공자 평균 참조치 (없으면 기본값)
# =========================
avg_map = dict(zip(success_avg["특성"], success_avg["평균값"]))
success_avg_now = {
    "운동빈도": float(avg_map.get("운동빈도", 4)),
    "스트레스": float(avg_map.get("스트레스", 3)),
    "아침식사": float(avg_map.get("아침식사", 1)),
    "음주량": float(avg_map.get("음주량", 2)),
    "구강건강": float(avg_map.get("구강건강자기평가", 3)),
}

# =========================
# 표시용 파생값(권장사항용 추가 피처 포함)
# =========================
# patient_view = {
#     "운동빈도": float(features_raw.get("운동빈도", 0)),
#     "스트레스": float(features_raw.get("스트레스", 3)),
#     "아침식사": 1.0 if str(features_raw.get("아침식사여부", "아니오")) == "예" else 0.0,
#     "음주량": float(features_raw.get("주당 총 음주량", features_raw.get("한 번 섭취 시 음주량", 0))),

# }
# 환자 표시 데이터 (raw 기준)
patient_view = {
    "운동빈도": float(features_raw.get("운동빈도", 0)),
    "스트레스": float(features_raw.get("스트레스", 3)),
    "아침식사": 1.0 if str(features_raw.get("아침식사여부", "아니오")) == "예" else 0.0,
    "음주량": float(features_raw.get("한 번 섭취 시 음주량", 0)),
    "구강건강": float(features_enc.get("oral_health_self", 3))
}
# 추가 피처 값(권장사항 확장에 사용)
bf_freq = int(features_enc.get("breakfast_freq", 0))          # 0~4
year_freq = int(features_enc.get("year_drink_freq", 0))       # 0~5
per_once = int(features_enc.get("drink_per_occasion", 0))     # 0~15+
flex_ex = int(features_enc.get("flex_ex_week", 0))            # 0~3
home_smoker = int(features_enc.get("home_smoker", 0))         # 0/1
work_smoke = int(st.session_state.get("work_smoke_code", 0))  # 0/1 (없으면 0)
wt_ctrl = str(features_raw.get("weight_control_method", "없음"))
age_group = int(st.session_state.get("age_group", 0))         # 연령대 코드(없으면 0)

# =========================
# 개선 필요 영역
# =========================
needs = []
if patient_view["운동빈도"] < success_avg_now["운동빈도"]: needs.append("운동")
if patient_view["스트레스"] > success_avg_now["스트레스"]: needs.append("스트레스")
if patient_view["아침식사"] < success_avg_now["아침식사"]: needs.append("아침식사")
if patient_view["음주량"] > success_avg_now["음주량"]: needs.append("음주")
if patient_view["구강건강"] < success_avg_now["구강건강"]: needs.append("구강건강")

# =========================
# 메트릭 요약
# =========================
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("금연 성공 예측 확률", f"{success_probability:.1f}%", f"{success_probability - 50:.1f}%p (평균 대비)")
with m2:
    status = "높음" if success_probability >= 70 else ("보통" if success_probability >= 50 else "낮음")
    st.metric("성공 가능성", status)
with m3:
    st.metric("개선 필요 영역", f"{len(needs)}개", " · ".join(needs) if needs else "양호")

# =========================
# 그래프 섹션
# =========================
st.markdown("---")
st.header("상세 분석")

col1, col2 = st.columns([6, 6], vertical_alignment="top")

with col1:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=success_probability,
        title={'text': "성공 확률 (%)", 'font': {'color': INK}},
        delta={'reference': 50, 'increasing': {'color': PRIMARY}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': MUTED},
            'bar': {'color': PRIMARY},
            'steps': [
                {'range': [0, 30], 'color': "#FEE2E2"},
                {'range': [30, 70], 'color': "#F3F4F6"},
                {'range': [70, 100], 'color': "#E9F8F0"},
            ],
            'threshold': {'line': {'color': "#EF4444", 'width': 3}, 'thickness': 0.7, 'value': 50},
            'shape': "angular",
        }
    ))
    fig_gauge.update_layout(height=260, margin=dict(l=0, r=0, t=60, b=40))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    categories = ['운동빈도', '스트레스(역점수)', '아침식사', '음주(역점수)', '구강건강']

    ex     = float(patient_view.get('운동빈도', 0))
    stress = float(patient_view.get('스트레스', 3))
    bf     = float(patient_view.get('아침식사', 0))
    drink  = float(patient_view.get('음주량', 0))
    oral   = float(patient_view.get('구강건강', 3))

    patient_scores = [
        (ex / 7.0) * 10.0,
        ((6.0 - stress) / 5.0) * 10.0,
        bf * 10.0,
        (max(0.0, 6.0 - drink) / 6.0) * 10.0,
        (oral / 5.0) * 10.0,
    ]

    ex_avg     = float(success_avg_now.get('운동빈도', 4))
    stress_avg = float(success_avg_now.get('스트레스', 3))
    bf_avg     = float(success_avg_now.get('아침식사', 1))
    drink_avg  = float(success_avg_now.get('음주량', 2))
    oral_avg   = float(success_avg_now.get('구강건강', 3))

    success_scores = [
        (ex_avg / 7.0) * 10.0,
        ((6.0 - stress_avg) / 5.0) * 10.0,
        bf_avg * 10.0,
        (max(0.0, 6.0 - drink_avg) / 6.0) * 10.0,
        (oral_avg / 5.0) * 10.0,
    ]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=patient_scores, theta=categories, fill='toself',
        name='현재 환자', line_color='#F97316'
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=success_scores, theta=categories, fill='toself',
        name='성공자 평균', line_color=PRIMARY
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True,
        legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
        height=260,
        margin=dict(l=0, r=0, t=30, b=40)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# =========================
# 생활 지표 비교 + 개선 우선순위
# =========================
st.subheader("생활 지표 비교")
c3, c4 = st.columns(2)

with c3:
    df_cmp = pd.DataFrame({
        '지표': ['운동빈도', '스트레스(낮을수록 좋음)', '아침식사', '음주량(적을수록 좋음)', '구강건강(높을수록 좋음)'],
        '환자': [
            patient_view['운동빈도'],
            patient_view['스트레스'],
            patient_view['아침식사'],
            patient_view['음주량'],
            patient_view['구강건강'],
        ],
        '성공자 평균': [
            success_avg_now['운동빈도'],
            success_avg_now['스트레스'],
            success_avg_now['아침식사'],
            success_avg_now['음주량'],
            success_avg_now['구강건강'],
        ],
    })
    fig_cmp = px.bar(
        df_cmp, x='지표', y=['환자', '성공자 평균'],
        barmode='group',
        color_discrete_map={'환자': '#F97316', '성공자 평균': PRIMARY},
        title='주요 생활 지표',
    )
    fig_cmp.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=0))
    st.plotly_chart(fig_cmp, use_container_width=True)

with c4:
    gap = {
        "운동": max(0, success_avg_now['운동빈도'] - patient_view['운동빈도']) / 7,
        "스트레스": max(0, patient_view['스트레스'] - success_avg_now['스트레스']) / 5,
        "아침식사": max(0, success_avg_now['아침식사'] - patient_view['아침식사']),
        "음주": max(0, patient_view['음주량'] - success_avg_now['음주량']) / 6,
        "구강건강": max(0, success_avg_now['구강건강'] - patient_view['구강건강']) / 5,
    }
    gap.update({
        "유연성운동": max(0, 2 - flex_ex) / 3,
        "아침식사빈도": max(0, 2 - bf_freq) / 4,
    })

    df_priority = (pd.Series(gap, name="개선필요도")
                   .sort_values(ascending=True)
                   .rename_axis("영역").reset_index())
    fig_priority = px.bar(
        df_priority, y='영역', x='개선필요도', orientation='h',
        color='개선필요도', color_continuous_scale='Greens',
        title='개선 우선순위',
    )
    fig_priority.update_layout(height=300, showlegend=False, margin=dict(l=10, r=10, t=30, b=0))
    st.plotly_chart(fig_priority, use_container_width=True)

# =========================
# 맞춤형 권장사항
# =========================
st.markdown("---")
st.header("맞춤형 권장사항")

recs = []
if "운동" in needs:
    recs.append((
        "운동 빈도 증가",
        f"주 {patient_view['운동빈도']}회 → 목표 주 {success_avg_now['운동빈도']}회",
        "규칙적인 유산소부터 시작해 빈도를 서서히 늘리세요."
    ))
if "스트레스" in needs:
    recs.append((
        "스트레스 관리",
        f"현재 {patient_view['스트레스']}/5",
        "호흡·명상 5분 루틴과 가벼운 걷기로 급격한 스트레스 상승을 완화하세요."
    ))
if "아침식사" in needs:
    recs.append((
        "아침식사 습관",
        "현재: 비정기적 또는 결식",
        "단백질·섬유질 위주의 간단한 식사를 매일 유지해 오전 흡연욕구를 낮추세요."
    ))
if "음주" in needs:
    recs.append((
        "음주량 조절",
        f"주 {patient_view['음주량']}잔 → 목표 주 {success_avg_now['음주량']}잔 이하",
        "주중 무알코올 데이를 지정하고 저도주로 전환하는 등 단계적으로 줄이세요."
    ))
if "구강건강" in needs:
    recs.append((
        "구강건강 관리",
        f"현재 {patient_view['구강건강']}/5 → 목표 {success_avg_now['구강건강']}/5",
        "식후/취침 전 양치, 치실·가글 습관화, 정기 스케일링으로 구강 불편을 줄여 흡연욕구 트리거를 완화하세요."
    ))

extra_recs = []
if bf_freq <= 1:
    extra_recs.append((
        "아침식사 빈도 개선",
        f"현재 빈도 지수 {bf_freq}/4",
        "주 3회 이상으로 늘리기부터 시작하고, 요거트·과일·견과류 등 준비물을 간소화하세요."
    ))
if year_freq >= 4 or per_once >= 5:
    extra_recs.append((
        "음주 패턴 조절",
        f"연간 빈도 지수 {year_freq}/5, 1회 {per_once}잔",
        "무알코올 데이 지정, 저도주 전환, 모임 전 식사·물 1잔 선행 등으로 1회 음주량을 줄이세요."
    ))
if flex_ex <= 1:
    extra_recs.append((
        "유연성 운동 루틴 추가",
        f"최근 1주 유연성 운동 지수 {flex_ex}/3",
        "매일 10분 스트레칭과 호흡운동으로 긴장 완화와 금연 갈망 저하를 노려보세요."
    ))
if home_smoker == 1:
    extra_recs.append((
        "가정 내 간접흡연 차단",
        "가정 내 흡연자 존재",
        "가정 내 전 구역 금연 선언, 환기 규칙 합의, 방문 전·후 환기 등으로 노출을 차단하세요."
    ))
if work_smoke == 1:
    extra_recs.append((
        "직장 내 간접흡연 노출 감소",
        "근무 중 간접흡연 노출",
        "흡연구역 동선 회피, 상급자·산안담당과 차폐·재배치 요청, 휴게시간 대체 동선을 마련하세요."
    ))
if wt_ctrl in ("없음",):
    extra_recs.append((
        "체중 관리 계획 수립",
        f"현재 방법: {wt_ctrl}",
        "주 150분 유산소+주 2회 근력, 가벼운 탄수 절감·단백질 보강으로 초간단 병행 플랜을 시작하세요."
    ))
if age_group >= 60 and patient_view["구강건강"] <= 3:
    extra_recs.append((
        "고령층 구강 관리 강화",
        f"자가평가 {patient_view['구강건강']}/5",
        "수분 보충, 무설탕 껌, 틀니·치주 점검 주기화, 스케일링 예약으로 구강 불편을 줄이세요."
    ))

recs.extend(extra_recs)

if not recs:
    st.info("현재 수치가 전반적으로 양호합니다. 유지 관리에 집중하세요.")
else:
    for title, current, tip in recs:
        with st.expander(title, expanded=False):
            c1, c2 = st.columns([2, 3])
            with c1:
                st.write(current)
            with c2:
                st.write(tip)

# =========================
# PDF 저장
# =========================
st.markdown("---")
st.write("리포트 저장")
comments = []

if st.button("PDF 미리 생성"):
    try:
        st.session_state["_pdf_bytes"] = build_pdf_bytes(name, comments)
        st.success("PDF가 생성되었습니다. 아래 버튼으로 다운로드하세요.")
    except Exception as e:
        st.error(f"PDF 생성 실패: {e}")

if st.session_state.get("_pdf_bytes"):
    st.download_button(
        label="PDF 다운로드",
        data=st.session_state["_pdf_bytes"],
        file_name=f"{name}_금연리포트.pdf",
        mime="application/pdf",
    )




# # pages/02_상담자_전용.py
# import streamlit as st
# import pandas as pd
# from pathlib import Path

# from utils.state import init_state, NAV_INPUT, go
# from utils.pdf_utils import build_pdf_bytes
# from utils.model_loader import predict_proba_from_features # 기존
# # from utils.model_loader import predict_proba_from_raw
# from data.defaults import success_avg, patient_data_all

# import plotly.graph_objects as go
# import plotly.express as px

# # =========================
# # 기본 설정 / 테마 색
# # =========================
# st.set_page_config(page_title="상담자 전용", layout="wide")
# init_state()

# PRIMARY = "#78D8A5"  # 연한 그린
# INK = "#0F172A"
# MUTED = "#64748B"

# # =========================
# # 가드: 입력 확인
# # =========================
# if not st.session_state.get("patient") or not st.session_state.get("features_enc"):
#     st.warning("먼저 '환자 정보 입력' 페이지에서 정보를 저장하세요.")
#     st.button("환자 정보 입력으로 이동", on_click=go, args=(NAV_INPUT,))
#     st.stop()

# patient = st.session_state["patient"]
# name = patient.get("이름", "-")
# age = patient.get("나이", "-")
# visit_date = patient.get("날짜", "-")
# bmi = patient.get("BMI", None)

# features_raw = st.session_state.get("features_raw", {})  # 시각화/설명용
# features_enc = st.session_state["features_enc"]          # 모델 입력용 (인코딩된 값)



# # =========================
# # 헤더 (토스풍 심플)
# # =========================
# st.subheader(f"환자: {name} (만 {age}세) | 방문일: {visit_date}")


# # c1, c2 = st.columns([3, 1])
# # with c1:
# #     st.subheader(f"환자: {name} (만 {age}세) | 방문일: {visit_date}")
# # with c2:
# #     sel = st.selectbox("다른 환자 보기(데모)", ["(선택 안 함)"] + list(patient_data_all.keys()))
# #     if st.button("열기") and sel != "(선택 안 함)":
# #         demo = patient_data_all[sel]
# #         st.session_state["patient"] = {"이름": sel, "날짜": visit_date, **demo}
# #         st.experimental_rerun()

# # BMI 카드 느낌 (상단 네모칸)
# st.markdown(
#     f"""
#     <div style="
#       border:1px solid #E5E7EB;border-radius:12px;padding:16px 20px;
#       background:linear-gradient(180deg,#EAF8F0 0%,#FFFFFF 100%);
#       display:flex;align-items:center;justify-content:space-between;">
#       <div style="font-weight:700;color:{INK}">{name} 고객님</div>
#       <div style="color:{MUTED}">BMI: <span style="color:{INK};font-weight:700">{bmi if bmi is not None else '-'}</span></div>
#     </div>
#     """,
#     unsafe_allow_html=True
# )

# st.markdown("---")

# # =========================
# # 예측 확률 계산
# #  - 실제 모델 연결. 실패 시 더미 점수로 폴백
# # =========================
# # =========================
# # 예측 확률 계산
# #  - 실제 모델 연결. 실패 시 더미 점수로 폴백
# # =========================
# USE_MODEL = True

# def build_model_features(enc: dict) -> dict:
#     keys = [
#         "sex", "marital_stability", "breakfast_freq", "weight_control_method",
#         "toilet_awake", "ever_drink", "year_drink_freq", "drink_per_occasion",
#         "home_smoker", "dementia_test", "occupation_type", "sleep_time_hour",
#         "flex_ex_week", "oral_health_self", "exercise_per_week",
#         "breakfast_yes", "alcohol_weekly", "stress_score",
#     ]
#     out = {k: enc[k] for k in keys if k in enc}
#     return out

# def dummy_score_for_fallback(raw: dict, enc: dict) -> float:
#     # 모델 파일이 없거나 로딩 실패 시 사용할 임시 점수 (0~1)
#     ex = enc.get("exercise_per_week", 0)        # 0~7 (↑좋음)
#     bf_yes = enc.get("breakfast_yes", 0)        # 0/1 (↑좋음)
#     drink = enc.get("drink_per_occasion", 0)    # 0~15+ (↓좋음)
#     stress = enc.get("stress_score", 3)         # 1~5 (↓좋음)
#     oral = enc.get("oral_health_self", 3)       # 1~5 (↑좋음)

#     s = (
#         (ex / 7) * 0.30 +
#         bf_yes * 0.15 +
#         (max(0, 6 - drink) / 6) * 0.20 +
#         ((6 - stress) / 5) * 0.20 +
#         (oral / 5) * 0.15
#     )
#     return max(0.0, min(1.0, s))


# # def dummy_score_for_fallback(raw: dict, enc: dict) -> float: # 기존
# #     ex = enc.get("exercise_per_week", 0)       # 0~7
# #     bf_yes = enc.get("breakfast_yes", 0)       # 0/1
# #     drink = enc.get("drink_per_occasion", 0)   # 0~15+
# #     stress = enc.get("stress_score", 3)        # 1~5
# #     s = ((ex / 7) * 0.35 +
# #          bf_yes * 0.20 +
# #          (max(0, 6 - drink) / 6) * 0.25 +
# #          ((6 - stress) / 5) * 0.20)
# #     return max(0.0, min(1.0, s))

# # ✅ 여기가 try/except 위치입니다
# try:
#     model_features = build_model_features(features_enc)
#     if USE_MODEL:
#         success_probability = predict_proba_from_features(model_features) * 100.0
#     else:
#         success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0
# except Exception as e:
#     # st.info(f"모델 예측에 실패하여 임시 점수로 대체합니다. ({e})")
#     success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0


# # try:
# #     # 기존 build_model_features(features_enc)는 삭제
# #     if USE_MODEL:
# #         # ✅ 원시 입력(features_raw)으로부터 바로 예측
# #         success_probability = predict_proba_from_raw(features_raw) * 100.0
# #     else:
# #         # 모델 사용 안 하는 경우 (테스트용)
# #         success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0

# # except Exception as e:
# #     st.info(f"모델 예측에 실패하여 임시 점수로 대체합니다. ({e})")
# #     success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0


# # try:
# #     model_features = build_model_features(features_enc)
# #     if USE_MODEL:
# #         success_probability = predict_proba_from_features(model_features) * 100.0
# #     else:
# #         success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0
# # except Exception as e:
# #     st.info(f"모델 예측에 실패하여 임시 점수로 대체합니다. ({e})")
# #     success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0

# # try: 3:24
# #     model_features = build_model_features(features_enc)
# #     if USE_MODEL:
# #         success_probability = predict_proba_from_features(model_features) * 100.0
# #     else:
# #         success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0
# # except Exception:
# #     # 콘솔 로그만 남기고 UI에는 표시하지 않음
# #     # import traceback; print("[predict fallback]\n", traceback.format_exc())
# #     success_probability = dummy_score_for_fallback(features_raw, features_enc) * 100.0


# # =========================
# # 성공자 평균 참조치
# #  - success_avg에 없는 항목은 디폴트로 보정
# # =========================

# avg_map = dict(zip(success_avg["특성"], success_avg["평균값"]))
# success_avg_now = {
#     "운동빈도": float(avg_map.get("운동빈도", 4)),
#     "스트레스": float(avg_map.get("스트레스", 3)),
#     "아침식사": float(avg_map.get("아침식사", 1)),
#     "음주량": float(avg_map.get("음주량", 2)),
#     "구강건강": float(avg_map.get("구강건강자기평가", 3)),  # 없으면 3으로
# }


# # avg_map = dict(zip(success_avg["특성"], success_avg["평균값"])) # 기존
# # success_avg_now = {
# #     "운동빈도": float(avg_map.get("운동빈도", 4)),
# #     "스트레스": float(avg_map.get("스트레스", 3)),
# #     "아침식사": float(avg_map.get("아침식사", 1)),
# #     # 비교용 음주량(없으면 2로 가정)
# #     "음주량": float(avg_map.get("음주량", 2)),
# #     # 수면시간은 실제 모델 피처에 없어서 비교용으로만 필요하면 기본값
# #     "수면시간": float(avg_map.get("수면시간", 7)),
# # }

# # 환자 표시 데이터 (raw 기준)

# patient_view = {
#     "운동빈도": float(features_raw.get("운동빈도", 0)),
#     "스트레스": float(features_raw.get("스트레스", 3)),
#     "아침식사": 1.0 if str(features_raw.get("아침식사여부", "아니오")) == "예" else 0.0,
#     "음주량": float(features_raw.get("주당 총 음주량", features_raw.get("한 번 섭취 시 음주량", 0))),
#     "구강건강": float(features_enc.get("oral_health_self", 3)),  # 1~5
# }


# # patient_view = { 
# #     "운동빈도": float(features_raw.get("운동빈도", 0)),
# #     "스트레스": float(features_raw.get("스트레스", 3)),
# #     "아침식사": 1.0 if str(features_raw.get("아침식사여부", "아니오")) == "예" else 0.0,
# #     "음주량": float(features_raw.get("주당 총 음주량", features_raw.get("한 번 섭취 시 음주량", 0))),
# #     # 필요 시 수면시간을 표시용으로만 쓸 수 있음(모델 입력 아님)
# #     "수면시간": float(features_raw.get("수면시간", 7.0)),
# # } # 기존

# # 개선 필요 영역

# needs = []
# if patient_view["운동빈도"] < success_avg_now["운동빈도"]: needs.append("운동")
# if patient_view["스트레스"] > success_avg_now["스트레스"]: needs.append("스트레스")
# if patient_view["아침식사"] < success_avg_now["아침식사"]: needs.append("아침식사")
# if patient_view["음주량"] > success_avg_now["음주량"]: needs.append("음주")
# if patient_view["구강건강"] < success_avg_now["구강건강"]: needs.append("구강건강")


# # needs = [] # 기존
# # if patient_view["운동빈도"] < success_avg_now["운동빈도"]: needs.append("운동")
# # if patient_view["수면시간"] < success_avg_now["수면시간"]: needs.append("수면")
# # if patient_view["스트레스"] > success_avg_now["스트레스"]: needs.append("스트레스")
# # if patient_view["아침식사"] < success_avg_now["아침식사"]: needs.append("아침식사")
# # if patient_view["음주량"] > success_avg_now["음주량"]: needs.append("음주")

# # =========================
# # 메트릭 요약
# # =========================
# m1, m2, m3 = st.columns(3)
# with m1:
#     st.metric("금연 성공 예측 확률", f"{success_probability:.1f}%", f"{success_probability - 50:.1f}%p (평균 대비)")
# with m2:
#     status = "높음" if success_probability >= 70 else ("보통" if success_probability >= 50 else "낮음")
#     st.metric("성공 가능성", status)
# with m3:
#     st.metric("개선 필요 영역", f"{len(needs)}개", " · ".join(needs) if needs else "양호")

# # =========================
# # 그래프 섹션
# # =========================
# st.markdown("---")
# st.header("상세 분석")

# # 좌우 2컬럼
# col1, col2 = st.columns([6, 6], vertical_alignment="top")

# # ──────────────── 게이지 (왼쪽) ────────────────
# with col1:
#     fig_gauge = go.Figure(go.Indicator(
#         mode="gauge+number+delta",
#         value=success_probability,
#         title={'text': "성공 확률 (%)", 'font': {'color': INK}},
#         delta={'reference': 50, 'increasing': {'color': PRIMARY}},
#         gauge={
#             'axis': {'range': [0, 100], 'tickcolor': MUTED},
#             'bar': {'color': PRIMARY},
#             'steps': [
#                 {'range': [0, 30], 'color': "#FEE2E2"},
#                 {'range': [30, 70], 'color': "#F3F4F6"},
#                 {'range': [70, 100], 'color': "#E9F8F0"},
#             ],
#             'threshold': {'line': {'color': "#EF4444", 'width': 3}, 'thickness': 0.7, 'value': 50},
#             'shape': "angular",
#         }
#     ))
#     fig_gauge.update_layout(height=260, margin=dict(l=0, r=0, t=60, b=40)) # t=60사이즈
#     st.plotly_chart(fig_gauge, use_container_width=True)

# # ──────────────── 레이더 (오른쪽) ────────────────
# with col2:
#     import numpy as np

#     categories = ['운동빈도', '스트레스(역점수)', '아침식사', '음주(역점수)', '구강건강']

# ex     = float(patient_view.get('운동빈도', 0))
# stress = float(patient_view.get('스트레스', 3))
# bf     = float(patient_view.get('아침식사', 0))
# drink  = float(patient_view.get('음주량', 0))
# oral   = float(patient_view.get('구강건강', 3))

# patient_scores = [
#     (ex / 7.0) * 10.0,
#     ((6.0 - stress) / 5.0) * 10.0,
#     bf * 10.0,
#     (max(0.0, 6.0 - drink) / 6.0) * 10.0,
#     (oral / 5.0) * 10.0,
# ]

# ex_avg     = float(success_avg_now.get('운동빈도', 4))
# stress_avg = float(success_avg_now.get('스트레스', 3))
# bf_avg     = float(success_avg_now.get('아침식사', 1))
# drink_avg  = float(success_avg_now.get('음주량', 2))
# oral_avg   = float(success_avg_now.get('구강건강', 3))

# success_scores = [
#     (ex_avg / 7.0) * 10.0,
#     ((6.0 - stress_avg) / 5.0) * 10.0,
#     bf_avg * 10.0,
#     (max(0.0, 6.0 - drink_avg) / 6.0) * 10.0,
#     (oral_avg / 5.0) * 10.0,
# ]


#     # categories = ['운동빈도', '수면시간', '스트레스(역점수)', '아침식사', '음주(역점수)'] # 기존

#     # def _safe(v, default=0.0):
#     #     try:
#     #         x = float(v)
#     #         if np.isnan(x) or np.isinf(x):
#     #             return default
#     #         return x
#     #     except Exception:
#     #         return default

#     # ex     = _safe(patient_view.get('운동빈도', 0))
#     # sleep  = _safe(patient_view.get('수면시간', 7))
#     # stress = _safe(patient_view.get('스트레스', 3))
#     # bf     = 1.0 if str(patient_view.get('아침식사', 0)) in ('1','예','True','true') else 0.0
#     # drink  = _safe(patient_view.get('음주량', 0))

#     # patient_scores = [
#     #     (ex / 7.0) * 10.0,
#     #     (sleep / 9.0) * 10.0,
#     #     ((6.0 - stress) / 5.0) * 10.0,
#     #     bf * 10.0,
#     #     (max(0.0, 6.0 - drink) / 6.0) * 10.0,
#     # ]

#     ex_avg     = _safe(success_avg_now.get('운동빈도', 4))
#     sleep_avg  = _safe(success_avg_now.get('수면시간', 7))
#     stress_avg = _safe(success_avg_now.get('스트레스', 3))
#     bf_avg     = _safe(success_avg_now.get('아침식사', 1))
#     drink_avg  = _safe(success_avg_now.get('음주량', 2))

#     success_scores = [
#         (ex_avg / 7.0) * 10.0,
#         (sleep_avg / 9.0) * 10.0,
#         ((6.0 - stress_avg) / 5.0) * 10.0,
#         bf_avg * 10.0,
#         (max(0.0, 6.0 - drink_avg) / 6.0) * 10.0,
#     ]

#     fig_radar = go.Figure()
#     fig_radar.add_trace(go.Scatterpolar(
#         r=patient_scores, theta=categories, fill='toself',
#         name='현재 환자', line_color='#F97316'
#     ))
#     fig_radar.add_trace(go.Scatterpolar(
#         r=success_scores, theta=categories, fill='toself',
#         name='성공자 평균', line_color=PRIMARY
#     ))
#     fig_radar.update_layout(
#         polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
#         showlegend=True,
#         legend=dict(orientation="h", yanchor="top", y=-0.2, xanchor="center", x=0.5),
#         height=260,
#         margin=dict(l=0, r=0, t=30, b=40)
#     )
#     st.plotly_chart(fig_radar, use_container_width=True)




# # with col_b:
# #     categories = ['운동빈도', '수면시간', '스트레스(역점수)', '아침식사', '음주(역점수)']
# #     patient_scores = [
# #         (patient_view['운동빈도'] / 7) * 10,
# #         (patient_view['수면시간'] / 9) * 10,
# #         ((6 - patient_view['스트레스']) / 5) * 10,
# #         patient_view['아침식사'] * 10,
# #         (max(0, 6 - patient_view['음주량']) / 6) * 10,
# #     ]
# #     success_scores = [
# #         (success_avg_now['운동빈도'] / 7) * 10,
# #         (success_avg_now['수면시간'] / 9) * 10,
# #         ((6 - success_avg_now['스트레스']) / 5) * 10,
# #         success_avg_now['아침식사'] * 10,
# #         (max(0, 6 - success_avg_now['음주량']) / 6) * 10,
# #     ]
# #     fig_radar = go.Figure()
# #     fig_radar.add_trace(go.Scatterpolar(r=patient_scores, theta=categories, fill='toself',
# #                                         name='현재 환자', line_color="#F97316"))
# #     fig_radar.add_trace(go.Scatterpolar(r=success_scores, theta=categories, fill='toself',
# #                                         name='성공자 평균', line_color=PRIMARY))
# #     fig_radar.update_layout(
# #         polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
# #         showlegend=True, height=300, margin=dict(l=10, r=10, t=30, b=0)
# #     )
# #     st.plotly_chart(fig_radar, use_container_width=True)

# # 2) 생활 지표 비교 + 개선 우선순위
# st.subheader("생활 지표 비교")
# c3, c4 = st.columns(2)

# with c3:

#     df_cmp = pd.DataFrame({
#     '지표': ['운동빈도', '스트레스(낮을수록 좋음)', '아침식사', '음주량(적을수록 좋음)', '구강건강(높을수록 좋음)'],
#     '환자': [
#         patient_view['운동빈도'],
#         patient_view['스트레스'],
#         patient_view['아침식사'],
#         patient_view['음주량'],
#         patient_view['구강건강'],
#     ],
#     '성공자 평균': [
#         success_avg_now['운동빈도'],
#         success_avg_now['스트레스'],
#         success_avg_now['아침식사'],
#         success_avg_now['음주량'],
#         success_avg_now['구강건강'],
#     ],
# })
    
#     # df_cmp = pd.DataFrame({
#     #     '지표': ['수면시간', '운동빈도', '스트레스(낮을수록 좋음)', '아침식사', '음주량(적을수록 좋음)'],
#     #     '환자': [
#     #         patient_view['수면시간'],
#     #         patient_view['운동빈도'],
#     #         patient_view['스트레스'],
#     #         patient_view['아침식사'],
#     #         patient_view['음주량'],
#     #     ],
#     #     '성공자 평균': [
#     #         success_avg_now['수면시간'],
#     #         success_avg_now['운동빈도'],
#     #         success_avg_now['스트레스'],
#     #         success_avg_now['아침식사'],
#     #         success_avg_now['음주량'],
#     #     ],
#     # }) # 기존
#     fig_cmp = px.bar(
#         df_cmp, x='지표', y=['환자', '성공자 평균'],
#         barmode='group',
#         color_discrete_map={'환자': '#F97316', '성공자 평균': PRIMARY},
#         title='주요 생활 지표',
#     )
#     fig_cmp.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=0))
#     st.plotly_chart(fig_cmp, use_container_width=True)

# with c4:

#     gap = {
#     "운동": max(0, success_avg_now['운동빈도'] - patient_view['운동빈도']) / 7,
#     "스트레스": max(0, patient_view['스트레스'] - success_avg_now['스트레스']) / 5,
#     "아침식사": max(0, success_avg_now['아침식사'] - patient_view['아침식사']),
#     "음주": max(0, patient_view['음주량'] - success_avg_now['음주량']) / 6,
#     "구강건강": max(0, success_avg_now['구강건강'] - patient_view['구강건강']) / 5,
# }

#     # gap = {
#     #     "운동": max(0, success_avg_now['운동빈도'] - patient_view['운동빈도']) / 7,
#     #     "수면": max(0, success_avg_now['수면시간'] - patient_view['수면시간']) / 9,
#     #     "스트레스": max(0, patient_view['스트레스'] - success_avg_now['스트레스']) / 5,
#     #     "아침식사": max(0, success_avg_now['아침식사'] - patient_view['아침식사']),
#     #     "음주": max(0, patient_view['음주량'] - success_avg_now['음주량']) / 6,
#     # } # 기존
#     df_priority = (pd.Series(gap, name="개선필요도")
#                    .sort_values(ascending=True)
#                    .rename_axis("영역").reset_index())
#     fig_priority = px.bar(
#         df_priority, y='영역', x='개선필요도', orientation='h',
#         color='개선필요도', color_continuous_scale='Greens',
#         title='개선 우선순위',
#     )
#     fig_priority.update_layout(height=300, showlegend=False, margin=dict(l=10, r=10, t=30, b=0))
#     st.plotly_chart(fig_priority, use_container_width=True)

# # 3) 맞춤형 권장사항
# st.markdown("---")
# st.header("맞춤형 권장사항")

# recs = []
# if "운동" in needs:
#     recs.append(("운동 빈도 증가",
#                  f"주 {patient_view['운동빈도']}회 → 목표 주 {success_avg_now['운동빈도']}회",
#                  "규칙적인 유산소부터 시작해 빈도를 서서히 늘리세요."))
# if "스트레스" in needs:
#     recs.append(("스트레스 관리",
#                  f"현재 {patient_view['스트레스']}/5",
#                  "호흡·명상 5분 루틴과 가벼운 걷기로 급격한 스트레스 상승을 완화하세요."))
# if "아침식사" in needs:
#     recs.append(("아침식사 습관",
#                  "현재: 비정기적 또는 결식",
#                  "단백질·섬유질 위주의 간단한 식사를 매일 유지해 오전 흡연욕구를 낮추세요."))
# if "음주" in needs:
#     recs.append(("음주량 조절",
#                  f"주 {patient_view['음주량']}잔 → 목표 주 {success_avg_now['음주량']}잔 이하",
#                  "주중 무알코올 데이를 지정하고 저도주로 전환하는 등 단계적으로 줄이세요."))
# if "구강건강" in needs:
#     recs.append(("구강건강 관리",
#                  f"현재 {patient_view['구강건강']}/5 → 목표 {success_avg_now['구강건강']}/5",
#                  "식후/취침 전 양치, 치실·가글 습관화, 정기 스케일링으로 구강 불편을 줄여 흡연욕구 트리거를 완화하세요."))


# # recs = [] # 기존
# # if "운동" in needs:
# #     recs.append(("운동 빈도 증가",
# #                  f"주 {patient_view['운동빈도']}회 → 목표 주 {success_avg_now['운동빈도']}회",
# #                  "규칙적인 유산소부터 시작해 빈도를 서서히 늘리세요."))
# # if "수면" in needs:
# #     recs.append(("수면 시간 개선",
# #                  f"{patient_view['수면시간']}시간 → 목표 {success_avg_now['수면시간']}시간",
# #                  "취침 1시간 전 스크린 타임을 줄이고 일정한 수면 리듬을 유지하세요."))
# # if "스트레스" in needs:
# #     recs.append(("스트레스 관리",
# #                  f"현재 {patient_view['스트레스']}/5",
# #                  "호흡·명상 5분 루틴과 가벼운 운동으로 급격한 스트레스 상승을 완화하세요."))
# # if "아침식사" in needs:
# #     recs.append(("아침식사 습관",
# #                  "현재: 비정기적 또는 결식",
# #                  "단백질·섬유질 위주의 간단한 식사를 매일 유지해 오전 흡연욕구를 낮추세요."))
# # if "음주" in needs:
# #     recs.append(("음주량 조절",
# #                  f"주 {patient_view['음주량']}잔 → 목표 주 {success_avg_now['음주량']}잔 이하",
# #                  "주중 무알코올 데이를 지정하고 저도주로 전환하는 등 단계적으로 줄이세요."))

# if not recs:
#     st.info("현재 수치가 전반적으로 양호합니다. 유지 관리에 집중하세요.")
# else:
#     for title, current, tip in recs:
#         with st.expander(title, expanded=False):
#             c1, c2 = st.columns([2, 3])
#             with c1:
#                 st.write(current)  # 이미 "현재 / 목표"가 합쳐져 있음
#             with c2:
#                 st.write(tip)



# # =========================
# # PDF 저장
# # =========================
# st.markdown("---")
# st.write("리포트 저장")
# comments = []  # pdf 유틸 요구 형식 맞춤(필요시 개선 포인트 텍스트 넣어도 됨)

# # pages/02_상담자_전용.py
# if st.button("PDF 미리 생성"):
#     try:
#         st.session_state["_pdf_bytes"] = build_pdf_bytes(name, comments)
#         st.success("PDF가 생성되었습니다. 아래 버튼으로 다운로드하세요.")
#     except Exception as e:
#         st.error(f"PDF 생성 실패: {e}")

# if st.session_state.get("_pdf_bytes"):
#     st.download_button(
#         label="PDF 다운로드",
#         data=st.session_state["_pdf_bytes"],
#         file_name=f"{name}_금연리포트.pdf",
#         mime="application/pdf",
#     )

#=========================

# # 스타일 색상
# PRIMARY = "#78D8A5"   # 연한 그린
# INK = "#0F172A"
# MUTED = "#64748B"



# st.set_page_config(page_title="상담자 전용", layout="wide")
# init_state()

# st.title("상담자 전용")

# # 환자 세션 확인
# if not st.session_state.get("patient"):
#     st.warning("먼저 '환자 정보 입력' 페이지에서 정보를 저장하세요.")
#     st.button("환자 정보 입력으로 이동", on_click=go, args=(NAV_INPUT,))
#     st.stop()

# patient = st.session_state["patient"]
# name = patient["이름"]

# # 헤더
# col1, col2 = st.columns([3, 1])
# with col1:
#     st.subheader(f"환자: {name}  |  방문일: {patient.get('날짜','-')}")
# with col2:
#     selected = st.selectbox("다른 환자 보기(데모)", ["(선택 안 함)"] + list(patient_data_all.keys()))
#     if st.button("열기") and selected != "(선택 안 함)":
#         p_demo = patient_data_all[selected]
#         st.session_state["patient"] = {"이름": selected, "날짜": patient.get("날짜",""), **p_demo}
#         st.experimental_rerun()

# # 현재 환자 참조
# p = st.session_state["patient"]

# # ---------------------------------------
# # 과거 비교(예시)  — 필요하면 접기/펼치기
# # ---------------------------------------
# with st.expander("과거 데이터 비교 보기"):
#     past_data = {'수면시간': 6, '아침식사': 1, '운동빈도': 3, '스트레스': 4}
#     df_past = pd.DataFrame({
#         '특성': success_avg['특성'],
#         '이번 방문': [p['수면시간'], p['아침식사'], p['운동빈도'], p['스트레스']],
#         '지난 방문': [past_data['수면시간'], past_data['아침식사'], past_data['운동빈도'], past_data['스트레스']]
#     })
#     bar_compare(df_past, "특성", ["이번 방문", "지난 방문"], y_label="값")

# # =======================================================
# # 금연 성공 예측 분석 리포트
# # (age_group 등 나이 기반 특징은 사용하지 않음)
# # =======================================================
# st.markdown("---")
# st.title("금연 성공 예측 분석 리포트")

# # 입력 → 분석용 스키마 매핑
# patient_data = {
#     "운동빈도": float(p["운동빈도"]),
#     "수면시간": float(p["수면시간"]),
#     "스트레스": float(p["스트레스"]),           # 1~5 (낮을수록 좋음)
#     "아침식사": float(p["아침식사"]),           # 0/1
#     "음주량": float(p.get("음주량", 0.0)),
# }
# avg_map = dict(zip(success_avg["특성"], success_avg["평균값"]))
# success_avg_now = {
#     "운동빈도": float(avg_map.get("운동빈도", 4)),
#     "수면시간": float(avg_map.get("수면시간", 7)),
#     "스트레스": float(avg_map.get("스트레스", 3)),
#     "아침식사": float(avg_map.get("아침식사", 1)),
#     "음주량": float(avg_map.get("음주량", 2)),
# }

# # 간단 가중치 기반 더미 예측 (실제 모델 연결 시 교체)
# score = (
#     (patient_data["운동빈도"] / 7) * 0.25 +
#     (patient_data["수면시간"] / 9) * 0.25 +
#     ((6 - patient_data["스트레스"]) / 5) * 0.20 +
#     (patient_data["아침식사"]) * 0.15 +
#     (max(0, 6 - patient_data["음주량"]) / 6) * 0.15
# )
# success_probability = max(0, min(100, score * 100))

# # 요약 메트릭
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric(
#         label="금연 성공 확률",
#         value=f"{success_probability:.1f}%",
#         delta=f"{success_probability - 50:.1f}%p (평균 대비)"
#     )
# with col2:
#     status = "높음" if success_probability >= 70 else ("보통" if success_probability >= 50 else "낮음")
#     st.metric(label="성공 가능성", value=status)
# with col3:
#     needs = []
#     if patient_data["운동빈도"] < success_avg_now["운동빈도"]: needs.append("운동")
#     if patient_data["수면시간"] < success_avg_now["수면시간"]: needs.append("수면")
#     if patient_data["스트레스"] > success_avg_now["스트레스"]: needs.append("스트레스")
#     if patient_data["아침식사"] < success_avg_now["아침식사"]: needs.append("아침식사")
#     if patient_data["음주량"] > success_avg_now["음주량"]: needs.append("음주")
#     st.metric(label="개선 필요 영역", value=f"{len(needs)}개", delta=(" · ".join(needs) if needs else "양호"))

# st.markdown("---")
# st.header("상세 분석")

# # ================= 상세 분석 (그래프 섹션) =================
# # ── 1) 게이지 + 레이더
# col_a, col_b = st.columns([7, 5])  # 게이지가 넓게 보이도록 비율 조정

# with col_a:
#     fig_gauge = go.Figure(go.Indicator(
#         mode="gauge+number+delta",
#         value=success_probability,
#         title={'text': "성공 확률 (%)", 'font': {'color': INK}},
#         delta={'reference': 50, 'increasing': {'color': PRIMARY}},
#         gauge={
#             'axis': {'range': [0, 100], 'tickcolor': MUTED},
#             'bar': {'color': PRIMARY},
#             'steps': [
#                 {'range': [0, 30], 'color': "#FEE2E2"},
#                 {'range': [30, 70], 'color': "#F3F4F6"},
#                 {'range': [70, 100], 'color': "#E9F8F0"},
#             ],
#             'threshold': {'line': {'color': "#EF4444", 'width': 3}, 'thickness': 0.7, 'value': 50},
#             'shape': "angular",  # 반원형
#         }
#     ))
#     # ⬇️ 짤림 방지: 높이·마진 튜닝
#     fig_gauge.update_layout(height=260, margin=dict(l=0, r=0, t=30, b=40))
#     st.plotly_chart(fig_gauge, use_container_width=True)

# with col_b:
#     categories = ['운동빈도', '수면시간', '스트레스(역점수)', '아침식사', '음주(역점수)']
#     patient_scores = [
#         (patient_data['운동빈도'] / 7) * 10,
#         (patient_data['수면시간'] / 9) * 10,
#         ((6 - patient_data['스트레스']) / 5) * 10,
#         patient_data['아침식사'] * 10,
#         (max(0, 6 - patient_data['음주량']) / 6) * 10,
#     ]
#     success_scores = [
#         (success_avg_now['운동빈도'] / 7) * 10,
#         (success_avg_now['수면시간'] / 9) * 10,
#         ((6 - success_avg_now['스트레스']) / 5) * 10,
#         success_avg_now['아침식사'] * 10,
#         (max(0, 6 - success_avg_now['음주량']) / 6) * 10,
#     ]
#     fig_radar = go.Figure()
#     fig_radar.add_trace(go.Scatterpolar(r=patient_scores, theta=categories, fill='toself',
#                                         name='현재 환자', line_color="#F97316"))
#     fig_radar.add_trace(go.Scatterpolar(r=success_scores, theta=categories, fill='toself',
#                                         name='성공자 평균', line_color=PRIMARY))
#     fig_radar.update_layout(
#         polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
#         showlegend=True, height=300, margin=dict(l=10, r=10, t=30, b=0)
#     )
#     st.plotly_chart(fig_radar, use_container_width=True)

# # ── 2) 생활 지표 비교 + 개선 우선순위
# st.subheader("생활 지표 비교")
# col_c, col_d = st.columns(2)

# with col_c:
#     df_cmp = pd.DataFrame({
#         '지표': ['수면시간', '운동빈도', '스트레스(낮을수록 좋음)', '아침식사', '음주량(적을수록 좋음)'],
#         '환자': [
#             patient_data['수면시간'],
#             patient_data['운동빈도'],
#             patient_data['스트레스'],
#             patient_data['아침식사'],
#             patient_data['음주량'],
#         ],
#         '성공자 평균': [
#             success_avg_now['수면시간'],
#             success_avg_now['운동빈도'],
#             success_avg_now['스트레스'],
#             success_avg_now['아침식사'],
#             success_avg_now['음주량'],
#         ],
#     })
#     fig_cmp = px.bar(
#         df_cmp, x='지표', y=['환자', '성공자 평균'],
#         barmode='group',
#         color_discrete_map={'환자': '#F97316', '성공자 평균': PRIMARY},
#         title='주요 생활 지표',
#     )
#     fig_cmp.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=0))
#     st.plotly_chart(fig_cmp, use_container_width=True)

# with col_d:
#     gap = {
#         "운동": max(0, success_avg_now['운동빈도'] - patient_data['운동빈도']) / 7,
#         "수면": max(0, success_avg_now['수면시간'] - patient_data['수면시간']) / 9,
#         "스트레스": max(0, patient_data['스트레스'] - success_avg_now['스트레스']) / 5,
#         "아침식사": max(0, success_avg_now['아침식사'] - patient_data['아침식사']),
#         "음주": max(0, patient_data['음주량'] - success_avg_now['음주량']) / 6,
#     }
#     df_priority = (pd.Series(gap, name="개선필요도")
#                    .sort_values(ascending=True)
#                    .rename_axis("영역").reset_index())
#     fig_priority = px.bar(
#         df_priority, y='영역', x='개선필요도', orientation='h',
#         color='개선필요도', color_continuous_scale='Greens',
#         title='개선 우선순위',
#     )
#     fig_priority.update_layout(height=300, showlegend=False, margin=dict(l=10, r=10, t=30, b=0))
#     st.plotly_chart(fig_priority, use_container_width=True)

# # ── 3) 맞춤형 권장사항
# st.markdown("---")
# st.header("맞춤형 권장사항")

# recs = []
# if "운동" in needs:
#     recs.append(("운동 빈도 증가",
#                  f"주 {patient_data['운동빈도']}회 → 목표 주 {success_avg_now['운동빈도']}회",
#                  "규칙적인 유산소부터 시작해 빈도를 서서히 늘리세요."))
# if "수면" in needs:
#     recs.append(("수면 시간 개선",
#                  f"{patient_data['수면시간']}시간 → 목표 {success_avg_now['수면시간']}시간",
#                  "취침 1시간 전 스크린 타임을 줄이고 일정한 수면 리듬을 유지하세요."))
# if "스트레스" in needs:
#     recs.append(("스트레스 관리",
#                  f"현재 {patient_data['스트레스']}/5",
#                  "호흡·명상 5분 루틴과 가벼운 운동으로 급격한 스트레스 상승을 완화하세요."))
# if "아침식사" in needs:
#     recs.append(("아침식사 습관",
#                  "현재: 비정기적 또는 결식",
#                  "단백질·섬유질 위주의 간단한 식사를 매일 유지해 오전 흡연욕구를 낮추세요."))
# if "음주" in needs:
#     recs.append(("음주량 조절",
#                  f"주 {patient_data['음주량']}잔 → 목표 주 {success_avg_now['음주량']}잔 이하",
#                  "주중 무알코올 데이를 지정하고 저도주로 전환하는 등 단계적으로 줄이세요."))

# if not recs:
#     st.info("현재 수치가 전반적으로 양호합니다. 유지 관리에 집중하세요.")
# else:
#     for title, current, tip in recs:
#         with st.expander(title, expanded=False):
#             c1, c2 = st.columns([2, 3])
#             with c1:
#                 st.write(f"현재 상태 / 목표: {current}")
#             with c2:
#                 st.write(tip)

# # ================= 리포트 저장 =================
# st.markdown("---")
# st.write("리포트 저장")
# comments = []  # (PDF 유틸이 요구하는 인자 형태 맞춤)
# if st.button("PDF 미리 생성"):
#     st.session_state["_pdf_bytes"] = build_pdf_bytes(name, comments)
#     st.success("PDF가 생성되었습니다. 아래 버튼으로 다운로드하세요.")

# if st.session_state.get("_pdf_bytes"):
#     st.download_button(
#         label="PDF 다운로드",
#         data=st.session_state["_pdf_bytes"],
#         file_name=f"{name}_금연리포트.pdf",
#         mime="application/pdf",
#     )
# else:
#     st.info("먼저 [PDF 미리 생성]을 눌러주세요.")

#===========================

# # pages/02_상담자_전용.py
# import streamlit as st
# import pandas as pd
# from utils.state import init_state, NAV_INPUT, go
# from utils.plot_utils import bar_compare
# from utils.pdf_utils import build_pdf_bytes
# from data.defaults import success_avg, patient_data_all
# import plotly.graph_objects as go
# import plotly.express as px

# # =========================
# # 기본 설정
# # =========================
# st.set_page_config(page_title="상담자 전용", layout="wide")
# init_state()

# st.title("상담자 전용")

# if not st.session_state.get("patient"):
#     st.warning("먼저 '환자 정보 입력' 페이지에서 정보를 저장하세요.")
#     st.button("환자 정보 입력으로 이동", on_click=go, args=(NAV_INPUT,))
#     st.stop()

# patient = st.session_state["patient"]
# name = patient["이름"]

# col1, col2 = st.columns([3, 1])
# with col1:
#     st.subheader(f"환자: {name}  |  방문일: {patient.get('날짜','-')}")
# with col2:
#     selected = st.selectbox("다른 환자 보기(데모)", ["(선택 안 함)"] + list(patient_data_all.keys()))
#     if st.button("열기") and selected != "(선택 안 함)":
#         p = patient_data_all[selected]
#         st.session_state["patient"] = {"이름": selected, "날짜": patient.get("날짜",""), **p}
#         st.experimental_rerun()

# p = st.session_state["patient"]

# # 과거 비교(예시)
# with st.expander("과거 데이터 비교 보기"):
#     past_data = {'수면시간': 6, '아침식사': 1, '운동빈도': 3, '스트레스': 4}
#     df_past = pd.DataFrame({
#         '특성': success_avg['특성'],
#         '이번 방문': [p['수면시간'], p['아침식사'], p['운동빈도'], p['스트레스']],
#         '지난 방문': [past_data['수면시간'], past_data['아침식사'], past_data['운동빈도'], past_data['스트레스']]
#     })
#     bar_compare(df_past, "특성", ["이번 방문", "지난 방문"], y_label="값")

# # =======================================================
# # 금연 성공 예측 분석 리포트 (새로 추가된 통합 섹션)
# # =======================================================
# PRIMARY = "#78D8A5"   # 연한 그린
# INK = "#0F172A"
# MUTED = "#64748B"

# st.markdown("---")
# st.title("금연 성공 예측 분석 리포트")

# # 환자/평균 매핑 (현재 보유 필드 기준)
# patient_data = {
#     "운동빈도": float(p["운동빈도"]),
#     "수면시간": float(p["수면시간"]),
#     "스트레스": float(p["스트레스"]),           # 1~5 (낮을수록 좋음)
#     "아침식사": float(p["아침식사"]),           # 0/1
#     "음주량": float(p.get("음주량", 0.0)),      # 주당 잔수 등
# }
# avg_map = dict(zip(success_avg["특성"], success_avg["평균값"]))
# success_avg_now = {
#     "운동빈도": float(avg_map.get("운동빈도", 4)),
#     "수면시간": float(avg_map.get("수면시간", 7)),
#     "스트레스": float(avg_map.get("스트레스", 3)),
#     "아침식사": float(avg_map.get("아침식사", 1)),
#     "음주량": float(avg_map.get("음주량", 2)),
# }

# # 더미 예측 점수(실제 모델로 교체 가능)
# score = (
#     (patient_data["운동빈도"] / 7) * 0.25 +
#     (patient_data["수면시간"] / 9) * 0.25 +
#     ((6 - patient_data["스트레스"]) / 5) * 0.20 +
#     (patient_data["아침식사"]) * 0.15 +
#     (max(0, 6 - patient_data["음주량"]) / 6) * 0.15
# )
# success_probability = max(0, min(100, score * 100))

# # 1) 요약 메트릭
# col1, col2, col3 = st.columns(3)
# with col1:
#     st.metric(
#         label="금연 성공 확률",
#         value=f"{success_probability:.1f}%",
#         delta=f"{success_probability - 50:.1f}%p (평균 대비)"
#     )
# with col2:
#     status = "높음" if success_probability >= 70 else ("보통" if success_probability >= 50 else "낮음")
#     st.metric(label="성공 가능성", value=status)
# with col3:
#     needs = []
#     if patient_data["운동빈도"] < success_avg_now["운동빈도"]: needs.append("운동")
#     if patient_data["수면시간"] < success_avg_now["수면시간"]: needs.append("수면")
#     if patient_data["스트레스"] > success_avg_now["스트레스"]: needs.append("스트레스")
#     if patient_data["아침식사"] < success_avg_now["아침식사"]: needs.append("아침식사")
#     if patient_data["음주량"] > success_avg_now["음주량"]: needs.append("음주")
#     st.metric(label="개선 필요 영역", value=f"{len(needs)}개", delta=(" · ".join(needs) if needs else "양호"))

# st.markdown("---")
# st.header("상세 분석")

# # 2) 시각화
# col_a, col_b = st.columns(2)

# # 2-1. 게이지
# with col_a:
#     fig_gauge = go.Figure(go.Indicator(
#         mode="gauge+number+delta",
#         value=success_probability,
#         domain={'x': [0, 1], 'y': [0, 1]},
#         title={'text': "성공 확률 (%)", 'font': {'color': INK}},
#         delta={'reference': 50, 'increasing': {'color': PRIMARY}},
#         gauge={
#             'axis': {'range': [0, 100], 'tickcolor': MUTED},
#             'bar': {'color': PRIMARY},
#             'steps': [
#                 {'range': [0, 30], 'color': "#FEE2E2"},
#                 {'range': [30, 70], 'color': "#F3F4F6"},
#                 {'range': [70, 100], 'color': "#E9F8F0"}
#             ],
#             'threshold': {
#                 'line': {'color': "#EF4444", 'width': 3},
#                 'thickness': 0.7,
#                 'value': 50
#             }
#         }
#     ))
#     fig_gauge.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=0))
#     st.plotly_chart(fig_gauge, use_container_width=True)

# # 2-2. 레이더 (보유 필드만)
# with col_b:
#     categories = ['운동빈도', '수면시간', '스트레스(역점수)', '아침식사', '음주(역점수)']
#     patient_scores = [
#         (patient_data['운동빈도'] / 7) * 10,
#         (patient_data['수면시간'] / 9) * 10,
#         (6 - patient_data['스트레스']) / 5 * 10,
#         patient_data['아침식사'] * 10,
#         (max(0, 6 - patient_data['음주량']) / 6) * 10
#     ]
#     success_scores = [
#         (success_avg_now['운동빈도'] / 7) * 10,
#         (success_avg_now['수면시간'] / 9) * 10,
#         (6 - success_avg_now['스트레스']) / 5 * 10,
#         success_avg_now['아침식사'] * 10,
#         (max(0, 6 - success_avg_now['음주량']) / 6) * 10
#     ]
#     fig_radar = go.Figure()
#     fig_radar.add_trace(go.Scatterpolar(
#         r=patient_scores, theta=categories, fill='toself',
#         name='현재 환자', line_color="#F97316"
#     ))
#     fig_radar.add_trace(go.Scatterpolar(
#         r=success_scores, theta=categories, fill='toself',
#         name='성공자 평균', line_color=PRIMARY
#     ))
#     fig_radar.update_layout(
#         polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
#         showlegend=True, height=300, margin=dict(l=10, r=10, t=30, b=0)
#     )
#     st.plotly_chart(fig_radar, use_container_width=True)

# # 2-3. 생활 지표 비교 막대
# st.subheader("생활 지표 비교")
# col_c, col_d = st.columns(2)

# with col_c:
#     df_cmp = pd.DataFrame({
#         '지표': ['수면시간', '운동빈도', '스트레스(낮을수록 좋음)', '아침식사', '음주량(적을수록 좋음)'],
#         '환자': [
#             patient_data['수면시간'],
#             patient_data['운동빈도'],
#             patient_data['스트레스'],
#             patient_data['아침식사'],
#             patient_data['음주량'],
#         ],
#         '성공자 평균': [
#             success_avg_now['수면시간'],
#             success_avg_now['운동빈도'],
#             success_avg_now['스트레스'],
#             success_avg_now['아침식사'],
#             success_avg_now['음주량'],
#         ]
#     })
#     fig_cmp = px.bar(
#         df_cmp, x='지표', y=['환자', '성공자 평균'],
#         barmode='group',
#         color_discrete_map={'환자': '#F97316', '성공자 평균': PRIMARY},
#         title='주요 생활 지표'
#     )
#     fig_cmp.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=0))
#     st.plotly_chart(fig_cmp, use_container_width=True)

# with col_d:
#     gap = {
#         "운동": max(0, success_avg_now['운동빈도'] - patient_data['운동빈도']) / 7,
#         "수면": max(0, success_avg_now['수면시간'] - patient_data['수면시간']) / 9,
#         "스트레스": max(0, patient_data['스트레스'] - success_avg_now['스트레스']) / 5,
#         "아침식사": max(0, success_avg_now['아침식사'] - patient_data['아침식사']),
#         "음주": max(0, patient_data['음주량'] - success_avg_now['음주량']) / 6,
#     }
#     df_priority = (pd.Series(gap, name="개선필요도")
#                    .sort_values(ascending=True)
#                    .rename_axis("영역").reset_index())
#     fig_priority = px.bar(
#         df_priority, y='영역', x='개선필요도', orientation='h',
#         color='개선필요도', color_continuous_scale='Greens',
#         title='개선 우선순위'
#     )
#     fig_priority.update_layout(height=300, showlegend=False, margin=dict(l=10, r=10, t=30, b=0))
#     st.plotly_chart(fig_priority, use_container_width=True)

# # 3) 맞춤형 권장사항
# st.markdown("---")
# st.header("맞춤형 권장사항")

# recs = []
# if "운동" in needs:
#     recs.append(("운동 빈도 증가", f"주 {patient_data['운동빈도']}회 → 목표 주 {success_avg_now['운동빈도']}회",
#                  "규칙적인 유산소부터 시작해 빈도를 서서히 늘리세요."))
# if "수면" in needs:
#     recs.append(("수면 시간 개선", f"{patient_data['수면시간']}시간 → 목표 {success_avg_now['수면시간']}시간",
#                  "취침 1시간 전 스크린 타임을 줄이고 일정한 수면 리듬을 유지하세요."))
# if "스트레스" in needs:
#     recs.append(("스트레스 관리", f"현재 {patient_data['스트레스']}/5",
#                  "호흡·명상 5분 루틴과 가벼운 운동으로 급격한 스트레스 상승을 완화하세요."))
# if "아침식사" in needs:
#     recs.append(("아침식사 습관", "현재: 비정기적 또는 결식",
#                  "단백질/섬유질 위주의 간단한 식사를 매일 유지해 오전 흡연욕구를 낮추세요."))
# if "음주" in needs:
#     recs.append(("음주량 조절", f"주 {patient_data['음주량']}잔 → 목표 주 {success_avg_now['음주량']}잔 이하",
#                  "주중 무알코올 데이를 지정하고 저도주로 전환하는 등 단계적으로 줄이세요."))

# if not recs:
#     st.info("현재 수치가 전반적으로 양호합니다. 유지 관리에 집중하세요.")
# else:
#     for title, current, tip in recs:
#         with st.expander(title, expanded=False):
#             c1, c2 = st.columns([2, 3])
#             with c1:
#                 st.write(f"현재 상태 / 목표: {current}")
#             with c2:
#                 st.write(tip)

# # =========================
# # PDF 저장
# # =========================
# st.markdown("---")
# st.write("### 리포트 저장")
# if st.button("PDF 미리 생성"):
#     st.session_state["_pdf_bytes"] = build_pdf_bytes(name, comments)
#     st.success("PDF가 생성되었습니다. 아래 버튼으로 다운로드하세요.")

# if st.session_state.get("_pdf_bytes"):
#     st.download_button(
#         label="PDF 다운로드",
#         data=st.session_state["_pdf_bytes"],
#         file_name=f"{name}_금연리포트.pdf",  # <- 파일명 변경
#         mime="application/pdf",
#     )
# else:
#     st.info("먼저 [PDF 미리 생성]을 눌러주세요.")
