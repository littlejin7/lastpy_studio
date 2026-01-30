import streamlit as st
import streamlit.components.v1 as components
import base64
import json
from datetime import datetime

def render_action_buttons(script_text):
    """
    스크립트 텍스트를 매개변수로 받아 다운로드 버튼과 복사 버튼을 생성합니다.
    """
    # 1. 파일 다운로드를 위한 설정
    file_name = f"shorts_script_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    # 한글 깨짐 방지를 위해 utf-8 인코딩 후 base64 변환
    b64 = base64.b64encode(script_text.encode('utf-8')).decode()
    
    # 2. JavaScript로 전달하기 위해 JSON 직렬화 (줄바꿈 처리 포함)
    json_script = json.dumps(script_text)
    
    # 3. HTML/CSS/JS 결합 코드
    html_code = f"""
    <html>
    <head>
        <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@700;800&family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,700,1,0" rel="stylesheet">
        <style>
            body {{ margin: 0; padding: 0; overflow: hidden; }}
            .button-container {{
                display: flex;
                gap: 15px;
                justify-content: flex-end; /* 우측 정렬 */
                padding: 10px;
            }}

            /* 공통 3D 버튼 디자인 */
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
                padding: 12px 24px;
                font-size: 16px;
                color: white;
            }}

            .cute-3d-button:active {{
                transform: translateY(4px);
                box-shadow: none !important;
            }}

            /* 다운로드 버튼 (빨강) */
            .btn-download {{
                background-color: #ef4444;
                box-shadow: 0 5px 0 #991b1b;
            }}
            .btn-download:hover {{ background-color: #f87171; }}

            /* 복사 버튼 (주황) */
            .btn-copy {{
                background-color: #fbbf24;
                color: #451a03 !important;
                box-shadow: 0 5px 0 #b45309;
            }}
            .btn-copy:hover {{ background-color: #fcd34d; }}

            .material-symbols-outlined {{
                font-size: 20px;
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
                const textToCopy = {json_script};
                const btn = document.getElementById("copyBtn");
                const originalHTML = btn.innerHTML;
                
                // 클립보드 API 호출
                navigator.clipboard.writeText(textToCopy).then(() => {{
                    // 성공 시 피드백 시각화
                    btn.innerHTML = '<span class="material-symbols-outlined">check</span> COPIED!';
                    btn.style.backgroundColor = "#4ade80"; // 초록색으로 변경
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
                    console.error('Copy failed:', err);
                    alert('복사에 실패했습니다. 브라우저 권한을 확인해주세요.');
                }});
            }}
        </script>
    </body>
    </html>
    """
    
    # 만든 HTML을 Streamlit iframe 컴포넌트로 출력
    components.html(html_code, height=80)