import streamlit as st

def apply_dark_css():
    """
    [다크 모드 전용] 
    1. 올-화이트 텍스트 및 테두리 제거
    2. 사이드바 유령 텍스트(keyboard_double) 박멸
    """
    font_css = """
        @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Fredoka', sans-serif !important; }
    """
    st.markdown(f"""
    <style>
        {font_css}
        .stApp {{ background-color: #111827 !important; }}

        /* [핵심] 모든 텍스트 화이트 강제 (입력창 내부 포함) */
        .main h1, .main h2, .main h3, .main p, .main span, .main div, .main label,
        .playful-container h1, .playful-container p,
        div[data-testid="stWidgetLabel"] p,
        .main input, 
        .main div[data-baseweb="select"] div,
        .main div[data-baseweb="select"] span {{
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
        }}

        /* 입력창 테두리 및 그림자 완전 제거 */
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"],
        div[data-baseweb="base-input"] > div,
        .stTextInput input {{
            background-color: #1e1e1e !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
        }}

        .main .stSelectbox svg {{ fill: #ffffff !important; }}

        /* 사이드바 가독성 설정 */
        section[data-testid="stSidebar"] {{ background-color: #f0f2f6 !important; }}
        section[data-testid="stSidebar"] * {{ color: #333333 !important; }}
        header {{ background-color: #f0f2f6 !important; }}

        .playful-container {{ background-color: #1f2937 !important; border: none !important; padding: 2rem; border-radius: 2rem; text-align: center; }}
        .stButton > button {{ background-color: #4ade80 !important; color: white !important; border-radius: 2rem !important; box-shadow: 0 5px 0 #2d9a58 !important; }}

        /* =========================================================
           [긴급] 사이드바 접기 버튼 유령 텍스트(keyboard_double) 박멸
           ========================================================= */
        /* 버튼 내부의 숨겨진 아이콘 텍스트 제거 */
        button[data-testid="stSidebarCollapseButton"] span {{
            display: none !important;
        }}

        /* 마우스 올릴 때 나타나는 모든 툴팁 차단 */
        div[data-testid="stTooltipContent"],
        div[data-testid="stTooltipHoverTarget"] {{
            display: none !important;
            visibility: hidden !important;
        }}

        /* 버튼 자체의 텍스트 투명화 */
        button[data-testid="stSidebarCollapseButton"] {{
            color: transparent !important;
            -webkit-text-fill-color: transparent !important;
        }}
        
        /* 화살표 아이콘만 다시 보이기 */
        button[data-testid="stSidebarCollapseButton"] svg {{
            fill: #333333 !important;
            visibility: visible !important;
        }}
    </style>
    """, unsafe_allow_html=True)