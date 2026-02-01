import streamlit as st

def apply_light_css():
    """
    [라이트 모드 전용] 
    지혜원 조장님이 선호하시는 노란색 Playful 테마입니다.
    """
    font_css = """
        @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300;400;500;600;700&display=swap');
        * { font-family: 'Fredoka', sans-serif !important; }
    """
    st.markdown(f"""
    <style>
        {font_css}
        
        /* 1. 배경: 노란색 그라데이션 */
        .stApp {{ 
            background: linear-gradient(135deg, #facc15 0%, #fbbf24 100%) !important; 
        }}
        
        /* 2. 텍스트: 원래의 갈색 */
        .main h1, .main label, .main p, .main span {{ 
            color: #451a03 !important; 
        }}
        
        /* 3. 입력창: 흰색 배경 + 노란 테두리 유지 */
        div[data-baseweb="select"] > div,
        div[data-baseweb="base-input"],
        div[data-baseweb="base-input"] > div {{
            background-color: #ffffff !important;
            border: 2px solid #fde68a !important;
            border-radius: 0.8rem !important;
            min-height: 45px !important;
        }}
        
        /* 입력창 내부 텍스트 색상 */
        .stTextInput input, .stSelectbox span {{ 
            color: #451a03 !important; 
        }}
        
        /* 4. 헤더 박스 (Playful Container) */
        .playful-container {{
            background-color: #fffbeb !important;
            padding: 2.5rem;
            border-radius: 2rem;
            border: 2px solid rgba(255,255,255,0.2) !important;
            text-align: center;
            margin-bottom: 2rem;
        }}
        .playful-container h1 {{ color: #451a03 !important; }}
        
        /* 5. 사이드바 및 상단 헤더 */
        section[data-testid="stSidebar"] {{ background-color: #fefce8 !important; }}
        header {{ background-color: #fefce8 !important; }}
        
        /* 6. 버튼 스타일 */
        .stButton > button {{
            background-color: #4ade80 !important;
            color: white !important;
            border-radius: 2rem !important;
            font-weight: 700 !important;
            box-shadow: 0 5px 0 #2d9a58 !important;
        }}
    </style>
    """, unsafe_allow_html=True)