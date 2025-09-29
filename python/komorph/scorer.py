from typing import List, Tuple
from .rules import MorphemeCandidate

class MorphemeScorer:
    def __init__(self):
        # 품사별 기본 점수
        self.pos_scores = {
            "N": 0.1,   # 명사
            "V": 0.2,   # 동사
            "A": 0.2,   # 형용사
            "J": 0.3,   # 조사
            "E": 0.3,   # 어미
        }
        
        # 품사 연접 점수 (bigram)
        self.transition_scores = {
            ("N", "J"): 0.5,    # 명사 + 조사
            ("V", "E"): 0.5,    # 동사 + 어미
            ("A", "E"): 0.5,    # 형용사 + 어미
        }
    
    def score_candidate(self, candidate: MorphemeCandidate) -> float:
        """후보에 대한 종합 점수 계산"""
        analysis = candidate.analysis
        score = candidate.score  # 기본 점수에서 시작
        
        # 1) 형태소 길이 보너스
        for morph, pos in analysis:
            if pos in ["N", "V", "A"]:  # 실질 형태소
                length_bonus = min(len(morph) * 0.05, 0.3)
                score += length_bonus
        
        # 2) 품사 연접 보너스
        if len(analysis) == 2:
            pos1, pos2 = analysis[0][1], analysis[1][1]
            if (pos1, pos2) in self.transition_scores:
                score += self.transition_scores[(pos1, pos2)]
        
        # 3) 너무 짧은 토큰 페널티
        total_length = sum(len(morph) for morph, _ in analysis)
        if total_length <= 1:
            score -= 0.2
        
        return score
    
    def rank_candidates(self, candidates: List[MorphemeCandidate]) -> List[MorphemeCandidate]:
        """후보들을 점수순으로 정렬"""
        for candidate in candidates:
            candidate.score = self.score_candidate(candidate)
        
        return sorted(candidates, key=lambda c: c.score, reverse=True)
