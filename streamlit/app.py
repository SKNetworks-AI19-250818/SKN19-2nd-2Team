# app.py
import streamlit as st

st.set_page_config(page_title="금연 클리닉 상담 지원", layout="wide")

# ✅ 신/구 버전 모두 지원하는 쿼리 파라미터 처리
params = st.query_params if hasattr(st, "query_params") else st.experimental_get_query_params()
goto = params.get("goto", "" if isinstance(params, dict) else [""])
if isinstance(goto, list):
    goto = goto[0] if goto else ""

if goto == "input":
    st.switch_page("pages/01_환자_정보_입력.py")

def render_scroll_hero():
    import streamlit.components.v1 as components
    components.html(r"""
    <div id="hero-wrapper">
      <div id="hero">
        <div class="copy">
          <p class="l1">담배 끊기, 혼자선 어렵지만 함께라면 가능합니다.</p>
          <p class="l2">당신의 폐가 미소 짓는 날, 그 여정을 함께합니다.</p>
          <!-- ✅ JS 없이 최상위로 이동 -->
          <a class="cta" href="/?goto=input" target="_top">지금 시작하기</a>
        </div>
      </div>
      <div style="height: 150vh;"></div>
    </div>

    <style>
      :root{ --primary:#78D8A5; --ink:#334155; --muted:#64748B; --bg:linear-gradient(180deg,#EAF8F0 0%,#FFFFFF 100%); }
      #hero-wrapper{position:relative;width:100%}
      #hero{position:sticky;top:0;height:100vh;display:flex;align-items:center;justify-content:center;background:var(--bg);
            border-radius:20px;box-shadow:0 8px 30px rgba(0,0,0,.04);overflow:hidden}
      #hero .copy{text-align:center;transform:scale(1);opacity:.8}
      .l1{margin:0 0 8px 0;font-weight:800;font-size:2rem;color:var(--ink)}
      .l2{margin:0 0 18px 0;font-size:1.1rem;color:var(--muted)}
      .cta{display:inline-block;padding:12px 18px;border-radius:12px;background:var(--primary);color:white;
           font-weight:700;text-decoration:none;box-shadow:0 6px 18px rgba(120,216,165,.35);transition:transform .15s ease}
      .cta:hover{transform:translateY(-1px)}
      @media (min-width:1100px){ .l1{font-size:2.2rem} .l2{font-size:1.2rem} }
    </style>
    """, height=820, scrolling=True)

render_scroll_hero()

# if st.button("지금 시작하기 (대체 버튼)"):
#     st.switch_page("pages/01_환자_정보_입력.py")

# 디버그용(원하면 숨기셔도 됨)
# with st.expander("상태(디버그)"):
#     st.json({k: v for k, v in st.session_state.items() if k in ["nav", "patient"]})

#=========================

# import streamlit as st
# from streamlit.components.v1 import html   # 👈 추가
# from utils.state import init_state, NAV_HOME, NAV_INPUT, NAV_COUNSELOR
# from utils.theme import inject_theme

# # ----------------------------
# # 홈 화면 (app.py)
# # ----------------------------
# st.set_page_config(page_title="금연 클리닉 상담 지원", layout="wide")

# # st.markdown("""
# # <div style="text-align:center; padding:80px 0; background:linear-gradient(180deg,#EAF8F0 0%,#FFFFFF 100%);
# #             border-radius:16px;">
# #     <h1 style="color:#334155;">담배 끊기, 혼자선 어렵지만 함께라면 가능합니다.</h1>
# #     <p style="color:#64748B;">당신의 폐가 미소 짓는 날, 그 여정을 함께합니다.</p>
# # </div>
# # """, unsafe_allow_html=True)

# if st.query_params.get("goto") == "input":
#     try:
#         st.switch_page("pages/01_환자_정보_입력.py")
#     except Exception:
#         pass


# # st.title("금연 클리닉 상담 지원")
# # st.caption("사이드바에서 페이지를 선택하세요. 기본 순서: 환자 정보 입력 → 상담자 전용")

# # ===== 스크롤 히어로 섹션 =====
# def render_scroll_hero():
#     import streamlit.components.v1 as components
#     components.html(r"""
#     <div id="hero-wrapper">
#       <div id="hero">
#         <div class="copy">
#           <p class="l1">담배 끊기, 혼자선 어렵지만 함께라면 가능합니다.</p>
#           <p class="l2">당신의 폐가 미소 짓는 날, 그 여정을 함께합니다.</p>
#           <!-- ✅ CTA 버튼 (링크형) -->
#           <a class="cta" href="?page=%ED%99%98%EC%9E%90%20%EC%A0%95%EB%B3%B4%20%EC%9E%85%EB%A0%A5">지금 시작하기</a>
#         </div>
#       </div>
#       <div style="height: 150vh;"></div>
#     </div>

#     <style>
#       :root{
#         --primary:#78D8A5; --ink:#334155; --muted:#64748B; --bg:linear-gradient(180deg,#EAF8F0 0%,#FFFFFF 100%);
#       }
#       #hero-wrapper{position:relative;width:100%}
#       #hero{position:sticky;top:0;height:100vh;display:flex;align-items:center;justify-content:center;background:var(--bg);
#             border-radius:20px;box-shadow:0 8px 30px rgba(0,0,0,.04);overflow:hidden}
#       #hero .copy{text-align:center;transform:scale(1);opacity:.8}
#       .l1{margin:0 0 8px 0;font-weight:800;font-size:2rem;color:var(--ink)}
#       .l2{margin:0 0 18px 0;font-size:1.1rem;color:var(--muted)}
#       /* ✅ 버튼 스타일 */
#       .cta{display:inline-block;padding:12px 18px;border-radius:12px;background:var(--primary);color:white;
#            font-weight:700;text-decoration:none;box-shadow:0 6px 18px rgba(120,216,165,.35);transition:transform .15s ease}
#       .cta:hover{transform:translateY(-1px)}
#       @media (min-width:1100px){ .l1{font-size:2.2rem} .l2{font-size:1.2rem} }
#     </style>

#     <script>
#       (function(){
#         const copy=document.querySelector('#hero .copy');
#         const cta=document.querySelector('.cta');
#         const clamp=(v,a,b)=>Math.max(a,Math.min(b,v));
#         function onScroll(){
#           const y=(window.parent&&window.parent!==window?window.parent.scrollY:window.scrollY)||0;
#           const t=clamp(y/500,0,1);                    // 0~500px에서 변화
#           const s=1 + 0.5*t;                          // 1.00 → 1.5
#           const o=0.8 + 0.2*t;                         // 0.80 → 1.00
#           copy.style.transform=`scale(${s})`;
#           copy.style.opacity=o.toFixed(2);
#           // 버튼도 살짝 함께 확대
#           cta.style.transform=`scale(${1+0.05*t})`;
#           requestAnimationFrame(onScroll);
#         }
#         requestAnimationFrame(onScroll);
#       })();
#     </script>
#     """, height=820, scrolling=True)




# render_scroll_hero()
# # ===== 스크롤 히어로 끝 =====

# with st.expander("상태(디버그)"):
#     st.json({k: v for k, v in st.session_state.items() if k in ["nav","patient"]})
