import argparse
import sys
from komorph import Analyzer

def main():
    parser = argparse.ArgumentParser(
        description="ko-morph: 하이브리드 한국어 형태소 분석기"
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        help="분석할 텍스트 (생략시 stdin에서 읽음)"
    )
    
    parser.add_argument(
        "--data-dir",
        help="데이터 디렉토리 경로"
    )
    
    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="LLM 재랭킹 사용"
    )
    
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="출력 형식"
    )
    
    args = parser.parse_args()
    
    # 입력 텍스트 처리
    if args.text:
        text = args.text
    else:
        text = sys.stdin.read().strip()
    
    if not text:
        print("분석할 텍스트를 입력해주세요.", file=sys.stderr)
        return 1
    
    # 분석기 초기화
    try:
        analyzer = Analyzer(
            data_dir=args.data_dir,
            use_llm=args.use_llm
        )
        
        # 분석 실행
        if args.format == "json":
            import json
            result = analyzer.analyze(text)
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            result = analyzer.analyze_text(text)
            print(result)
            
    except Exception as e:
        print(f"분석 중 오류 발생: {e}", file=sys.stderr)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
