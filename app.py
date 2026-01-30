import streamlit as st
import os
import sys
import base64 #한글 인식?
import json  #json 파일 읽기
import streamlit.components.v1 as components  # <--- [중요!] 이 줄이 꼭 있어야 작동합니다! 
from dotenv import load_dotenv
from tavily import TavilyClient
from datetime import datetime

# [경로 설정] modules와 utils 폴더 인식시키기
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# [모듈 불러오기]
try:
    from modules import prompts, trans, search, draft, seo
    from utils import seo_analyzer
except ImportError as e:
    st.error(f"❌ 모듈을 찾을 수 없습니다. 폴더 위치를 확인해주세요.\n에러 내용: {e}")
    st.stop()

# --------------------------------------------------------------------------
# 1. 초기 설정 (디자인 & API)
# --------------------------------------------------------------------------
load_dotenv()
api_key = os.getenv("TAVILY_API_KEY")

# [디자인] 페이지 탭 설정 (번개 아이콘 ⚡)
st.set_page_config(page_title="Last.py Studio", page_icon="⚡", layout="wide")




# --------------------------------------------------------------------------
# [디자인] CSS 스타일 적용 (메인 버튼을 Copy 버튼 스타일로 완벽 변신!)
# --------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* 1. 폰트 및 기본 설정 */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&family=Nunito:wght@400;600;700;800&display=swap');

    .stApp {
        background: linear-gradient(135deg, #facc15 0%, #fbbf24 100%);
        font-family: 'Nunito', sans-serif;
    }

    /* 2. 메인 컨테이너 */
    .playful-container {
        background-color: #fefce8;
        border-radius: 2rem;
        padding: 2.5rem;
        border: 1px solid white;
        box-shadow: 0 8px 0 rgba(0,0,0,0.05), 0 20px 25px -5px rgba(0,0,0,0.1);
        color: #451a03;
        margin-bottom: 2rem;
    }

    /* 3. 제목 폰트 */
    h1, h2, h3, .playful-font {
        font-family: 'Fredoka', sans-serif !important;
        font-weight: 900 !important;
    }

    /* ================================================================= */
    /* 👇 [핵심] 메인 실행 버튼 (Copy 버튼 스타일 이식!) 👇 */
    /* ================================================================= */
    
    /* 4-1. 버튼 껍데기 (3D 입체 효과) */
   /* 4-1. 버튼 껍데기 (3D 입체 효과 - Copy 버튼 스타일 복제) */
    .stButton > button {
        background-color: #4ade80 !important; /* 연두색 배경 */
        color: #14532d !important;            /* 진한 녹색 글씨 */
        border-radius: 2rem !important;       /* 둥근 모서리 (2rem) */
        border: none !important;
        padding: 16px 24px !important;        /* 패딩 통일 */
        
        /* [3D 그림자] Copy 버튼과 똑같은 5px 두께 */
        box-shadow: 0 5px 0 #15803d !important; 
        
        transition: all 0.1s !important;
        width: 100%;
        height: auto !important;
        margin-top: 10px;
    }

    /* 4-2. 버튼 안의 글자 (폰트 Nunito로 변경!) */
    .stButton > button p {
        font-family: 'Nunito', sans-serif !important; /* <--- 여기가 핵심! */
        font-weight: 800 !important;          /* 아주 굵게 */
        font-size: 1.2rem !important;
        letter-spacing: 0.5px !important;
        margin-bottom: 0 !important;
    }

    /* 4-3. [클릭 효과] 쫀득하게 눌림 */
    .stButton > button:active {
        transform: translateY(5px) !important; /* 5px 아래로 */
        box-shadow: none !important;           /* 그림자 삭제 */
    }
    
    /* 4-4. 마우스 올렸을 때 */
    .stButton > button:hover {
        background-color: #86efac !important;
        color: #052e16 !important;
    }
    /* ================================================================= */

    /* 5. 입력창 높이 & 정렬 (이전 설정 유지) */
    .stSelectbox div[data-baseweb="select"] > div,
    .stTextInput div[data-baseweb="input"] {
        height: 65px !important;
        min-height: 65px !important;
        border-radius: 1rem !important;
        display: flex !important;
        align-items: center !important;
    }
    .stTextInput input {
        height: 65px !important;
        font-size: 1.2rem !important;
    }

    /* 6. 결과 박스 */
    .result-box {
        background: #fffbeb;
        padding: 1.5rem; 
        border-radius: 1rem; 
        border-left: 5px solid #ef4444;
        margin-top: 1rem;
        white-space: pre-wrap;
        line-height: 1.6;
    }

    /* 7. 기타 폰트 통일 */
    .stSelectbox label p, .stRadio label p, .stTextInput label p,
    .stRadio [data-testid="stMarkdownContainer"] p,
    .stSelectbox div[data-baseweb="select"] div,
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-family: 'Fredoka', sans-serif !important;
        font-weight: 800 !important;
        color: #451a03 !important;
    }
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: #ef4444 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# --------------------------------------------------------------------------
# 2. 사이드바 (설정 메뉴)
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
    # prompts 모듈에서 페르소나 리스트 가져오기
    selected_persona_key = st.radio("페르소나 설정", list(prompts.PERSONA_PROMPTS.keys()), index=1)

