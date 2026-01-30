# 1. 페르소나 설정 (AI 말투 - 기존 유지)
PERSONA_PROMPTS = {
    "1020 (도파민/비주얼)": """
        - **Role**: Hyperactive Gen-Z Creator.
        - **Tone**: Chaotic, Loud, High-Pitch. Use exclamation marks!!!
        - **Structure**: Start with a scream or visual fail. Cut every 0.5 seconds.
    """,
    "3040 (핵심요약/효율)": """
        - **Role**: Smart Efficiency Expert.
        - **Tone**: Professional, Sharp, slightly Cynical but helpful.
        - **Structure**: [0s] Conclusion -> [Body] 3 Reasons -> [End] Verdict.
    """,
    "5060 (연륜/솔직함)": """
        - **Role**: Brutally Honest K-Uncle/Auntie.
        - **Tone**: Loud, Rough, but Warm. "Trust me, I know better."
        - **Structure**: Loud entrance -> Eating/Trying -> Honest reaction -> Recommendation.
    """
}

# 2. 주제별 검색 설정 (요청하신 내용 반영 완료)
# {q}는 사용자가 입력한 한국어 질문, {t}는 번역된 영어 키워드로 자동 치환됩니다.
TOPIC_CONFIG = {
    "Food": {
        "placeholder": "K-Food 주제 (예: 두바이 초콜릿, 탕후루, 불닭볶음면...)",
        "query_template": """
        Korean trend "{q}"
        viral food dessert reaction
        {t}
        """
    },
    "Animals": {
        "placeholder": "동물 관련 주제 (예: 푸바오, 시골잡종 강아지, 고양이 밈...)",
        "query_template": """
        Korean animal trend "{q}"
        focus on cute, funny, heartwarming pet reactions
        exclude: hunting, abuse, violence, exhausting or disturbing content
        {t}
        """
    },
    "K-culture": {
        "placeholder": "K-컬처 전반 (예: 뉴진스, 챌린지, 한국 드라마 명장면...)",
        "query_template": """
        Korean K-culture trend "{q}"
        covering K-pop, K-beauty, K-fashion, K-drama, K-food, K-memes, and Korean Gen-Z culture
        viral choreography challenge reaction
        viral skincare & makeup hacks
        aesthetic streetwear outfit inspiration
        trending drama scenes and emotional moments
        Korean food and dessert viral reactions
        K-meme humor popular on TikTok & YouTube Shorts
        {t}
        """
    },
    "Lifestyle": {
        "placeholder": "일상/브이로그 (예: 편의점 꿀조합, 한강 라면, 출근룩...)",
        "query_template": """
        Korean daily lifestyle trend "{q}"
        Korean convenience store (CU, GS25) food hacks & mukbang
        'Get Ready With Me' (GRWM) & OOTD for Korean weather
        Realistic day in the life (Vlog style): Student or Office worker
        Study with me (Gongbang) culture
        {t}
        """
    },
    "Slang": {
        "placeholder": "유행어/신조어 (예: 럭키비키, 완전 럭키, 추구미...)",
        "query_template": """
        Korean language & slang trend "{q}"
        Latest Gen-Z slang and internet memes explained
        Funny cultural differences and mannerisms
        Useful survival Korean phrases for travelers
        Reaction to funny Korean comments
        {t}
        """
    }
}