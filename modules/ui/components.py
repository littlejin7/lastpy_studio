import streamlit as st
import re
from utils.seo_tools import render_copy_button


def render_title_selector(titles):
    """
    [1단계] 제목 추천 섹션
    - 아이콘과 CHOOSE TITLE 문구의 수직 정렬 완벽 최적화
    """
    if not titles:
        return None

    st.markdown("---")

    # 1. 상단 헤더 (아이콘과 텍스트 정렬 보정)
    st.markdown(
        """
        <div style="margin-top: 10px; margin-bottom: 25px; display: flex; align-items: center; gap: 12px;">
            <span class="material-symbols-outlined" 
                  style="color: #ef4444; font-size: 2.2rem; font-weight: 900; line-height: 1; display: inline-block;">
                checklist
            </span>
            <div style="display: flex; flex-direction: column; justify-content: center;">
                <h3 style="font-family: 'Fredoka', sans-serif; font-size: 1.5rem; font-weight: 700; color: #451a03; margin: 0; line-height: 1.1;">
                    CHOOSE TITLE
                </h3>
                <p style="font-family: 'Fredoka', sans-serif; font-size: 0.85rem; font-weight: 600; color: #92400e; margin: 0; line-height: 1;">
                    (최대 3개 선택 가능)
                </p>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # (이하 제목 리스트 및 체크박스 로직은 기존과 동일)
    selected = []

    # 제목 리스트 디자인 (기존 유지)
    for i, title in enumerate(titles):
        index_label = f"{i+1:02}"
        col_check, col_content = st.columns([0.08, 0.92], gap="small")

        with col_check:
            is_checked = st.checkbox(
                f"cb_{i}", label_visibility="hidden", key=f"title_cb_{i}"
            )

        with col_content:
            is_dark = st.session_state.get("dark_mode", False)
            bg_color = (
                ("#fefce8" if is_checked else "#ffffff")
                if not is_dark
                else ("#2d3748" if is_checked else "#1f2937")
            )

            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 15px; padding: 16px 20px; background-color: {bg_color}; 
                            border: 2px solid #fef08a; border-radius: 1rem; margin-bottom: 12px; margin-left: -15px;">
                    <span style="background-color: #ef4444; color: white; font-weight: 900; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">{index_label}</span>
                    <span style="font-family: 'Fredoka', sans-serif; font-weight: 600; color: {('#451a03' if not is_dark else '#ffffff')}; font-size: 1.1rem;">
                        {title}
                    </span>
                </div>
            """,
                unsafe_allow_html=True,
            )
            if is_checked:
                selected.append(title)

    if selected:
        # 일괄 생성 버튼 폰트 설정 (기존 유지)
        st.markdown(
            """
            <style>
            div.stButton > button { font-family: 'Fredoka', sans-serif !important; font-weight: 700 !important; }
            </style>
        """,
            unsafe_allow_html=True,
        )
        if st.button(
            "🚀 선택된 제목으로 스크립트 일괄 생성",
            key="btn_batch",
            use_container_width=True,
        ):
            return selected
    return None


def render_action_buttons(script_content):
    """
    [2단계] 최종 통합 워크스페이스
    - 조장님 요청: 해시태그랩과 바이럴팁을 상단으로 올리고 에디터를 가로 풀사이즈로 변경
    """
    if not script_content:
        return

    # 정규식으로 #태그 실시간 추출
    extracted_tags = re.findall(r"#\w+", script_content)
    display_tags = (
        extracted_tags
        if extracted_tags
        else ["#유튜브쇼츠", "#트렌드", "#LastpyStudio"]
    )

    # CSS: 3D 버튼 및 해시태그 디자인
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@900&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-25..0');

        div[data-testid="stDownloadButton"] > button {
            background-color: #ef4444 !important;
            color: white !important;
            border-radius: 1.5rem !important;
            padding: 0.6rem 2rem !important;
            font-weight: 900 !important;
            /* [핵심 추가] 폰트를 Fredoka로 설정 */
            font-family: 'Fredoka', sans-serif !important;
            box-shadow: 0 6px 0 #991b1b, inset 0 -3px 4px rgba(0,0,0,0.1) !important;
            transition: all 0.1s !important;
        }
        div[data-testid="stDownloadButton"] > button:active { transform: translateY(4px) !important; box-shadow: none !important; }

        .hashtag-wrapper {
            display: flex;
            flex-wrap: wrap; 
            gap: 8px !important; 
            align-items: center;
        }

        .hashtag-pill {
            background-color: #fef08a;
            color: #451a03;
            padding: 4px 10px;
            border-radius: 10px;
            font-size: 0.8rem;
            font-weight: 800;
            white-space: nowrap;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            border: 1px solid rgba(253, 224, 71, 0.4);
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # 1. 헤더 및 다운로드 버튼
    header_col, download_col = st.columns([0.7, 0.3])
    with header_col:
        st.markdown(
            """
            <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
                <span class="material-symbols-outlined" style="color: #ef4444; font-size: 2.5rem; font-weight: 900;">verified</span>
                <h3 style="font-size: 1.5rem; font-weight: 900; color: #451a03; margin: 0; font-family: 'Fredoka';">FINAL WORKSPACE</h3>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with download_col:
        st.download_button(
            "📥 전체 저장",
            data=script_content,
            file_name="lastpy_script.txt",
            use_container_width=True,
        )

    # 2. 상단 가로 배치: Hashtag Lab & Viral Tips
    info_col_left, info_col_right = st.columns([0.5, 0.5], gap="medium")

    with info_col_left:
        st.markdown(
            """
            <p style='font-size: 1rem; font-weight: 900; color: #ef4444; text-transform: uppercase; margin-bottom: 8px; font-family: "Fredoka";'>
                Hashtag Lab
            </p>
            <div class="hashtag-wrapper">
        """,
            unsafe_allow_html=True,
        )
        tags_html = "".join(
            [f'<span class="hashtag-pill">{tag}</span>' for tag in display_tags]
        )
        st.markdown(tags_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with info_col_right:
        st.markdown(
            """
            <div style='background: #fefce8; border: 2px dashed #fde047; border-radius: 1rem; padding: 12px 18px;'>
                <span style='font-size: 1rem; font-weight: 900; color: #92400e; display: block; margin-bottom: 4px;'>VIRAL TIPS</span>
                <p style='font-size: 0.75rem; color: #451a03; font-weight: 600; line-height: 1.4; margin: 0;'>
                    💡 <b>EDITOR</b>에서 직접 수정하세요. 모든 작업이 한 화면에서 가능합니다!
                </p>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='margin-top: 25px;'></div>", unsafe_allow_html=True)

    # 3. 하단 풀 가로 배치: Editor
    st.markdown(
        "<p style='font-size: 1.25em; font-weight: 900; color: #92400e; margin-bottom: 8px;'>EDITOR</p>",
        unsafe_allow_html=True,
    )
    edited_script = st.text_area(
        "Editor",
        value=script_content,
        height=500,
        label_visibility="collapsed",
        key="unified_editor",
    )
    render_copy_button(edited_script, "📋 편집 내용 복사")

    return edited_script
