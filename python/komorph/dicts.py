from pathlib import Path

class MorphemeDictionary:
    def __init__(self, data_dir=None):
        if data_dir is None:
            package_dir = Path(__file__).parent.parent.parent
            data_dir = package_dir / "data"
        
        self.data_dir = Path(data_dir)
        self.eomi = self._load_file("eomi152.txt")
        self.josa = self._load_file("josa96.txt")
        
        self.eomi_sorted = sorted(self.eomi, key=len, reverse=True)
        self.josa_sorted = sorted(self.josa, key=len, reverse=True)
        self.eomi_set = set(self.eomi)
        self.josa_set = set(self.josa)
        
        self._ensure_minimum_coverage()
    
    def _load_file(self, filename):
        filepath = self.data_dir / filename
        items = []
        
        if not filepath.exists():
            print(f"Warning: {filename} not found at {filepath}")
            return items
        
        for encoding in ['utf-8', 'utf-8-sig', 'cp949', 'euc-kr']:
            try:
                with open(filepath, 'r', encoding=encoding) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and not line.startswith('//'):
                            items.append(line)
                break
            except (UnicodeDecodeError, FileNotFoundError):
                continue
        
        seen = set()
        unique = []
        for item in items:
            if item and item not in seen:
                seen.add(item)
                unique.append(item)
        
        return unique
    
    def _ensure_minimum_coverage(self):
        """최소한의 기본 형태소 보장"""
        basic_josa = [
            "은", "는", "이", "가", "을", "를", "에", "에서", "에게", 
            "으로", "로", "과", "와", "의", "도", "만", "부터", "까지"
        ]
        basic_eomi = [
            "다", "요", "ㄴ다", "는다", "ㅂ니다", "습니다", "네요",
            "고", "지만", "면", "는데", "아서", "어서", "니까",
            "았다", "었다", "겠다", "ㄹ까요", "ㄹ게요"
        ]
        
        for j in basic_josa:
            if j not in self.josa_set:
                self.josa.append(j)
                self.josa_set.add(j)
        
        for e in basic_eomi:
            if e not in self.eomi_set:
                self.eomi.append(e)
                self.eomi_set.add(e)
        
        self.eomi_sorted = sorted(self.eomi, key=len, reverse=True)
        self.josa_sorted = sorted(self.josa, key=len, reverse=True)

