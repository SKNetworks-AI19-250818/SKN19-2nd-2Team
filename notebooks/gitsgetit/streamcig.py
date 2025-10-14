import streamlit as st
import joblib
import numpy as np

st.title("🚭 금연 성공 예측기")

# 모델 불러오기
# model = joblib.load('02_ML학습준비.ipynb')

# 입력
age = st.slider("나이", 18, 70, 30)
cigs = st.number_input("하루 흡연량(개피)", 0, 40, 10)
stress = st.slider("스트레스 정도", 1, 10, 5)
exercise = st.selectbox("운동 습관", ["없음", "가끔", "자주"])
support = st.selectbox("가족/친구의 지지", ["없음", "보통", "강함"])

# # 예측
# if st.button("결과 보기"):
#     # 입력 → 전처리 (예: one-hot 인코딩 등)
#     X_input = np.array([[age, cigs, stress, ...]])
#     prob = model.predict_proba(X_input)[0][1]
#     st.progress(prob)
#     st.write(f"당신의 금연 성공 확률은 **{prob*100:.2f}%** 입니다.")
    
#     # 조건부 피드백
#     if prob < 0.6:
#         st.warning("운동 습관을 늘리고, 사회적 지지를 활용해보세요!")
#     else:
#         st.success("금연 성공 가능성이 높아요! 꾸준히 유지하세요 💪")
