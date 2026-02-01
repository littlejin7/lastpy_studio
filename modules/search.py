import ollama
from modules.prompts import SEARCH_QUERY_OPTIMIZER, TOPIC_CONFIG

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

def run(tavily_client, topic, question_ko, translation):
    """
    1. [검색어 최적화] LLM에게 '사실 확인용' 검색어를 물어봄 (춘봉이 방지)
    2. [검색] 최적화된 검색어로 Tavily 실행
    3. [요약] 결과 정리
    """

    # ---------------------------------------------------------
    # [STEP 1] 검색어 최적화 (여기가 핵심!)
    # ---------------------------------------------------------
    print(f"🤔 [Thinking] '{question_ko}'에 대한 최적의 검색어 고민 중...")
    
    # 방금 prompts.py에 추가한 그 프롬프트를 가져와서 포맷팅
    opt_prompt = SEARCH_QUERY_OPTIMIZER.format(category=topic, user_input=question_ko)
    
    # LLM에게 검색어 생성 요청
    res = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": opt_prompt}])
    optimized_query = res["message"]["content"].strip()
    
    print(f"⚡ [Search] 최적화된 검색어: '{optimized_query}'") 

    # ---------------------------------------------------------
    # [STEP 2] 똑똑해진 검색어로 Tavily 실행
    # ---------------------------------------------------------
    # 이제 'Korean viral trend...'가 아니라 '시고르자브종 뜻 특징...'으로 검색됨
    search_result = tavily_client.search(query=optimized_query, search_depth="advanced")
    
    # ---------------------------------------------------------
    # [STEP 3] 결과 청소 및 요약
    # ---------------------------------------------------------
    raw_content = "\n".join([item["content"] for item in search_result.get("results", [])[:5]])
    
    cleaning_prompt = f"""
    Analyze the provided Search Data about "{question_ko}".
    Summarize the key definitions, characteristics, and interesting facts.
    
    [IMPORTANT]
    - Focus on the specific topic "{question_ko}". 
    - Do NOT include unrelated viral trends unless directly mentioned in the data.
    
    [SEARCH DATA]:
    {raw_content}
    """
    
    response = ollama.chat(model="gemma3:latest", messages=[{"role": "user", "content": cleaning_prompt}])
    cleaned_trends = response["message"]["content"]
    
    return cleaned_trends