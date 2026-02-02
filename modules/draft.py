import ollama
from modules.prompts import PERSONA_PROMPTS
import re

# [옵션 설정] 문맥 길이 확장 (중간에 말 끊김 방지용)
AI_OPTIONS = {'num_ctx': 2000, "temperature": 0.7}

# [기능 1] 영어 제목 3개 생성 (기존 유지 + 잡담 필터 강화)
def generate_titles(persona_key, trend_info, question_ko):
    target_persona = PERSONA_PROMPTS[persona_key]
    
    prompt = f"""
    Act as a YouTube Shorts Strategist.
    # PERSONA: {target_persona}
    # TREND INFO: {trend_info}
    # TOPIC: {question_ko}
    
    Task: Create exactly 3 Viral Short Video Titles (Hooks) in ENGLISH.
    
    [STRICT OUTPUT RULES]
    1. Output **ONLY** the 3 titles.
    2. No numbering (1., 2.), no bullets.
    3. One title per line.
    """
    
    res = ollama.chat(
        model="gemma3:latest", 
        messages=[{"role": "user", "content": prompt}],
        options=AI_OPTIONS
    )
    
    # 영어 제목 필터링
    raw_content = res["message"]["content"].strip()
    lines = raw_content.split('\n')
    clean_titles = []
    
    for line in lines:
        clean_line = re.sub(r'^[\d\.\-\*\•\)]+\s*', '', line).strip().strip('"\'')
        if clean_line and not clean_line.lower().startswith(("here", "sure", "okay")):
            clean_titles.append(clean_line)
    
    return clean_titles[:3]

# [기능 2] 영어 제목 리스트 -> 한국어 번역
def translate_hooks_to_korean(titles_en_list):
    """
    영어 제목 3개를 한 번에 받아서, 자연스러운 한국어(유튜브 스타일)로 번역
    """
    if not titles_en_list:
        return []

    # 리스트를 하나의 문자열로 합쳐서 보냄 (효율성 UP)
    input_text = "\n".join(titles_en_list)

    prompt = f"""
    You are a professional Korean YouTube Shorts Translator.
    Translate the following English hooks into **Viral Korean (Hangul)**.
    
    [Input English Hooks]:
    {input_text}
    
    [Rules]:
    1. Maintain the "Viral/Clickbait" nuance (use words like 충격, 헉, ㄷㄷ naturally).
    2. Output EXACTLY {len(titles_en_list)} lines.
    3. **NO** conversational fillers (e.g., "Here is the translation").
    4. **NO** numbering or bullet points. Just the Korean text.
    """

    res = ollama.chat(
        model="gemma3:latest", 
        messages=[{"role": "user", "content": prompt}],
        options=AI_OPTIONS
    )

    # 결과 파싱
    raw_content = res["message"]["content"].strip()
    lines = raw_content.split('\n')

    titles_ko = []
    for line in lines:
        # 번호, 특수기호 제거 및 정제
        clean_line = re.sub(r'^[\d\.\-\*\•\)]+\s*', '', line).strip().strip('"\'')
        
        # 잡담 필터링 (혹시 모를 AI의 말대꾸 차단)
        if clean_line and not clean_line.startswith(("Here", "Sure", "Certainly", "Translation")):
            titles_ko.append(clean_line)

    # 혹시 개수가 안 맞으면 원본(영어)이라도 돌려줌 (안전장치)
    if len(titles_ko) == 0:
        return titles_en_list
        
    return titles_ko[:3]

# [기능 3] 선택된 제목으로 대본 쓰기 (루프 규칙 제거됨)
def generate_script(persona_key, selected_titles, trend_info):
    target_persona = PERSONA_PROMPTS[persona_key]
    
    # 리스트를 문자열로 변환
    titles_str = ", ".join(selected_titles)
    
    prompt = f"""
    Act as a Scriptwriter.
    # PERSONA: {target_persona}
    # SELECTED HOOKS: {titles_str} (User selected these!)
    # TREND INFO: {trend_info}
    
    Task: Write a 60s Shorts Script that integrates the selected hooks perfectly.
    
    Please provide:
    1. Script: 60s, Time-stamped, strictly following the persona's tone.
    2. Tags: 10 hashtags in a SINGLE LINE.
    """
    
    # 기억력 옵션 추가
    res = ollama.chat(
        model="gemma3:latest", 
        messages=[{"role": "user", "content": prompt}],
        options=AI_OPTIONS
    )
    return res["message"]["content"]