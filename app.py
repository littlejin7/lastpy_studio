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

# 환경 변수 및 API 키 설정
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

# 페이지 설정
st.set_page_config(page_title="Last.py Studio", page_icon="⚡", layout="wide")

# CSS 및 사이드바 적용 (버튼 CSS 등이 styles.py로 통합됨)
styles.apply_custom_css()
selected_persona_key = sidebar.render_sidebar()

# 세션 상태 초기화
if "script" not in st.session_state: st.session_state["script"] = ""
if "titles" not in st.session_state: st.session_state["titles"] = []
if "translation" not in st.session_state: st.session_state["translation"] = ""

# --- [상단] 메인 타이틀 (components.py로 모듈화 가능) ---
components.render_main_header()

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
            st.session_state["translation"] = translation 
            
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
    
    # AI 분석 실행 및 실제 점수 획득 (modules/seo.py에서 한글 번역 및 점수 추출 처리)
    with st.spinner("AI가 SEO 지표를 정밀 분석 중입니다..."):
        analysis_report, actual_score, actual_rewatch = seo.run(st.session_state["script"])

    # 추출된 실제 점수를 딕셔너리에 담아 컴포넌트로 전달
    seo_display_data = {
        "score": actual_score,    
        "volume": "High",         
        "rewatch": actual_rewatch 
    }

    # 워크스페이스 렌더링 (내부에 SEO 대시보드와 Editor가 순서대로 배치됨)
    updated_content = components.render_action_buttons(
        st.session_state["script"], 
        seo_data=seo_display_data
    )
    
    if updated_content:
        st.session_state["script"] = updated_content

    # 상세 분석 리포트 전문 확인 (한글화된 텍스트 리포트)
    with st.expander("🔍 상세 SEO 분석 리포트 전문 확인"):
        st.markdown(analysis_report)
    
    st.markdown("---")

# 푸터
st.markdown('<div style="text-align: center; padding: 2rem; opacity: 0.3;">© 2026 LAST.PY_STUDIO</div>', unsafe_allow_html=True)