# --------------------------------------------------------------------------
# 3. 메인 화면 (UI Layout)
# --------------------------------------------------------------------------
st.markdown("""
    <div class="playful-container">
        <h1 style="font-size: 3rem; margin: 0;">YouTube Shorts Script Generator</h1>
        <p style="font-size: 1.1rem; font-weight: 700; color: #92400e;">AI Script & SEO Analyzer v3.0.0</p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2.5])

with col1:
    # prompts 모듈에서 카테고리 리스트 가져오기
    selected_topic = st.selectbox("카테고리 선택", options=list(prompts.TOPIC_CONFIG.keys()))

with col2:
    placeholder_text = prompts.TOPIC_CONFIG[selected_topic]["placeholder"]
    # [중요] label_visibility="hidden"으로 줄 맞춤
    question_ko = st.text_input("주제 입력", placeholder=placeholder_text, label_visibility="hidden")

# --------------------------------------------------------------------------
# 4. 실행 로직 (버튼을 왼쪽 카테고리 칸 크기에 맞춤)
# --------------------------------------------------------------------------
# [수정] 버튼을 위한 투명 칸을 다시 1:2.5 비율로 만듭니다.
btn_col1, btn_col2 = st.columns([1, 2.5])

# 왼쪽 칸(btn_col1)에만 버튼을 넣으면, 위쪽 '카테고리' 박스와 폭이 똑같아집니다!
with btn_col1:
    start_trigger = st.button("✨ Generate")

# 버튼이 눌렸을 때 실행 (들여쓰기 주의!)
if start_trigger:
    if not question_ko.strip():
        st.warning(f"{selected_topic} 관련 주제를 입력해주세요!")
    elif not api_key:
        st.error("🔑 .env 파일을 확인해주세요 (API Key 없음)")
    else:
        try:
            tavily_client = TavilyClient(api_key=api_key)

            # [1단계] 번역
            with st.spinner("🔍 분석 중..."):
                translation = trans.run(question_ko)

            # [2단계] 검색
            with st.spinner("🌍 트렌드 검색 중..."):
                trend_data = search.run(tavily_client, selected_topic, question_ko, translation)

            # [3단계] 대본 작성
            with st.spinner("✍️ 대본 작성 중..."):
                final_script = draft.run(selected_persona_key, trend_data, question_ko)

            # [4단계] SEO 분석
            with st.spinner("📊 SEO 분석 중..."):
                seo_result = seo.run(final_script)

            # 결과 저장
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
# 5. 결과 출력 (다운로드 & 복사 - 완벽한 3D 버튼 세트)
# --------------------------------------------------------------------------
if st.session_state.get("generated"):
    
    tab1, tab2, tab3 = st.tabs(["📝 스크립트", "📊 SEO 점수", "📈 트렌드 분석"])
    
    with tab1:
        # ------------------------------------------------------------------
        # [1] HTML/JS 코드로 버튼 2개 생성 (다운로드 + 복사)
        # ------------------------------------------------------------------
        
        # 1. 데이터 준비
        script_text = st.session_state["script"]
        file_name = f"shorts_script_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
        
        # 2. 파이썬 데이터를 HTML용으로 변환
        b64 = base64.b64encode(script_text.encode()).decode() # 다운로드용
        json_script = json.dumps(script_text)                 # 복사(JS)용
        
        # 3. HTML/CSS/JS 코드 작성
        custom_buttons_html = f"""
        <html>
        <head>
            <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,700,1,0" rel="stylesheet">
            <style>
                /* 전체 컨테이너: 우측 정렬 */
                .button-container {{
                    display: flex;
                    gap: 15px;
                    justify-content: flex-end; /* 오른쪽 정렬 */
                    padding: 5px;
                }}

                /* 공통 3D 버튼 스타일 */
                .cute-3d-button {{
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    gap: 8px;
                    font-family: 'Nunito', sans-serif;
                    font-weight: 800;
                    text-decoration: none;
                    cursor: pointer;
                    transition: all 0.1s;
                    user-select: none;
                    border: none;
                    border-radius: 2rem;
                    padding: 12px 24px; /* 크기 적당히 */
                    font-size: 16px;
                    color: white; /* 글자색 흰색 고정 */
                }}

                .cute-3d-button:active {{
                    transform: translateY(4px); /* 눌리는 효과 */
                    box-shadow: none !important;
                }}

                /* [빨강] 다운로드 버튼 */
                .btn-download {{
                    background-color: #ef4444;
                    box-shadow: 0 5px 0 #991b1b;
                }}
                .btn-download:hover {{ background-color: #f87171; }}

                /* [주황] 복사 버튼 */
                .btn-copy {{
                    background-color: #fbbf24;
                    color: #451a03 !important; /* 주황색 배경엔 진한 갈색 글씨 */
                    box-shadow: 0 5px 0 #b45309;
                }}
                .btn-copy:hover {{ background-color: #fcd34d; }}

                /* 아이콘 스타일 */
                .material-symbols-outlined {{
                    font-size: 20px;
                    vertical-align: middle;
                }}
            </style>
        </head>
        <body>
            <div class="button-container">
                <a href="data:text/plain;base64,{b64}" download="{file_name}" class="cute-3d-button btn-download">
                    <span class="material-symbols-outlined">download</span>
                    DOWNLOAD
                </a>

                <button onclick="copyToClipboard()" class="cute-3d-button btn-copy" id="copyBtn">
                    <span class="material-symbols-outlined">content_copy</span>
                    COPY TEXT
                </button>
            </div>

            <script>
                function copyToClipboard() {{
                    // 파이썬에서 넘겨준 텍스트를 받음
                    const textToCopy = {json_script};
                    
                    navigator.clipboard.writeText(textToCopy).then(() => {{
                        // 성공 시 버튼 모양 변경
                        const btn = document.getElementById("copyBtn");
                        const originalHTML = btn.innerHTML;
                        
                        btn.innerHTML = '<span class="material-symbols-outlined">check</span> COPIED!';
                        btn.style.backgroundColor = "#4ade80"; // 초록색으로 잠시 변경
                        btn.style.color = "white";
                        btn.style.boxShadow = "0 5px 0 #15803d";
                        
                        // 2초 뒤 원상복구
                        setTimeout(() => {{
                            btn.innerHTML = originalHTML;
                            btn.style.backgroundColor = ""; 
                            btn.style.color = "";
                            btn.style.boxShadow = "";
                        }}, 2000);
                    }}).catch(err => {{
                        console.error('복사 실패:', err);
                        alert('복사에 실패했습니다. 브라우저 권한을 확인해주세요.');
                    }});
                }}
            </script>
        </body>
        </html>
        """
        
        # 만든 HTML을 Streamlit 화면에 뿌려줍니다 (높이 80px 확보)
        components.html(custom_buttons_html, height=80)
        
        # ------------------------------------------------------------------
        # [2] 대본 박스 (버튼 바로 아래)
        # ------------------------------------------------------------------
        st.markdown(f'<div class="result-box" style="margin-top: 0;">{st.session_state["script"]}</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown(st.session_state["seo_result"])
    with tab3:
        st.info(st.session_state["trends"])

st.markdown('<div style="text-align: center; padding: 2rem; opacity: 0.5;">© 2026 LAST.PY_STUDIO</div>', unsafe_allow_html=True)