from .normalize import normalize_text
from .tokenize import tokenize
from .dicts import MorphemeDictionary
from .rules import KoreanMorphemeRules
from .decoder import MorphemeDecoder
from .llm_rerank import LLMReranker

class Analyzer:
    def __init__(self, data_dir=None, use_llm=False, llm_provider=None):
        self.dictionary = MorphemeDictionary(data_dir)
        self.rules = KoreanMorphemeRules(self.dictionary)
        self.decoder = MorphemeDecoder()
        self.use_llm = use_llm
        self.llm_reranker = LLMReranker(llm_provider) if use_llm else None
    
    def analyze(self, text):
        normalized = normalize_text(text)
        tokens = tokenize(normalized)
        
        token_candidates = [
            self.rules.generate_candidates(tok) 
            for tok in tokens
        ]
        
        best_path = self.decoder.decode(token_candidates)
        
        results = []
        for tok, candidate in zip(tokens, best_path):
            token_result = [
                {"morph": m, "pos": p, "original": tok}
                for m, p in candidate.analysis
            ]
            results.append(token_result)
        
        return results
    
    def analyze_text(self, text):
        results = self.analyze(text)
        lines = []
        for token_result in results:
            if not token_result:
                continue
            original = token_result[0]["original"]
            morphs = " + ".join([f"{r['morph']}/{r['pos']}" for r in token_result])
            lines.append(f"{original}\t{morphs}")
        return "\n".join(lines)