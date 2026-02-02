import streamlit as st
import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from tavily import TavilyClient 
import ollama

# 현재 디렉토리를 경로에 추가하여 modules를 찾을 수 있게 함
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# UI 모듈 및 핵심 로직 임포트
try:
    from modules.ui import styles, sidebar, components
    from modules import prompts, trans, search, draft, seo, prompts_kr
    from utils import seo_tools
except ImportError:
    from modules.ui import styles, sidebar, components
    import modules.prompts as prompts
    import modules.trans as trans
    import modules.search as search
    import modules.draft as draft
    import modules.seo as seo
    import modules.prompts_kr as prompts_kr
    from utils import seo_tools

load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

st.set_page_config(page_title="Last.py Studio", page_icon="⚡", layout="wide")

# CSS 및 사이드바 적용
styles.apply_custom_css()
selected_persona_key = sidebar.render_sidebar()

# --- [UI 개선] Generate 버튼 전용 CSS ---
st.markdown("""
    <style>
    div.stButton > button {
        height: 42px !important;
        min-height: 42px !important;
        line-height: 42px !important;
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        font-size: 0.95rem !important;
        margin-top: 1px !important;
    }
    div[data-testid="column"] { display: flex; align-items: center; }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "script" not in st.session_state: st.session_state["script"] = ""
if "titles" not in st.session_state: st.session_state["titles"] = []
if "translation" not in st.session_state: st.session_state["translation"] = ""

# --- [상단] 메인 타이틀 ---
st.markdown("""
    <div class="playful-container">
        <h1 style="font-size: 3rem; margin: 0;">YouTube Shorts Script Generator</h1>
        <p style="font-size: 1.1rem; font-weight: 700; color: #92400e;">AI Script & SEO Analyzer v3.0.0</p>
    </div>
""", unsafe_allow_html=True)

# --- [중단] 입력칸 + 버튼 섹션 ---
input_col, btn_col = st.columns([4, 1])
with input_col:
    cat_col, text_col = st.columns([1, 2])
    with cat_col:
        selected_topic = st.selectbox("카테고리", options=list(prompts.TOPIC_CONFIG.keys()), label_visibility="collapsed")
    with text_col:
        placeholder_text = prompts.TOPIC_CONFIG[selected_topic]["placeholder"]
        question_ko = st.text_input("주제 입력", placeholder=placeholder_text, key="input_topic", label_visibility="collapsed")

with btn_col:
    start_trigger = st.button("✨ Generate", type="primary", use_container_width=True)

# 1단계: 분석 및 제목 생성
if start_trigger:
    if not question_ko.strip():
        st.warning("주제를 입력해주세요!")
    else:
        with st.spinner(":mag: 분석 및 제목 생성 중..."):
            tavily_client = TavilyClient(api_key=api_key)
            translation = trans.run(question_ko)
            st.session_state["translation"] = translation # 다운로드 도구용 저장
            
            trend_data = search.run(tavily_client, selected_topic, question_ko, translation)
            titles_en = draft.generate_titles(selected_persona_key, trend_data, question_ko)
            titles_ko = draft.translate_hooks_to_korean(titles_en)

            st.session_state["titles"] = titles_ko
            st.session_state["title_map"] = dict(zip(titles_ko, titles_en))
            st.session_state["trends"] = trend_data

# 제목 선택 UI
selected_titles = components.render_title_selector(st.session_state.get("titles"))

# 2단계: 스크립트 생성
if selected_titles:
    titles_en_selected = [st.session_state["title_map"][t] for t in selected_titles]
    with st.spinner("✍️ 1단계: 초안 작성 중..."):
        draft_script_en = draft.generate_script(selected_persona_key, titles_en_selected, st.session_state["trends"])

    with st.spinner("🇰🇷 2단계: 한국어 패치 중..."):
        korean_prompt = prompts_kr.get_translation_prompt(selected_persona_key, draft_script_en)
        res = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": korean_prompt}])
        st.session_state["script"] = res["message"]["content"]
        st.rerun()

# --- [하단] 통합 워크스페이스 ---
if st.session_state["script"]:
    st.markdown("---")
    
    # 1. 편집기 (components.py 내부에서 복사 버튼 렌더링 포함)
    updated_content = components.render_action_buttons(st.session_state["script"])
    if updated_content:
        st.session_state["script"] = updated_content

    # 2. SEO 분석 섹션 (중복 제목 제거)
    with st.spinner("AI가 SEO 지표를 정밀 분석 중입니다..."):
        # seo.run()이 반환하는 결과 내부에 이미 "## 📊 SEO Score Analysis" 헤더가 포함되어 있습니다.
        analysis_report = seo.run(st.session_state["script"])
        st.markdown(analysis_report)
    
    st.markdown("---")

    
st.markdown('<div style="text-align: center; padding: 2rem; opacity: 0.3;">© 2026 LAST.PY_STUDIO</div>', unsafe_allow_html=True)