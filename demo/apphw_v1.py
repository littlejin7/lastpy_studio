import streamlit as st
from tavily import TavilyClient
import ollama
import os
from dotenv import load_dotenv
import seo_analyzer
from datetime import datetime

# --------------------------------------------------------------------------
# 1. 초기 설정
# --------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

if not api_key:
    st.error("TAVILY_API_KEY가 설정되지 않았습니다. .env 파일을 확인해주세요.")
    st.stop()

tavily_client = TavilyClient(api_key=api_key)

# --------------------------------------------------------------------------
# 2. 데이터 및 템플릿 설정
# --------------------------------------------------------------------------
persona_prompts = {
    "1020 (도파민/비주얼)": """
        - **Role**: Hyperactive Gen-Z Creator.
        - **Tone**: Chaotic, Loud, High-Pitch. Use exclamation marks!!!
        - **Structure**: Start with a scream or visual fail. Cut every 0.5 seconds.
    """,
    "3040 (핵심요약/효율)": """
        - **Role**: Smart Efficiency Expert.
        - **Tone**: Professional, Sharp, slightly Cynical but helpful.
        - **Structure**: [0s] Conclusion -> [Body] 3 Reasons -> [End] Verdict.
    """,
    "5060 (연륜/솔직함)": """
        - **Role**: Brutally Honest K-Uncle/Auntie.
        - **Tone**: Loud, Rough, but Warm. "Trust me, I know better."
        - **Structure**: Loud entrance -> Eating/Trying -> Honest reaction -> Recommendation.
    """,
}

# 주제별 검색 쿼리 및 플레이스홀더 설정
topic_config = {
    "Food": {
        "placeholder": "K-Food 주제를 입력하세요 (예: 두바이 초콜릿, 탕후루...)",
        "query_template": "Korean trend {q} viral food dessert reaction {t}"
    },
    "K-pop": {
        "placeholder": "K-pop 주제를 입력하세요 (예: NewJeans 하입보이 챌린지...)",
        "query_template": "Korean K-pop trend {q} viral choreography challenge reaction {t}"
    },
    "K-Beauty": {
        "placeholder": "K-Beauty 주제를 입력하세요 (예: 가히 멀티밤 활용법...)",
        "query_template": "Korean beauty skincare trend {q} viral product hack reaction {t}"
    }
}

