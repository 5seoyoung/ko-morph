import pytest
from komorph import Analyzer

def test_analyzer_initialization():
    """분석기 초기화 테스트"""
    analyzer = Analyzer()
    assert analyzer is not None
    assert analyzer.dictionary is not None
    assert analyzer.rules is not None

def test_basic_analysis():
    """기본 형태소 분석 테스트"""
    analyzer = Analyzer()
    
    # 간단한 문장 테스트
    result = analyzer.analyze("안녕하세요")
    assert isinstance(result, list)
    assert len(result) > 0
    
    # 각 토큰 결과 검증
    for token_result in result:
        assert isinstance(token_result, list)
        for morph_info in token_result:
            assert "morph" in morph_info
            assert "pos" in morph_info
            assert isinstance(morph_info["morph"], str)
            assert isinstance(morph_info["pos"], str)

def test_josa_analysis():
    """조사 분석 테스트"""
    analyzer = Analyzer()
    
    result = analyzer.analyze("학교에서")
    # 결과 검증은 실제 사전 파일 로드 후에 가능
    assert len(result) > 0

def test_text_format_output():
    """텍스트 형식 출력 테스트"""
    analyzer = Analyzer()
    
    result = analyzer.analyze_text("안녕하세요")
    assert isinstance(result, str)
    assert len(result) > 0

if __name__ == "__main__":
    pytest.main([__file__])