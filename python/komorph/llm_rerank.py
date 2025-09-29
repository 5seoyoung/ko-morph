from typing import List, Dict, Any, Optional
from .rules import MorphemeCandidate

class LLMReranker:
    """LLM을 이용한 형태소 분석 재랭킹 (현재는 스텁)"""
    
    def __init__(self, provider: str = None, api_key: str = None):
        self.provider = provider  # "openai", "anthropic", etc.
        self.api_key = api_key
        self._available = False
        
        # TODO: API 키 확인 및 연결 설정
    
    def is_available(self) -> bool:
        """LLM 서비스 사용 가능 여부"""
        return self._available
    
    def rerank_candidates(self, 
                         context: str,
                         target_token: str, 
                         candidates: List[MorphemeCandidate],
                         top_k: int = 3) -> List[MorphemeCandidate]:
        """후보들을 LLM으로 재랭킹"""
        
        if not self.is_available() or len(candidates) <= 1:
            return candidates
        
        # TODO: 실제 LLM API 호출 구현
        # 현재는 원래 순서 그대로 반환
        return candidates
    
    def _prepare_prompt(self, context: str, token: str, candidates: List[MorphemeCandidate]) -> str:
        """LLM 프롬프트 준비"""
        # TODO: 프롬프트 템플릿 구현
        return ""
    
    def _parse_response(self, response: str) -> int:
        """LLM 응답 파싱하여 선택된 후보 인덱스 반환"""
        # TODO: 응답 파싱 구현
        return 0