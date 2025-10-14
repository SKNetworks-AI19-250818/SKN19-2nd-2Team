# import streamlit as st
# import pandas as pd
# from utils.state import init_state, NAV_INPUT, go
# from utils.plot_utils import bar_compare
# from utils.pdf_utils import build_pdf_bytes
# from data.defaults import success_avg, patient_data_all
# import pandas as pd
# import plotly.graph_objects as go
# import plotly.express as px

# pages/02_상담자_전용.py
import streamlit as st
import pandas as pd
from utils.state import init_state, NAV_INPUT, go
from utils.plot_utils import bar_compare
from utils.pdf_utils import build_pdf_bytes
from data.defaults import success_avg, patient_data_all
import plotly.graph_objects as go
import plotly.express as px

# =========================
# 기본 설정
# =========================
st.set_page_config(page_title="상담자 전용", layout="wide")
init_state()

st.title("상담자 전용")

if not st.session_state.get("patient"):
    st.warning("먼저 '환자 정보 입력' 페이지에서 정보를 저장하세요.")
    st.button("환자 정보 입력으로 이동", on_click=go, args=(NAV_INPUT,))
    st.stop()

patient = st.session_state["patient"]
name = patient["이름"]

col1, col2 = st.columns([3, 1])
with col1:
    st.subheader(f"환자: {name}  |  방문일: {patient.get('날짜','-')}")
with col2:
    selected = st.selectbox("다른 환자 보기(데모)", ["(선택 안 함)"] + list(patient_data_all.keys()))
    if st.button("열기") and selected != "(선택 안 함)":
        p = patient_data_all[selected]
        st.session_state["patient"] = {"이름": selected, "날짜": patient.get("날짜",""), **p}
        st.experimental_rerun()

p = st.session_state["patient"]

# 과거 비교(예시)
with st.expander("과거 데이터 비교 보기"):
    past_data = {'수면시간': 6, '아침식사': 1, '운동빈도': 3, '스트레스': 4}
    df_past = pd.DataFrame({
        '특성': success_avg['특성'],
        '이번 방문': [p['수면시간'], p['아침식사'], p['운동빈도'], p['스트레스']],
        '지난 방문': [past_data['수면시간'], past_data['아침식사'], past_data['운동빈도'], past_data['스트레스']]
    })
    bar_compare(df_past, "특성", ["이번 방문", "지난 방문"], y_label="값")

# =======================================================
# 금연 성공 예측 분석 리포트 (새로 추가된 통합 섹션)
# =======================================================
PRIMARY = "#78D8A5"   # 연한 그린
INK = "#0F172A"
MUTED = "#64748B"

st.markdown("---")
st.title("금연 성공 예측 분석 리포트")

# 환자/평균 매핑 (현재 보유 필드 기준)
patient_data = {
    "운동빈도": float(p["운동빈도"]),
    "수면시간": float(p["수면시간"]),
    "스트레스": float(p["스트레스"]),           # 1~5 (낮을수록 좋음)
    "아침식사": float(p["아침식사"]),           # 0/1
    "음주량": float(p.get("음주량", 0.0)),      # 주당 잔수 등
}
avg_map = dict(zip(success_avg["특성"], success_avg["평균값"]))
success_avg_now = {
    "운동빈도": float(avg_map.get("운동빈도", 4)),
    "수면시간": float(avg_map.get("수면시간", 7)),
    "스트레스": float(avg_map.get("스트레스", 3)),
    "아침식사": float(avg_map.get("아침식사", 1)),
    "음주량": float(avg_map.get("음주량", 2)),
}

# 더미 예측 점수(실제 모델로 교체 가능)
score = (
    (patient_data["운동빈도"] / 7) * 0.25 +
    (patient_data["수면시간"] / 9) * 0.25 +
    ((6 - patient_data["스트레스"]) / 5) * 0.20 +
    (patient_data["아침식사"]) * 0.15 +
    (max(0, 6 - patient_data["음주량"]) / 6) * 0.15
)
success_probability = max(0, min(100, score * 100))

# 1) 요약 메트릭
col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="금연 성공 확률",
        value=f"{success_probability:.1f}%",
        delta=f"{success_probability - 50:.1f}%p (평균 대비)"
    )
with col2:
    status = "높음" if success_probability >= 70 else ("보통" if success_probability >= 50 else "낮음")
    st.metric(label="성공 가능성", value=status)
with col3:
    needs = []
    if patient_data["운동빈도"] < success_avg_now["운동빈도"]: needs.append("운동")
    if patient_data["수면시간"] < success_avg_now["수면시간"]: needs.append("수면")
    if patient_data["스트레스"] > success_avg_now["스트레스"]: needs.append("스트레스")
    if patient_data["아침식사"] < success_avg_now["아침식사"]: needs.append("아침식사")
    if patient_data["음주량"] > success_avg_now["음주량"]: needs.append("음주")
    st.metric(label="개선 필요 영역", value=f"{len(needs)}개", delta=(" · ".join(needs) if needs else "양호"))

st.markdown("---")
st.header("상세 분석")

