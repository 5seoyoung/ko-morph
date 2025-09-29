from typing import List, Dict, Optional
from dataclasses import dataclass
from .rules import MorphemeCandidate

@dataclass
class LatticeNode:
    """라티스 노드"""
    position: int
    candidate: MorphemeCandidate
    score: float
    backpointer: Optional['LatticeNode'] = None

class MorphemeLattice:
    """형태소 분석 라티스"""
    def __init__(self):
        self.nodes: List[List[LatticeNode]] = []
        self.sentence_length = 0
    
    def build(self, token_candidates: List[List[MorphemeCandidate]]):
        """토큰별 후보들로부터 라티스 구성"""
        self.sentence_length = len(token_candidates)
        self.nodes = []
        
        for pos, candidates in enumerate(token_candidates):
            layer = []
            for candidate in candidates:
                node = LatticeNode(
                    position=pos,
                    candidate=candidate,
                    score=candidate.score
                )
                layer.append(node)
            self.nodes.append(layer)
    
    def get_best_path(self) -> List[MorphemeCandidate]:
        """현재는 단순한 greedy selection (나중에 Viterbi로 교체)"""
        best_path = []
        for layer in self.nodes:
            best_node = max(layer, key=lambda n: n.score)
            best_path.append(best_node.candidate)
        
        return best_path
