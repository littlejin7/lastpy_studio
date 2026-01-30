import streamlit as st
# app.py에서 sys.path 설정을 했으므로 modules에서 바로 불러올 수 있습니다.
try:
    from modules import prompts
except ImportError:
    # 예외 처리: 경로 문제 발생 시 대비
    import prompts 

def render_sidebar():
    """
    사이드바의 로고, 제목, 페르소나 선택 라디오 버튼을 렌더링합니다.
    선택된 페르소나의 키(Key) 값을 반환합니다.
    """
    with st.sidebar:
        # 1. 상단 로고 및 타이틀 구역
        st.markdown(
            """
            <div style="text-align: center; padding: 1rem 0;">
                <div style="background: #ef4444; width: 60px; height: 60px; border-radius: 1.5rem; margin: 0 auto 1rem; display: flex; align-items: center; justify-content: center;">
                    <span style="color: white; font-size: 2rem;">⚡</span>
                </div>
                <h2 style="margin: 0; color: #451a03; font-family: 'Fredoka', sans-serif;">last.py_studio</h2>
            </div>
            """, 
            unsafe_allow_html=True
        )

        st.write("---")

        # 2. 페르소나 설정 (라디오 버튼)
        # prompts.PERSONA_PROMPTS 딕셔너리의 키값들을 가져와 선택지를 만듭니다.
        persona_list = list(prompts.PERSONA_PROMPTS.keys())
        
        selected_persona = st.radio(
            "페르소나 설정", 
            options=persona_list, 
            index=1  # 기본값: 두 번째 항목
        )

        # 하단 여백이나 추가 정보를 넣고 싶다면 여기에 작성
        st.markdown("---")
        st.caption("v3.0.0 Powered by Gemini & Tavily")
        
    # 사용자가 선택한 페르소나 이름을 반환하여 app.py에서 사용하게 함
    return selected_persona