# 2) 시각화
col_a, col_b = st.columns(2)

# 2-1. 게이지
with col_a:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=success_probability,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "성공 확률 (%)", 'font': {'color': INK}},
        delta={'reference': 50, 'increasing': {'color': PRIMARY}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': MUTED},
            'bar': {'color': PRIMARY},
            'steps': [
                {'range': [0, 30], 'color': "#FEE2E2"},
                {'range': [30, 70], 'color': "#F3F4F6"},
                {'range': [70, 100], 'color': "#E9F8F0"}
            ],
            'threshold': {
                'line': {'color': "#EF4444", 'width': 3},
                'thickness': 0.7,
                'value': 50
            }
        }
    ))
    fig_gauge.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=0))
    st.plotly_chart(fig_gauge, use_container_width=True)

# 2-2. 레이더 (보유 필드만)
with col_b:
    categories = ['운동빈도', '수면시간', '스트레스(역점수)', '아침식사', '음주(역점수)']
    patient_scores = [
        (patient_data['운동빈도'] / 7) * 10,
        (patient_data['수면시간'] / 9) * 10,
        (6 - patient_data['스트레스']) / 5 * 10,
        patient_data['아침식사'] * 10,
        (max(0, 6 - patient_data['음주량']) / 6) * 10
    ]
    success_scores = [
        (success_avg_now['운동빈도'] / 7) * 10,
        (success_avg_now['수면시간'] / 9) * 10,
        (6 - success_avg_now['스트레스']) / 5 * 10,
        success_avg_now['아침식사'] * 10,
        (max(0, 6 - success_avg_now['음주량']) / 6) * 10
    ]
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=patient_scores, theta=categories, fill='toself',
        name='현재 환자', line_color="#F97316"
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=success_scores, theta=categories, fill='toself',
        name='성공자 평균', line_color=PRIMARY
    ))
    fig_radar.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
        showlegend=True, height=300, margin=dict(l=10, r=10, t=30, b=0)
    )
    st.plotly_chart(fig_radar, use_container_width=True)

# 2-3. 생활 지표 비교 막대
st.subheader("생활 지표 비교")
col_c, col_d = st.columns(2)

with col_c:
    df_cmp = pd.DataFrame({
        '지표': ['수면시간', '운동빈도', '스트레스(낮을수록 좋음)', '아침식사', '음주량(적을수록 좋음)'],
        '환자': [
            patient_data['수면시간'],
            patient_data['운동빈도'],
            patient_data['스트레스'],
            patient_data['아침식사'],
            patient_data['음주량'],
        ],
        '성공자 평균': [
            success_avg_now['수면시간'],
            success_avg_now['운동빈도'],
            success_avg_now['스트레스'],
            success_avg_now['아침식사'],
            success_avg_now['음주량'],
        ]
    })
    fig_cmp = px.bar(
        df_cmp, x='지표', y=['환자', '성공자 평균'],
        barmode='group',
        color_discrete_map={'환자': '#F97316', '성공자 평균': PRIMARY},
        title='주요 생활 지표'
    )
    fig_cmp.update_layout(height=300, margin=dict(l=10, r=10, t=30, b=0))
    st.plotly_chart(fig_cmp, use_container_width=True)

with col_d:
    gap = {
        "운동": max(0, success_avg_now['운동빈도'] - patient_data['운동빈도']) / 7,
        "수면": max(0, success_avg_now['수면시간'] - patient_data['수면시간']) / 9,
        "스트레스": max(0, patient_data['스트레스'] - success_avg_now['스트레스']) / 5,
        "아침식사": max(0, success_avg_now['아침식사'] - patient_data['아침식사']),
        "음주": max(0, patient_data['음주량'] - success_avg_now['음주량']) / 6,
    }
    df_priority = (pd.Series(gap, name="개선필요도")
                   .sort_values(ascending=True)
                   .rename_axis("영역").reset_index())
    fig_priority = px.bar(
        df_priority, y='영역', x='개선필요도', orientation='h',
        color='개선필요도', color_continuous_scale='Greens',
        title='개선 우선순위'
    )
    fig_priority.update_layout(height=300, showlegend=False, margin=dict(l=10, r=10, t=30, b=0))
    st.plotly_chart(fig_priority, use_container_width=True)

# 3) 맞춤형 권장사항
st.markdown("---")
st.header("맞춤형 권장사항")

recs = []
if "운동" in needs:
    recs.append(("운동 빈도 증가", f"주 {patient_data['운동빈도']}회 → 목표 주 {success_avg_now['운동빈도']}회",
                 "규칙적인 유산소부터 시작해 빈도를 서서히 늘리세요."))
if "수면" in needs:
    recs.append(("수면 시간 개선", f"{patient_data['수면시간']}시간 → 목표 {success_avg_now['수면시간']}시간",
                 "취침 1시간 전 스크린 타임을 줄이고 일정한 수면 리듬을 유지하세요."))
if "스트레스" in needs:
    recs.append(("스트레스 관리", f"현재 {patient_data['스트레스']}/5",
                 "호흡·명상 5분 루틴과 가벼운 운동으로 급격한 스트레스 상승을 완화하세요."))
