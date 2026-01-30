import ollama
from modules.prompts import PERSONA_PROMPTS

def run(persona_key, trend_info, question_ko):
    # 1. 선택된 페르소나 내용 가져오기
    target_persona = PERSONA_PROMPTS[persona_key]
    
    # 2. AI에게 명령할 전체 프롬프트 조립
    full_prompt = f"""
    Act as a YouTube Shorts Strategist.
    # PERSONA: {target_persona}
    # TREND INFO: {trend_info}
    # TASK: Create a 'Viral Shorts Package' for "{question_ko}".
    
    Please provide:
    1. Titles: 3 options (Viral style).
    2. Script: 60s, Time-stamped, following the persona's tone strictly.
    3. Tags: 10 hashtags in a SINGLE LINE.
    """
    
    # 3. AI 실행
    res = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": full_prompt}])
    return res["message"]["content"]