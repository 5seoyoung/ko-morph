from typing import List
from .rules import MorphemeCandidate
from .lattice import MorphemeLattice
from .scorer import MorphemeScorer

class MorphemeDecoder:
    """형태소 분석 디코더"""
    def __init__(self):
        self.scorer = MorphemeScorer()
        self.lattice = MorphemeLattice()
    
    def decode(self, token_candidates: List[List[MorphemeCandidate]]) -> List[MorphemeCandidate]:
        """최적 형태소 분석 경로 찾기"""
        
        # 1) 모든 후보에 대해 점수 재계산
        scored_candidates = []
        for candidates in token_candidates:
            scored = self.scorer.rank_candidates(candidates)
            scored_candidates.append(scored)
        
        # 2) 라티스 구성
        self.lattice.build(scored_candidates)
        
        # 3) 최적 경로 찾기 (현재는 greedy, 추후 Viterbi로 교체)
        best_path = self.lattice.get_best_path()
        
        return best_path