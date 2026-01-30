# utils 폴더에 있는 seo_analyzer.py를 불러옵니다.
# (만약 에러나면 sys.path 설정이 필요한데, app.py가 같은 위치에 있다면 자동 인식됩니다.)
from utils.seo_analyzer import analyze_seo_score

def run(script):
    # 기존에 만들어두신 분석 함수를 실행하고 결과만 돌려줍니다.
    return analyze_seo_score(script)