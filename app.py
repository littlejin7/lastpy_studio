import streamlit as st
import os
import sys
from dotenv import load_dotenv
from tavily import TavilyClient 
import ollama

# 현재 디렉토리를 경로에 추가하여 modules를 찾을 수 있게 함
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 프로젝트 루트 경로를 시스템 경로에 추가하여 모듈을 잘 찾게 함
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# UI 모듈들을 정확한 경로에서 가져오기
try:
    from modules.ui import styles, sidebar, components
    from modules import prompts, trans, search, draft, seo, prompts_kr
except ImportError:
    # 경로 인식이 안 될 경우를 대비한 직접 임포트
    from modules.ui import styles, sidebar, components
    import modules.prompts as prompts
    import modules.trans as trans
    import modules.search as search
    import modules.draft as draft
    import modules.seo as seo
    import modules.prompts_kr as prompts_kr

load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

st.set_page_config(page_title="Last.py Studio", page_icon="⚡", layout="wide")

# CSS 및 사이드바 적용
styles.apply_custom_css()
selected_persona_key = sidebar.render_sidebar()

# --- [UI 개선] Generate 버튼 높이 조절 전용 CSS ---
st.markdown("""
    <style>
    /* 버튼의 세로 높이를 입력창과 비슷하게 슬림하게 조정 */
    div.stButton > button {
        height: 42px !important;      /* 높이 축소 */
        min-height: 42px !important;  /* 최소 높이 강제 고정 */
        line-height: 42px !important; /* 텍스트 수직 중앙 정렬 */
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        font-size: 0.95rem !important;
        margin-top: 1px !important;    /* 미세한 위치 보정 */
    }
    
    /* 입력창과 버튼의 수직 정렬을 맞추기 위해 컬럼 정렬 수정 */
    div[data-testid="column"] {
        display: flex;
        align-items: center;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if "script" not in st.session_state: st.session_state["script"] = ""
if "titles" not in st.session_state: st.session_state["titles"] = []

# --- [상단] 메인 타이틀 ---
st.markdown("""
    <div class="playful-container">
        <h1 style="font-size: 3rem; margin: 0;">YouTube Shorts Script Generator</h1>
        <p style="font-size: 1.1rem; font-weight: 700; color: #92400e;">AI Script & SEO Analyzer v3.0.0</p>
    </div>
""", unsafe_allow_html=True)

# --- [중단] 입력칸 + 버튼 한 줄 배치 섹션 ---
input_col, btn_col = st.columns([4, 1])

with input_col:
    cat_col, text_col = st.columns([1, 2])
    with cat_col:
        selected_topic = st.selectbox("카테고리", options=list(prompts.TOPIC_CONFIG.keys()), label_visibility="collapsed")
    with text_col:
        placeholder_text = prompts.TOPIC_CONFIG[selected_topic]["placeholder"]
        question_ko = st.text_input("주제 입력", placeholder=placeholder_text, key="input_topic", label_visibility="collapsed")

with btn_col:
    # 높이가 줄어든 ✨ Generate 버튼
    start_trigger = st.button("✨ Generate", type="primary", use_container_width=True)

# 3. 로직 실행 (제목 생성)
if start_trigger:
    if not question_ko.strip():
        st.warning("주제를 입력해주세요!")
    else:
        with st.spinner(":mag: 분석 및 제목 생성 중..."):
            tavily_client = TavilyClient(api_key=api_key)
            translation = trans.run(question_ko)
            trend_data = search.run(tavily_client, selected_topic, question_ko, translation)
            
            # 영어 제목 생성
            titles_en = draft.generate_titles(selected_persona_key, trend_data, question_ko)
            # 한국어 번역
            titles_ko = draft.translate_hooks_to_korean(titles_en)

            # 세션에 한국어/영어/매핑 저장
            st.session_state["titles"] = titles_ko
            st.session_state["titles_en"] = titles_en
            st.session_state["title_map"] = dict(zip(titles_ko, titles_en))

            st.session_state["trends"] = trend_data

# --- 제목 선택 UI ---
selected_titles = components.render_title_selector(st.session_state.get("titles"))

# --- [핵심 수정] 선택된 제목으로 스크립트 생성 (2단계 방식 적용) ---
if selected_titles:
    # 한국어 제목을 영어 제목으로 다시 변환
    titles_en_selected = [st.session_state["title_map"][t] for t in selected_titles]

    # 1단계: 영어 초안 생성
    with st.spinner("✍️ 1단계: 초안 작성 중... (English Draft)"):
        draft_script_en = draft.generate_script(
            selected_persona_key,
            titles_en_selected,
            st.session_state["trends"]
        )

    # 2단계: 한국어 페르소나 이식 (prompts_kr 사용)
    with st.spinner("🇰🇷 2단계: 페르소나 이식 및 한국어 패치 중..."):
        # prompts_kr에서 강력한 오더가 담긴 프롬프트를 가져옴
        korean_prompt = prompts_kr.get_translation_prompt(selected_persona_key, draft_script_en)
        
        # AI에게 최종 실행 명령 
        res = ollama.chat(
            model="gemma3:latest",  # 사용하시는 모델명으로 꼭 확인하세요! 
            messages=[{"role": "user", "content": korean_prompt}]
        )
        final_script_ko = res["message"]["content"]

        # 결과 저장 및 리로드
        st.session_state["script"] = final_script_ko
        st.rerun()

# --- [하단] 통합 워크스페이스 ---
if st.session_state["script"]:
    st.markdown("---")
    updated_content = components.render_action_buttons(st.session_state["script"])
    
    if updated_content:
        st.session_state["script"] = updated_content

st.markdown('<div style="text-align: center; padding: 2rem; opacity: 0.3;">© 2026 LAST.PY_STUDIO</div>', unsafe_allow_html=True)