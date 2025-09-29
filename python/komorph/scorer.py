from typing import List, Tuple
from .rules import MorphemeCandidate

class MorphemeScorer:
    def __init__(self):
        self.transition_scores = {
            ("N", "J"): 0.5,
            ("V", "E"): 0.5,
            ("A", "E"): 0.5,
        }
    
    def score_candidate(self, candidate):
        score = candidate.score
        analysis = candidate.analysis
        
        for morph, pos in analysis:
            if pos in ["N", "V", "A"] and len(morph) >= 2:
                score += min(len(morph) * 0.03, 0.2)
        
        if len(analysis) == 2:
            pos1, pos2 = analysis[0][1], analysis[1][1]
            if (pos1, pos2) in self.transition_scores:
                score += self.transition_scores[(pos1, pos2)]
        
        total_len = sum(len(m) for m, _ in analysis)
        if total_len <= 1:
            score -= 0.2
        
        return score
    
    def rank_candidates(self, candidates):
        for cand in candidates:
            cand.score = self.score_candidate(cand)
        return sorted(candidates, key=lambda c: c.score, reverse=True)
