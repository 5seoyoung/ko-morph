from typing import List, Dict, Tuple
from .utils import is_korean_token
from .dicts import MorphemeDictionary

class MorphemeCandidate:
    def __init__(self, analysis: List[Tuple[str, str]], score: float = 0.0, note: str = ""):
        self.analysis = analysis  # [(형태소, 품사), ...]
        self.score = score
        self.note = note
    
    def __repr__(self):
        return f"Candidate({self.analysis}, {self.score:.2f}, '{self.note}')"

class KoreanMorphemeRules:
    def __init__(self, dictionary: MorphemeDictionary):
        self.dict = dictionary
        
        # 모호한 어미/조사 (문맥에 따라 판단)
        self.ambiguous_suffixes = {"은", "는", "을", "를"}
    
    def generate_candidates(self, token: str) -> List[MorphemeCandidate]:
        """토큰에 대한 형태소 분석 후보들 생성"""
        candidates = []
        
        # 1) Baseline: 단일 명사로 처리
        candidates.append(MorphemeCandidate(
            analysis=[(token, "N")],
            score=0.1,
            note="baseline_noun"
        ))
        
        if not is_korean_token(token):
            return candidates
        
        # 2) 어미 분해 (동사/형용사 + 어미)
        for eomi in self.dict.eomi_sorted:
            if token.endswith(eomi) and len(token) > len(eomi):
                stem = token[:-len(eomi)]
                if len(stem) >= 1:  # 어간이 너무 짧지 않도록
                    candidates.append(MorphemeCandidate(
                        analysis=[(stem, "V"), (eomi, "E")],
                        score=0.6,
                        note=f"verb_stem+eomi({eomi})"
                    ))
                    break  # longest first
        
        # 3) 조사 분해 (명사 + 조사)
        for josa in self.dict.josa_sorted:
            if token.endswith(josa) and len(token) > len(josa):
                stem = token[:-len(josa)]
                if len(stem) >= 1:
                    score = 0.7
                    # 모호한 접미사는 조사로 해석하는 것을 선호
                    if josa in self.ambiguous_suffixes:
                        score = 0.8
                    
                    candidates.append(MorphemeCandidate(
                        analysis=[(stem, "N"), (josa, "J")],
                        score=score,
                        note=f"noun_stem+josa({josa})"
                    ))
                    break  # longest first
        
        return candidates

