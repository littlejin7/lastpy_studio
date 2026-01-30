import streamlit as st
import os
import sys
from dotenv import load_dotenv
from tavily import TavilyClient

# [경로 설정] modules, utils, ui 폴더를 인식시키기 위함
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# [모듈 불러오기] 분리된 ui 모듈과 기존 로직 모듈들
from ui import styles, sidebar, components
from modules import prompts, trans, search, draft, seo

# --------------------------------------------------------------------------
# 1. 초기 설정 (디자인 & API)
# --------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

# 페이지 기본 설정
st.set_page_config(page_title="Last.py Studio", page_icon="⚡", layout="wide")

# [ui/styles.py]에서 정의한 CSS 적용
styles.apply_custom_css()

# --------------------------------------------------------------------------
# 2. 사이드바 렌더링 (ui/sidebar.py)
# --------------------------------------------------------------------------
# 사이드바를 호출하고 사용자가 선택한 페르소나 키를 받아옵니다.
selected_persona_key = sidebar.render_sidebar()

# --------------------------------------------------------------------------
# 3. 메인 화면 구성
# --------------------------------------------------------------------------
st.markdown("""
    <div class="playful-container">
        <h1 style="font-size: 3rem; margin: 0;">YouTube Shorts Script Generator</h1>
        <p style="font-size: 1.1rem; font-weight: 700; color: #92400e;">AI Script & SEO Analyzer v3.0.0</p>
    </div>
""", unsafe_allow_html=True)

# 입력 필드 레이아웃
col1, col2 = st.columns([1, 2.5])

with col1:
    selected_topic = st.selectbox("카테고리 선택", options=list(prompts.TOPIC_CONFIG.keys()))

with col2:
    placeholder_text = prompts.TOPIC_CONFIG[selected_topic]["placeholder"]
    question_ko = st.text_input("주제 입력", placeholder=placeholder_text, label_visibility="hidden")

# 버튼 레이아웃 (카테고리 박스 폭에 맞춤)
btn_col1, btn_col2 = st.columns([1, 2.5])
with btn_col1:
    start_trigger = st.button("✨ Generate")

# --------------------------------------------------------------------------
# 4. 실행 프로세스
# --------------------------------------------------------------------------
if start_trigger:
    if not question_ko.strip():
        st.warning(f"{selected_topic} 관련 주제를 입력해주세요!")
    elif not api_key:
        st.error("🔑 .env 파일을 확인해주세요 (API Key 없음)")
    else:
        try:
            tavily_client = TavilyClient(api_key=api_key)

            with st.spinner("🔍 분석 중..."):
                translation = trans.run(question_ko)

            with st.spinner("🌍 트렌드 검색 중..."):
                trend_data = search.run(tavily_client, selected_topic, question_ko, translation)

            with st.spinner("✍️ 대본 작성 중..."):
                final_script = draft.run(selected_persona_key, trend_data, question_ko)

            with st.spinner("📊 SEO 분석 중..."):
                seo_result = seo.run(final_script)

            # 세션 상태 업데이트
            st.session_state.update({
                "generated": True, 
                "script": final_script, 
                "seo_result": seo_result, 
                "trends": trend_data
            })
            st.balloons()

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# --------------------------------------------------------------------------
# 5. 결과 출력 구역
# --------------------------------------------------------------------------
if st.session_state.get("generated"):
    tab1, tab2, tab3 = st.tabs(["📝 스크립트", "📊 SEO 점수", "📈 트렌드 분석"])
    
    with tab1:
        # [ui/components.py] 복사/다운로드 커스텀 버튼 렌더링
        components.render_action_buttons(st.session_state["script"])
        
        # 스크립트 출력 박스
        st.markdown(
            f'<div class="result-box" style="margin-top: 0;">{st.session_state["script"]}</div>', 
            unsafe_allow_html=True
        )

    with tab2:
        st.markdown(st.session_state["seo_result"])

    with tab3:
        st.info(st.session_state["trends"])

# 하단 푸터
st.markdown('<div style="text-align: center; padding: 2rem; opacity: 0.5;">© 2026 LAST.PY_STUDIO</div>', unsafe_allow_html=True)