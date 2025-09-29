from typing import List
from .rules import MorphemeCandidate
from .lattice import MorphemeLattice
from .lattice import MorphemeLattice
from .scorer import MorphemeScorer

class MorphemeDecoder:
    def __init__(self):
        self.scorer = MorphemeScorer()
        self.lattice = MorphemeLattice()
    
    def decode(self, token_candidates):
        scored = []
        for candidates in token_candidates:
            ranked = self.scorer.rank_candidates(candidates)
            scored.append(ranked)
        
        self.lattice.build(scored)
        return self.lattice.get_best_path()