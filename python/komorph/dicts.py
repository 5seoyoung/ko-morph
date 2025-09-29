from pathlib import Path
from typing import List, Set
import os

class MorphemeDictionary:
    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # 패키지 상대 경로로 data 디렉토리 찾기
            package_dir = Path(__file__).parent.parent.parent
            data_dir = package_dir / "data"
        
        self.data_dir = Path(data_dir)
        self.eomi = self._load_file("eomi152.txt")
        self.josa = self._load_file("josa96.txt")
        
        # 길이순 정렬 (longest first matching용)
        self.eomi_sorted = sorted(self.eomi, key=len, reverse=True)
        self.josa_sorted = sorted(self.josa, key=len, reverse=True)
        
        # 빠른 lookup을 위한 set
        self.eomi_set = set(self.eomi)
        self.josa_set = set(self.josa)
        
        # fallback 기본 리스트
        self._add_fallbacks()
    
    def _load_file(self, filename: str) -> List[str]:
        """파일에서 형태소 목록 로드"""
        filepath = self.data_dir / filename
        items = []
        
        if not filepath.exists():
            return items
        
        try:
            # 다양한 인코딩 시도
            for encoding in ['utf-8', 'cp949', 'euc-kr', 'utf-8-sig']:
                try:
                    with open(filepath, 'r', encoding=encoding) as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#'):
                                items.append(line)
                    break
                except UnicodeDecodeError:
                    continue
        except Exception as e:
            print(f"Warning: Failed to load {filename}: {e}")
        
        # 중복 제거
        seen = set()
        unique_items = []
        for item in items:
            if item not in seen:
                seen.add(item)
                unique_items.append(item)
        
        return unique_items
    
    def _add_fallbacks(self):
        """기본 형태소가 부족할 경우 fallback 추가"""
        if len(self.josa) < 20:
            fallback_josa = [
                "은", "는", "이", "가", "을", "를", "에", "에서", "에게", "으로", "로",
                "과", "와", "보다", "의", "도", "만", "까지", "부터", "마다", "처럼"
            ]
            self.josa.extend([j for j in fallback_josa if j not in self.josa_set])
            self._update_sorted_lists()
        
        if len(self.eomi) < 30:
            fallback_eomi = [
                "다", "요", "니다", "네요", "습니다", "합니다", "한다", "했다",
                "고", "게", "도록", "면", "지만", "니까", "는데", "아서", "어서",
                "며", "었다", "겠다", "라서", "잖아", "네"
            ]
            self.eomi.extend([e for e in fallback_eomi if e not in self.eomi_set])
            self._update_sorted_lists()
    
    def _update_sorted_lists(self):
        """정렬된 리스트 업데이트"""
        self.eomi_sorted = sorted(self.eomi, key=len, reverse=True)
        self.josa_sorted = sorted(self.josa, key=len, reverse=True)
        self.eomi_set = set(self.eomi)
        self.josa_set = set(self.josa)
