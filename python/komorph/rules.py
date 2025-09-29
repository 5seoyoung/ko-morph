from .utils import is_korean_token

class MorphemeCandidate:
    def __init__(self, analysis, score=0.0, note=""):
        self.analysis = analysis
        self.score = score
        self.note = note
    
    def __repr__(self):
        morphs = "+".join([f"{m}/{p}" for m, p in self.analysis])
        return f"[{morphs}] ({self.score:.2f})"

class KoreanMorphemeRules:
    def __init__(self, dictionary):
        self.dict = dictionary
    
    def generate_candidates(self, token):
        candidates = []
        
        # Baseline: 명사
        candidates.append(MorphemeCandidate(
            analysis=[(token, "N")],
            score=0.1,
            note="baseline"
        ))
        
        if not is_korean_token(token):
            if token.isdigit():
                candidates[-1] = MorphemeCandidate(
                    analysis=[(token, "NUM")],
                    score=0.9,
                    note="number"
                )
            elif token.isalpha():
                candidates[-1] = MorphemeCandidate(
                    analysis=[(token, "ENG")],
                    score=0.9,
                    note="english"
                )
            elif token in '.!?':
                candidates[-1] = MorphemeCandidate(
                    analysis=[(token, "SF")],
                    score=1.0,
                    note="sentence_final"
                )
            elif token in ',;:':
                candidates[-1] = MorphemeCandidate(
                    analysis=[(token, "SP")],
                    score=1.0,
                    note="punctuation"
                )
            return candidates
        
        # 어미 분해 시도
        for eomi in self.dict.eomi_sorted:
            if len(token) > len(eomi) and token.endswith(eomi):
                stem = token[:-len(eomi)]
                if len(stem) >= 1:
                    candidates.append(MorphemeCandidate(
                        analysis=[(stem, "V"), (eomi, "E")],
                        score=0.6,
                        note=f"verb+{eomi}"
                    ))
                    break
        
        # 조사 분해 시도
        for josa in self.dict.josa_sorted:
            if len(token) > len(josa) and token.endswith(josa):
                stem = token[:-len(josa)]
                if len(stem) >= 1:
                    score = 0.75 if josa in ["은", "는", "이", "가"] else 0.7
                    candidates.append(MorphemeCandidate(
                        analysis=[(stem, "N"), (josa, "J")],
                        score=score,
                        note=f"noun+{josa}"
                    ))
                    break
        
        return candidates