# --------------------------------------------------------------------------
# 3. 디자인 (CSS)
# --------------------------------------------------------------------------
st.set_page_config(page_title="Last.py Studio", page_icon="⚡", layout="wide")

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=Nunito:wght@400;600;700;800&display=swap');

    .stApp {
        background: linear-gradient(135deg, #facc15 0%, #fbbf24 100%);
        font-family: 'Nunito', sans-serif;
    }

    .playful-container {
        background-color: #fefce8;
        border-radius: 2rem;
        padding: 2.5rem;
        border: 1px solid white;
        box-shadow: 0 8px 0 rgba(0,0,0,0.05), 0 20px 25px -5px rgba(0,0,0,0.1);
        color: #451a03;
        margin-bottom: 2rem;
    }

    h1, h2, h3, .playful-font {
        font-family: 'Fredoka', sans-serif !important;
        font-weight: 900 !important;
    }

    .stButton>button {
        background-color: #4ade80 !important;
        color: white !important;
        border-radius: 9999px !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        font-weight: 900 !important;
        box-shadow: 0 4px 0 #166534 !important;
        transition: all 0.2s;
        text-transform: uppercase;
        width: 100%;
        font-family: 'Fredoka', sans-serif !important;
    }
    
    .result-box {
        background: #fffbeb;
        padding: 1.5rem; 
        border-radius: 1rem; 
        border-left: 5px solid #ef4444;
        margin-top: 1rem;
        white-space: pre-wrap;
        line-height: 1.6;
    }
    
    /* 입력창 둥글게 디자인 */
    .stTextInput input {
        border-radius: 1rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------------------------------
# 4. 사이드바
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div style="text-align: center; padding: 1rem 0;">
            <div style="background: #ef4444; width: 60px; height: 60px; border-radius: 1.5rem; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;">
                <span style="color: white; font-size: 2rem;">⚡</span>
            </div>
            <h2 style="margin: 0; color: #451a03;">last.py_studio</h2>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    selected_persona_key = st.radio("페르소나 설정", list(persona_prompts.keys()), index=1)

# --------------------------------------------------------------------------
# 5. 메인 화면 (입력 및 실행)
# --------------------------------------------------------------------------
st.markdown("""
    <div class="playful-container">
        <h1 style="font-size: 3rem; margin: 0;">YouTube Shorts Script Generator</h1>
        <p style="font-size: 1.1rem; font-weight: 700; color: #92400e;">AI Script & SEO Analyzer v3.0.0</p>
    </div>
""", unsafe_allow_html=True)

# [요청사항] 카테고리 선택과 주제 입력창 가로 배치
col1, col2 = st.columns([1, 2.5])

with col1:
    selected_topic = st.selectbox("카테고리 선택", options=list(topic_config.keys()))

with col2:
    current_placeholder = topic_config[selected_topic]["placeholder"]
    question_ko = st.text_input("주제 입력", placeholder=current_placeholder)

if st.button("✨ 스크립트 생성 및 분석 (Generate)"):
    if not question_ko.strip():
        st.warning(f"{selected_topic} 관련 주제를 입력해주세요!")
    else:
        try:
            # 1. 트렌드 분석 및 쿼리 생성
            with st.spinner("🔍 분석 중..."):
                translate_prompt = f"Generate English search keywords for '{question_ko}'. Output: keywords only."
                translation = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": translate_prompt}])["message"]["content"]

                # 동적 쿼리 조합
                raw_template = topic_config[selected_topic]["query_template"]
                tavily_query = raw_template.format(q=question_ko, t=translation)[:350]

                search_result = tavily_client.search(query=tavily_query, search_depth="advanced")
                raw_content = "\n\n".join([item["content"] for item in search_result.get("results", [])[:3]])

                summary_prompt = f"Summarize key facts about '{question_ko}' based on: {raw_content}"
                cleaned_trends = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": summary_prompt}])["message"]["content"]

            # 2. 스크립트 작성
            with st.spinner("✍️ 대본 작성 중..."):
                target_persona = persona_prompts[selected_persona_key]
                full_prompt = f"""
                Act as a YouTube Shorts Strategist.
                # PERSONA: {target_persona}
                # TREND INFO: {cleaned_trends}
                # TASK: Create a 'Viral Shorts Package' for "{question_ko}".
                1. Titles: 3 options. 2. Script: 60s, Time-stamped. 3. Tags: 10 hashtags in a SINGLE LINE.
                """
                final_script = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": full_prompt}])["message"]["content"]

            # 3. SEO 점수 분석 (utils 폴더의 seo_analyzer 호출)
            with st.spinner("📊 SEO 분석 중..."):
                seo_result = seo_analyzer.analyze_seo_score(final_script)

            st.session_state["generated"] = True
            st.session_state["script"] = final_script
            st.session_state["seo_result"] = seo_result
            st.session_state["trends"] = cleaned_trends
            st.balloons()

        except Exception as e:
            st.error(f"오류가 발생했습니다: {e}")

# --------------------------------------------------------------------------
# 6. 결과 탭 출력
# --------------------------------------------------------------------------
if st.session_state.get("generated"):
    tab1, tab2, tab3 = st.tabs(["📝 스크립트", "📊 SEO 점수", "📈 트렌드 분석"])
    
    with tab1:
        st.markdown(f'<div class="result-box">{st.session_state["script"]}</div>', unsafe_allow_html=True)
    with tab2:
        st.markdown(st.session_state["seo_result"])
    with tab3:
        st.info(st.session_state["trends"])

st.markdown('<div style="text-align: center; padding: 2rem; opacity: 0.5;">© 2026 LAST.PY_STUDIO</div>', unsafe_allow_html=True)