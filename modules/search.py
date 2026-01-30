import ollama
from modules.prompts import TOPIC_CONFIG

def run(tavily_client, topic, question_ko, translation):
    # 1. prompts.py에서 템플릿 가져오기
    # (에러 방지를 위해 .strip()으로 공백 제거)
    raw_template = TOPIC_CONFIG[topic]["query_template"].strip()
    
    # 2. 검색어 완성하기
    # {q}에는 한국어 질문, {t}에는 영어 번역 키워드가 들어갑니다.
    tavily_query = raw_template.format(q=question_ko, t=translation)
    
    # 3. Tavily로 검색 실행
    search_result = tavily_client.search(query=tavily_query, search_depth="advanced")
    
    # 4. 검색 결과에서 텍스트만 뽑아내기 (여기에 r/BeginnerKorean 같은 게 섞여 있음)
    raw_content = "\n".join([item["content"] for item in search_result.get("results", [])[:5]])
    
    # 5. [청소 단계] AI에게 잡다한 UI 텍스트 제거하고 핵심만 요약하라고 시키기
    cleaning_prompt = f"""
    Analyze the following search results about "{question_ko}".
    Your task is to summarize the trend/facts clearly.
    
    [IMPORTANT RULES]
    1. Remove all website UI text (e.g., "r/...", "icon", "menu", "login", "cookies", "sign up").
    2. Focus ONLY on the viral content, reactions, and key information.
    3. Provide the summary in a clean, bullet-point format.
    
    [SEARCH DATA]:
    {raw_content}
    """
    
    # AI가 청소한 결과 받기
    response = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": cleaning_prompt}])
    cleaned_trends = response["message"]["content"]
    
    return cleaned_trends