if "아침식사" in needs:
    recs.append(("아침식사 습관", "현재: 비정기적 또는 결식",
                 "단백질/섬유질 위주의 간단한 식사를 매일 유지해 오전 흡연욕구를 낮추세요."))
if "음주" in needs:
    recs.append(("음주량 조절", f"주 {patient_data['음주량']}잔 → 목표 주 {success_avg_now['음주량']}잔 이하",
                 "주중 무알코올 데이를 지정하고 저도주로 전환하는 등 단계적으로 줄이세요."))

if not recs:
    st.info("현재 수치가 전반적으로 양호합니다. 유지 관리에 집중하세요.")
else:
    for title, current, tip in recs:
        with st.expander(title, expanded=False):
            c1, c2 = st.columns([2, 3])
            with c1:
                st.write(f"현재 상태 / 목표: {current}")
            with c2:
                st.write(tip)

# =========================
# PDF 저장
# =========================
st.markdown("---")
st.write("### 리포트 저장")
if st.button("PDF 미리 생성"):
    st.session_state["_pdf_bytes"] = build_pdf_bytes(name, comments)
    st.success("PDF가 생성되었습니다. 아래 버튼으로 다운로드하세요.")

if st.session_state.get("_pdf_bytes"):
    st.download_button(
        label="PDF 다운로드",
        data=st.session_state["_pdf_bytes"],
        file_name=f"{name}_금연리포트.pdf",  # <- 파일명 변경
        mime="application/pdf",
    )
else:
    st.info("먼저 [PDF 미리 생성]을 눌러주세요.")


# st.set_page_config(page_title="상담자 전용", page_icon="🧑‍⚕️", layout="wide")
# init_state()

# st.title("🧑‍⚕️ 상담자 전용")

# if not st.session_state.get("patient"):
#     st.warning("먼저 '환자 정보 입력' 페이지에서 정보를 저장하세요.")
#     st.button("👉 환자 정보 입력으로 이동", on_click=go, args=(NAV_INPUT,))
#     st.stop()

# patient = st.session_state["patient"]
# name = patient["이름"]

# col1, col2 = st.columns([3, 1])
# with col1:
#     st.subheader(f"👤 환자: {name}  |  📅 {patient.get('날짜','-')}")
# with col2:
#     selected = st.selectbox("다른 환자 보기(데모)", ["(선택 안 함)"] + list(patient_data_all.keys()))
#     if st.button("열기") and selected != "(선택 안 함)":
#         p = patient_data_all[selected]
#         st.session_state["patient"] = {"이름": selected, "날짜": patient.get("날짜",""), **p}
#         st.experimental_rerun()

# # 비교 테이블
# p = st.session_state["patient"]
# df_compare = pd.DataFrame({
#     "특성": success_avg["특성"],
#     "금연 성공자 평균": success_avg["평균값"],
#     "해당 환자": [p["수면시간"], p["아침식사"], p["운동빈도"], p["스트레스"]],
# })

# st.write("### 📊 금연 성공자 평균 vs 환자 데이터")
# bar_compare(df_compare, "특성", ["금연 성공자 평균", "해당 환자"], y_label="값")

# # 개선 코멘트
# st.write("### 💬 개선 코멘트")
# comments = []
# for _, row in df_compare.iterrows():
#     if row["해당 환자"] < row["금연 성공자 평균"]:
#         diff = row["금연 성공자 평균"] - row["해당 환자"]
#         comments.append(f"- {row['특성']}이 평균보다 {diff:.1f}만큼 낮습니다. 개선이 필요합니다.")
# if comments:
#     for c in comments:
#         st.write(c)
# else:
#     st.success("모든 항목이 평균 이상입니다!")

# # 과거 비교(예시)
# with st.expander("📈 과거 데이터 비교 보기"):
#     past_data = {'수면시간': 6, '아침식사': 1, '운동빈도': 3, '스트레스': 4}
#     df_past = pd.DataFrame({
#         '특성': success_avg['특성'],
#         '이번 방문': [p['수면시간'], p['아침식사'], p['운동빈도'], p['스트레스']],
#         '지난 방문': [past_data['수면시간'], past_data['아침식사'], past_data['운동빈도'], past_data['스트레스']]
#     })
#     bar_compare(df_past, "특성", ["이번 방문", "지난 방문"], y_label="값")

# # PDF
# st.write("---")
# st.write("### 📄 리포트 저장")
# if st.button("PDF 미리 생성"):
#     st.session_state["_pdf_bytes"] = build_pdf_bytes(name, comments)
#     st.success("PDF가 생성되었습니다. 아래 버튼으로 다운로드하세요.")

# if st.session_state.get("_pdf_bytes"):
#     st.download_button(
#         label="⬇️ PDF 다운로드",
#         data=st.session_state["_pdf_bytes"],
#         file_name=f"{name}_report.pdf",
#         mime="application/pdf",
#     )
# else:
#     st.info("먼저 [PDF 미리 생성]을 눌러주세요.")
