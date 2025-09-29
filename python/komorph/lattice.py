from typing import List, Dict, Optional
from dataclasses import dataclass
from .rules import MorphemeCandidate


@dataclass
class LatticeNode:
    position: int
    candidate: object
    score: float
    backpointer: object = None

class MorphemeLattice:
    def __init__(self):
        self.nodes = []
    
    def build(self, token_candidates):
        self.nodes = []
        for pos, candidates in enumerate(token_candidates):
            layer = [
                LatticeNode(pos, cand, cand.score)
                for cand in candidates
            ]
            self.nodes.append(layer)
    
    def get_best_path(self):
        best_path = []
        for layer in self.nodes:
            if layer:
                best = max(layer, key=lambda n: n.score)
                best_path.append(best.candidate)
        return best_path
