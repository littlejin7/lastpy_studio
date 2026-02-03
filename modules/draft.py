import ollama
from modules.prompts import PERSONA_PROMPTS
import re

# [설정 변경] 사용자 요청 파라미터 완벽 적용
AI_OPTIONS = {
    # 1. context_length 대응 (기억 용량)
    "num_ctx": 4096,        # 4096 정도면 쇼츠 대본 작업에 충분합니다.
    
    # 2. max_tokens 대응 (출력 길이)
    "num_predict": 1000,    # 요청하신 대로 1000으로 설정 (약 60~80초 분량)
    
    # 3. 창의성 조절
    "temperature": 0.4,     # 0.4: 구조와 형식을 잘 지킴 (안정적)
    
    # 4. (선택) 반복 방지 (필요하면 유지, 아니면 삭제해도 됨)
    "repeat_penalty": 1.1,  
}

# [기능 1] 영어 제목 3개 생성
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
        options=AI_OPTIONS,    # ✅ 튜닝 옵션 적용
        keep_alive=0           # ✅ 메모리 즉시 해제
    )
    
    # 영어 제목 필터링
    raw_content = res["message"]["content"].strip()
    lines = raw_content.split('\n')
    clean_titles = []
    
    for line in lines:
        clean_line = re.sub(r'^[\d\.\-\*\•\)]+\s*', '', line).strip().strip('"\'')
        # 기존 필터 유지
        if clean_line and not clean_line.lower().startswith(("here", "sure", "okay")):
            clean_titles.append(clean_line)
    
    return clean_titles[:3]

# [기능 2] 영어 제목 리스트 -> 한국어 번역
def translate_hooks_to_korean(titles_en_list, question_ko):
    """
    영어 제목들을 원본 한글 주제(question_ko)의 맥락을 고려하여 
    자연스러운 한국어 유튜브 스타일로 번역합니다.
    """
    if not titles_en_list:
        return []

    input_text = "\n".join(titles_en_list)

    prompt = f"""
    You are a professional Korean YouTube Shorts Translator and Strategist.
    The user's original topic is: "{question_ko}"
    
    Translate the following English hooks into **Viral Korean (Hangul)**, 
    keeping the original topic's context and nuance.
    
    [Input English Hooks]:
    {input_text}
    
    [Rules]:
    1. Maintain the "Viral/Clickbait" nuance (use words like 충격, 헉, ㄷㄷ naturally).
    2. Output EXACTLY {len(titles_en_list)} lines.
    3. **NO** conversational fillers or numbering.
    4. **PURE TEXT ONLY**: Output ONLY the Korean text.
    5. **NO EMOJIS**: Do not use any emojis or special symbols (e.g., ✨, 😱, 🔥).
    """

    res = ollama.chat(
        model="gemma3:latest", 
        messages=[{"role": "user", "content": prompt}],
        options=AI_OPTIONS,    # ✅ 튜닝 옵션 적용
        keep_alive=0           # ✅ 메모리 즉시 해제
    )

    # 결과 파싱 및 정제
    raw_content = res["message"]["content"].strip()
    lines = raw_content.split('\n')

    titles_ko = []
    for line in lines:
        # 번호, 특수기호 제거 및 정제
        clean_line = re.sub(r'^[\d\.\-\*\•\)]+\s*', '', line).strip().strip('"\'')
        # 혹시나 남아있을 수 있는 이모지 패턴 제거 (정규식)
        clean_line = re.sub(r'[^\w\s\?\!\,\.\%\(\)]', '', clean_line)
        
        # 잡담 필터링 (기존 목록에 "Okay" 하나만 추가했습니다)
        if clean_line and not clean_line.startswith(("Here", "Sure", "Certainly", "Translation", "Okay")):
            titles_ko.append(clean_line)

    # 개수가 안 맞거나 실패 시 원본(영어) 반환 (안전장치)
    if len(titles_ko) == 0:
        return titles_en_list
        
    return titles_ko[:3]

# [기능 3] 선택된 제목으로 대본 쓰기
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
    
    res = ollama.chat(
        model="gemma3:latest", 
        messages=[{"role": "user", "content": prompt}],
        options=AI_OPTIONS,    # ✅ 튜닝 옵션 적용
        keep_alive=0           # ✅ 메모리 즉시 해제
    )
    return res["message"]["content"]