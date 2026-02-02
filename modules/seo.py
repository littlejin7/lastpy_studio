# modules/seo.py

from utils.seo_analyzer import analyze_seo_score

def run(script):
    # 1. 원본 분석기 실행 (영문 결과 반환)
    english_report = analyze_seo_score(script)
    
    # 2. 번역 매핑 리스트
    translation_map = {
        "SEO Score Analysis": "상세 SEO 분석 리포트",
        "Overall Score": "종합 점수",
        "Watch Time Retention": "시청 지속 시간",
        "Rewatch Rate": "재시청률",
        "Search Intent Alignment": "검색 의도 부합도",
        "GEO Semantic Structure": "구조적 완성도",
        "Hook Power": "초반 후킹 강도",
        "User Engagement": "사용자 참여 유도",
        "AI Slop Filter": "AI 부자연스러움 필터"
    }
    
    # 3. 텍스트 치환
    korean_report = english_report
    for eng, kor in translation_map.items():
        korean_report = korean_report.replace(eng, kor)
    
    return korean_report