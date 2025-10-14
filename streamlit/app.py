import streamlit as st
from streamlit.components.v1 import html   # 👈 추가
from utils.state import init_state, NAV_HOME, NAV_INPUT, NAV_COUNSELOR
from utils.theme import inject_theme

st.set_page_config(page_title="금연 클리닉 상담 지원", layout="wide")
init_state()
inject_theme()

# 전역 스크롤바를 눈에만 안 보이게 숨김 (스크롤 기능은 유지)
st.markdown(
    """
    <style>
    html, body { scrollbar-width: none; -ms-overflow-style: none; }
    html::-webkit-scrollbar, body::-webkit-scrollbar { display: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

if st.query_params.get("goto") == "input":
    try:
        st.switch_page("pages/01_고객_정보_입력.py")
    except Exception:
        pass

st.title("금연 클리닉 상담 지원")
st.caption("사이드바에서 페이지를 선택하세요. 기본 순서: 고객 정보 입력 → 상담자 전용")

# ===== 스크롤 히어로 섹션 =====
def render_scroll_hero():
    # 전역 CSS 스타일 (가장 먼저 적용)
    st.markdown("""
    <style>
    /* 텍스트 페이드 + 확대 애니메이션 (JS 불필요) */
    @keyframes heroFadeZoom {
      to { opacity: 1; transform: scale(1.05); }
    }
    .hero-animated {
      opacity: 0;            /* 시작은 보이지 않음 */
      transform: scale(0.95);
      animation: heroFadeZoom 2.5s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
      animation-delay: .35s; /* 약간 지연 후 시작 */
    }

    /* Streamlit 기본 버튼을 안전하게 타겟팅 + 중앙 정렬 */
    /* CTA 래퍼 기준으로 완전 중앙 정렬 */
    #cta-wrap { display:grid; place-items:center; width:100% !important; }
    #cta-wrap div.stButton { width:auto !important; margin:20px 0 !important; }
    /* 컨테이너 자체를 가운데 정렬 (래퍼 없이도 동작) */
    div.stButton { display:block !important; width:max-content !important; margin:20px auto !important; }
    div.stButton > button {
      background: #78D8A5 !important;
      color: #FFFFFF !important;
      font-weight: 700 !important;
      padding: 12px 18px !important;
      border-radius: 12px !important;
      box-shadow: 0 6px 18px rgba(120,216,165,0.35) !important;
      border: none !important;
      font-size: 16px !important;
      transition: all .3s ease !important;
      opacity: 0;                 /* 텍스트보다 늦게, 살며시 */
      transform: scale(0.98);
      animation: heroFadeZoom 1.8s ease forwards;
      animation-delay: .9s;       /* 텍스트가 다 나타난 뒤 천천히 */
    }
    div.stButton > button:hover {
      background: #6BC494 !important;
      transform: translateY(-2px);
      box-shadow: 0 8px 25px rgba(120,216,165,0.5) !important;
    }

    @media (min-width: 1100px) {
      .hero-title { font-size: 2.1rem !important; }
      .hero-subtitle { font-size: 1.15rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 히어로 섹션
    st.markdown("""
    <div style="
        background: linear-gradient(180deg, #EAF8F0 0%, #FFFFFF 100%);
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.04);
        padding: 60px 40px;
        text-align: center;
        margin: 20px 0;
    ">
        <h1 class="hero-animated hero-title" style="
            font-size: 1.9rem;
            font-weight: 800;
            color: #334155;
            margin: 0 0 8px 0;
        ">담배 끊기, 혼자선 어렵지만 함께라면 가능합니다.</h1>
        <p class="hero-animated hero-subtitle" style="
            font-size: 1.05rem;
            color: #64748B;
            margin: 0 0 18px 0;
        ">당신의 폐가 미소 짓는 날, 그 여정을 함께합니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # 버튼 (래퍼로 확실한 중앙 정렬)
    st.markdown('<div id="cta-wrap">', unsafe_allow_html=True)
    if st.button("지금 시작하기", key="hero_cta"):
        st.switch_page("pages/01_고객_정보_입력.py")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # (JS 불필요) 키프레임 애니메이션으로만 처리

    # 백업: 컴포넌트가 차단되거나 브라우저가 링크를 무시할 경우 대비한 네이티브 버튼
    # 버튼 클릭 시 쿼리파라미터를 통해 메인에서 switch_page 수행
    




render_scroll_hero()
# ===== 스크롤 히어로 끝 =====

# iframe 관련 코드 제거 (더 이상 필요 없음)

# with st.expander("상태(디버그)"):
#     st.json({k: v for k, v in st.session_state.items() if k in ["nav","patient"]})
