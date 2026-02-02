import streamlit as st
import re
from utils.seo_tools import render_copy_button

def render_title_selector(titles):
    """ 
    [1단계] 제목 추천 섹션 
    - 조장님 요청: 체크박스 크기 확대 및 제목 박스와의 완벽한 수직 대칭 정렬
    """
    if not titles: return None
    
    st.markdown("---")
    
    # 체크박스 크기 및 정렬 전용 CSS 추가
    st.markdown("""
        <style>
        /* 1. 체크박스 자체 크기 확대 (1.3배) */
        [data-testid="stCheckbox"] > label > span:first-child {
            transform: scale(1.3) !important; 
            margin-right: 10px !important;
        }
        
        /* 2. 체크박스 컬럼을 Flex박스로 만들어 수직 중앙 정렬 강제 */
        div[data-testid="column"]:first-child {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="margin-top: 10px; margin-bottom: 20px;">
            <p style="font-size: 0.9rem; font-weight: 900; color: #92400e; text-transform: uppercase; letter-spacing: 0.15em; display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="font-size: 1.2rem;">checklist</span>
                제안된 제목 (최대 3개 선택 가능)
            </p>
        </div>
    """, unsafe_allow_html=True)

    selected = []
    
    for i, title in enumerate(titles):
        index_label = f"{i+1:02}"
        # 큰 체크박스가 들어갈 수 있게 첫 번째 컬럼 비율을 0.08로 미세 조정
        col_check, col_content = st.columns([0.08, 0.92], gap="small")
        
        with col_check:
            # 수직 정렬이 적용된 체크박스
            is_checked = st.checkbox(f"cb_{i}", label_visibility="hidden", key=f"title_cb_{i}")
        
        with col_content:
            is_dark = st.session_state.get("dark_mode", False)
            bg_color = ("#fefce8" if is_checked else "#ffffff") if not is_dark else ("#2d3748" if is_checked else "#1f2937")
            st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 15px; padding: 16px 20px; background-color: {bg_color}; 
                            border: 2px solid #fef08a; border-radius: 1rem; margin-bottom: 12px; margin-left: -15px;">
                    <span style="background-color: #ef4444; color: white; font-weight: 900; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">{index_label}</span>
                    <span style="font-weight: 700; color: {('#451a03' if not is_dark else '#ffffff')}; font-size: 1.05rem;">{title}</span>
                </div>
            """, unsafe_allow_html=True)
            if is_checked: selected.append(title)
            
    if selected:
        if st.button("🚀 선택된 제목 스크립트 일괄 생성", key="btn_batch", use_container_width=True):
            return selected
    return None

def render_action_buttons(script_content):
    """
    [2단계] 최종 통합 워크스페이스
    - 조장님 요청: 하단 중복 창을 제거하고 에디터에 모든 내용 통합
    - 해시태그는 실시간 추출하여 Hashtag Lab에 슬림하게 노출
    """
    if not script_content:
        return

    # 정규식으로 #태그 실시간 추출
    extracted_tags = re.findall(r'#\w+', script_content) 
    display_tags = extracted_tags if extracted_tags else ["#유튜브쇼츠", "#트렌드", "#LastpyStudio"]

    # CSS: 3D 버튼 및 해시태그 슬림 디자인
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@900&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-25..0');

        div[data-testid="stDownloadButton"] > button {
            background-color: #ef4444 !important;
            color: white !important;
            border-radius: 1.5rem !important;
            padding: 0.6rem 2rem !important;
            font-weight: 900 !important;
            box-shadow: 0 6px 0 #991b1b, inset 0 -3px 4px rgba(0,0,0,0.1) !important;
            transition: all 0.1s !important;
        }
        div[data-testid="stDownloadButton"] > button:active { transform: translateY(4px) !important; box-shadow: none !important; }

        .hashtag-wrapper {
            display: flex;
            flex-wrap: wrap; 
            gap: 10px !important; 
            align-items: center;
            margin-top: 10px;
        }

        .hashtag-pill {
            background-color: #fef08a;
            color: #451a03;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 800;
            white-space: nowrap;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid rgba(253, 224, 71, 0.4);
        }
        </style>
    """, unsafe_allow_html=True)

    # 헤더 및 다운로드 버튼 (우측 정렬)
    header_col, download_col = st.columns([0.7, 0.3])
    with header_col:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <span class="material-symbols-outlined" style="color: #ef4444; font-size: 2.5rem; font-weight: 900;">verified</span>
                <h3 style="font-size: 1.5rem; font-weight: 900; color: #451a03; margin: 0; font-family: 'Fredoka';">FINAL WORKSPACE</h3>
            </div>
        """, unsafe_allow_html=True)
    with download_col:
        st.download_button("📥 전체 저장", data=script_content, file_name="lastpy_script.txt", use_container_width=True)

    col_main, col_info = st.columns([0.65, 0.35], gap="medium")
    
    with col_main:
        st.markdown("<p style='font-size: 0.75rem; font-weight: 900; color: #92400e; margin-bottom: 10px;'>EDITOR</p>", unsafe_allow_html=True)
        edited_script = st.text_area("Editor", value=script_content, height=550, label_visibility="collapsed", key="unified_editor")
        render_copy_button(edited_script, "📋 편집 내용 복사")

    with col_info:
        st.markdown("""
            <p style='font-size: 0.85rem; font-weight: 900; color: #ef4444; text-transform: uppercase; margin-bottom: 10px; font-family: "Fredoka";'>
                Hashtag Lab
            </p>
            <div class="hashtag-wrapper">
        """, unsafe_allow_html=True)
        
        tags_html = "".join([f'<span class="hashtag-pill">{tag}</span>' for tag in display_tags])
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("""
            <div style='background: #fefce8; border: 2px dashed #fde047; border-radius: 1.5rem; padding: 20px; margin-top: 35px;'>
                <p style='font-size: 0.75rem; font-weight: 900; color: #92400e; margin-bottom: 8px;'>VIRAL TIPS</p>
                <p style='font-size: 0.75rem; color: #451a03; font-weight: 600; line-height: 1.5;'>
                    💡 <b>EDITOR</b>에서 직접 수정하고 저장하세요.<br>
                    💡 하단에 중복되던 창은 조장님 요청으로 제거되었습니다.<br>
                    💡 한 화면에서 모든 작업이 가능합니다!
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    return edited_script