import ollama
from modules.prompts import PERSONA_PROMPTS

# [옵션 설정] 문맥 길이 확장 (중간에 말 끊김 방지용)
# temperature: 0에 가까울수록 일관되고 정확한 답변, 1에 가까울수록 창의적이고 다양한 답변
AI_OPTIONS = {
    "num_ctx": 2000,
    "temperature": 0.7,  # 이 부분을 추가하세요 (0.0 ~ 1.0 사이 권장)
}


# [기능 1] 제목(훅) 3개만 먼저 뽑아오기
def generate_titles(persona_key, trend_info, question_ko):
    target_persona = PERSONA_PROMPTS[persona_key]

    prompt = f"""
    Act as a YouTube Shorts Strategist.
    # PERSONA: {target_persona}
    # TREND INFO: {trend_info}
    # TOPIC: {question_ko}
    
    Task: Create 3 Viral Short Video Titles (Hooks) strictly related to the topic.
    [CRITICAL RULE]: Do NOT use any emojis in the titles.
    Output format:
    1. [Title 1]
    2. [Title 2]
    3. [Title 3]
    (Do not write the script yet, ONLY titles)
    """

    # 기억력 옵션 추가
    res = ollama.chat(
        model="gemma3:latest",
        messages=[{"role": "user", "content": prompt}],
        options=AI_OPTIONS,
    )

    # 결과 파싱 (텍스트 -> 리스트 변환)
    raw_titles = res["message"]["content"].strip().split("\n")
    clean_titles = [t.strip() for t in raw_titles if t.strip()]
    # 요청하신 대로 최대 3개까지만 반환하도록 수정했습니다
    return clean_titles[:3]


# [기능 2] 선택된 제목으로 대본 쓰기 (루프 규칙 제거됨)
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
    [CRITICAL RULE]: Do NOT use any emojis in the script or tags.
    
    Please provide:
    1. Script: 60s, Time-stamped, strictly following the persona's tone.
    2. Tags: 10 hashtags in a SINGLE LINE.
    """

    # 기억력 옵션 추가
    res = ollama.chat(
        model="gemma3:latest",
        messages=[{"role": "user", "content": prompt}],
        options=AI_OPTIONS,
    )
    return res["message"]["content"]
