from typing import List, Dict, Any
from .normalize import normalize_text
from .tokenize import tokenize
from .dicts import MorphemeDictionary
from .rules import KoreanMorphemeRules, MorphemeCandidate
from .decoder import MorphemeDecoder
from .llm_rerank import LLMReranker

class Analyzer:
    """한국어 형태소 분석기 메인 클래스"""
    
    def __init__(self, data_dir: str = None, use_llm: bool = False, llm_provider: str = None):
        self.dictionary = MorphemeDictionary(data_dir)
        self.rules = KoreanMorphemeRules(self.dictionary)
        self.decoder = MorphemeDecoder()
        self.use_llm = use_llm
        
        if use_llm:
            self.llm_reranker = LLMReranker(provider=llm_provider)
        else:
            self.llm_reranker = None
    
    def analyze(self, text: str) -> List[List[Dict[str, Any]]]:
        """문장 형태소 분석"""
        # 1) 전처리
        normalized_text = normalize_text(text)
        
        # 2) 토크나이징
        tokens = tokenize(normalized_text)
        
        # 3) 각 토큰별 후보 생성
        token_candidates = []
        for token in tokens:
            candidates = self.rules.generate_candidates(token)
            token_candidates.append(candidates)
        
        # 4) 디코딩 (최적 경로 찾기)
        best_path = self.decoder.decode(token_candidates)
        
        # 5) LLM 재랭킹 (옵션)
        if self.use_llm and self.llm_reranker and self.llm_reranker.is_available():
            best_path = self._apply_llm_reranking(tokens, token_candidates, best_path)
        
        # 6) 결과 포맷팅
        results = []
        for token_idx, candidate in enumerate(best_path):
            token_result = []
            for morph, pos in candidate.analysis:
                token_result.append({
                    "morph": morph,
                    "pos": pos,
                    "original": tokens[token_idx]
                })
            results.append(token_result)
        
        return results
    
    def _apply_llm_reranking(self, tokens: List[str], 
                           token_candidates: List[List[MorphemeCandidate]], 
                           current_best: List[MorphemeCandidate]) -> List[MorphemeCandidate]:
        """LLM을 이용한 재랭킹"""
        # TODO: 실제 LLM 재랭킹 구현
        # 현재는 원래 결과 그대로 반환
        return current_best
    
    def analyze_text(self, text: str) -> str:
        """분석 결과를 텍스트 형태로 반환"""
        results = self.analyze(text)
        lines = []
        
        for i, token_result in enumerate(results):
            morphs = " + ".join([f"{item['morph']}/{item['pos']}" for item in token_result])
            original = token_result[0]['original'] if token_result else ""
            lines.append(f"{original}\t{morphs}")
        
        return "\n".join(lines)
