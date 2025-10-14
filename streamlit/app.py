import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF

# -----------------------------
# 0️⃣ 예시용 데이터
# -----------------------------
# 금연 성공자 평균 데이터 (예시)
success_avg = pd.DataFrame({
    '특성': ['수면시간', '아침식사', '운동빈도', '스트레스'],
    '평균값': [7, 1, 4, 3]
})

# 환자 데이터 (예시)
patient_data_all = {
    '홍길동': {'수면시간': 5, '아침식사': 0, '운동빈도': 2, '스트레스': 5},
    '김철수': {'수면시간': 6, '아침식사': 1, '운동빈도': 3, '스트레스': 4}
}

# -----------------------------
# 1️⃣ 홈 화면
# -----------------------------
st.title("🚭 금연 클리닉 상담 지원 시스템")

page = st.sidebar.radio("메뉴 선택", ["홈", "환자 정보 입력", "상담자 전용"])

if page == "홈":
    st.subheader("금연 희망자 맞춤형 분석 서비스")
    st.write("금연 클리닉 상담사를 위한 데이터 기반 상담 보조 도구입니다.")
    if st.button("👉 환자 정보 입력하러 가기"):
        st.session_state['page'] = "환자 정보 입력"

# -----------------------------
# 2️⃣ 환자 정보 입력
# -----------------------------
elif page == "환자 정보 입력":
    st.subheader("🧾 환자 정보 입력")

    name = st.text_input("환자 이름")
    date = st.date_input("상담 날짜")

    st.write("### 환자 특성 입력")
    sleep = st.number_input("수면 시간 (시간)", 0, 12, 7)
    breakfast = st.selectbox("아침식사 여부", ["예", "아니오"])
    exercise = st.slider("운동 빈도 (주당 횟수)", 0, 7, 3)
    stress = st.slider("스트레스 수준 (1~5)", 1, 5, 3)

    st.write("---")
    password = st.text_input("상담자 비밀번호 입력", type="password")

    if st.button("🔒 상담자 전용 화면으로 이동"):
        if password == "clinic123":  # 예시용 비밀번호
            st.session_state['patient'] = {
                '이름': name,
                '날짜': str(date),
                '수면시간': sleep,
                '아침식사': 1 if breakfast == "예" else 0,
                '운동빈도': exercise,
                '스트레스': stress
            }
            st.session_state['page'] = "상담자 전용"
            st.success("접근 승인되었습니다.")
        else:
            st.error("비밀번호가 올바르지 않습니다.")

# -----------------------------
# 3️⃣ 상담자 전용 화면
# -----------------------------
elif page == "상담자 전용":
    if 'patient' not in st.session_state:
        st.warning("먼저 환자 정보를 입력해주세요.")
    else:
        patient = st.session_state['patient']
        name = patient['이름']

        # 헤더
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"👤 환자: {name}")
        with col2:
            selected_patient = st.selectbox("다른 환자 보기", list(patient_data_all.keys()))
            if st.button("열기"):
                patient = patient_data_all[selected_patient]
                name = selected_patient

        # 비교 데이터프레임 생성
        df_compare = pd.DataFrame({
            '특성': success_avg['특성'],
            '금연 성공자 평균': success_avg['평균값'],
            '해당 환자': [
                patient['수면시간'],
                patient['아침식사'],
                patient['운동빈도'],
                patient['스트레스']
            ]
        })

        # 그래프
        st.write("### 📊 금연 성공자 평균 vs 환자 데이터 비교")
        fig, ax = plt.subplots()
        df_compare.plot(x='특성', kind='bar', ax=ax)
        st.pyplot(fig)

        # 개선 코멘트
        st.write("### 💬 개선 코멘트")
        comments = []
        for i, row in df_compare.iterrows():
            if row['해당 환자'] < row['금연 성공자 평균']:
                diff = row['금연 성공자 평균'] - row['해당 환자']
                comments.append(f"- **{row['특성']}**이 평균보다 {diff:.1f}만큼 낮습니다. 개선이 필요합니다.")
        if comments:
            for c in comments:
                st.write(c)
        else:
            st.success("모든 항목이 평균 이상입니다!")

        # 재방문 환자 비교 (사이드 패널)
        with st.expander("📈 과거 데이터 비교 보기"):
            past_data = {'수면시간': 6, '아침식사': 1, '운동빈도': 3, '스트레스': 4}  # 예시
            df_past = pd.DataFrame({
                '특성': success_avg['특성'],
                '이번 방문': [
                    patient['수면시간'],
                    patient['아침식사'],
                    patient['운동빈도'],
                    patient['스트레스']
                ],
                '지난 방문': [
                    past_data['수면시간'],
                    past_data['아침식사'],
                    past_data['운동빈도'],
                    past_data['스트레스']
                ]
            })
            fig2, ax2 = plt.subplots()
            df_past.plot(x='특성', kind='bar', ax=ax2)
            st.pyplot(fig2)

        # PDF 저장 버튼
        if st.button("📄 PDF로 저장"):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"금연 상담 리포트 - {name}", ln=True)
            for c in comments:
                pdf.cell(200, 10, txt=c, ln=True)
            pdf.output(f"{name}_report.pdf")
            st.success(f"{name}_report.pdf 파일이 저장되었습니다.")
