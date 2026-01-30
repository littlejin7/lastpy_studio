import streamlit as st

# 변수 임의 설정(필요x)
question_ko = st.text_input("한국어 질문 입력")
translation = st.text_input("영문 번역")

topics = {
    "Food": f"""
    Korean trend "{question_ko}"
    viral food dessert reaction
    {translation}
    """[:350],

    "K-pop": f"""
    Korean K-pop trend "{question_ko}"
    viral choreography challenge reaction
    {translation}
    """[:350],

    "K-Beauty": f"""
    Korean beauty skincare trend "{question_ko}"
    viral product hack reaction
    {translation}
    """[:350]
}

# 사이드 바 쪽으로 빼면 좋을듯
selected_topic = st.selectbox(
    "쿼리 주제를 선택하세요",
    list(topics.keys())
)

#확인용
if selected_topic and question_ko:
    tavily_query = topics[selected_topic]
    st.text_area("최종 Tavily Query", tavily_query, height=180)



